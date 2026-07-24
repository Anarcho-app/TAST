#!/usr/bin/env python3
"""
TAST Bayesian Core — Skepticism-First Edition (v5.1)

Single parameter: victors_reliability ∈ [0.0, 1.0]
  1.0 = treat census / manifest / ledger counts as approximately accurate
  0.0 = maximal skepticism: all quantitative head-counts become UNDEFINED;
        only qualitative / physical / meta patterns survive.

Core epistemic rules (v5.1):
  See also model/inference_extensions.py for functional dependence,
  multi-axis reliability, correlation damping, and adversarial hooks.
  1. Estimates calculated from the administrative records are CONDITIONAL
     ESTIMATES derived from biased sources (victors' paperwork).
     They are NEVER facts. Language that converts them into facts
     ("least-bad", "best available", "robust after correction", etc.)
     is forbidden under --strict (default on).
  2. The focal population is multi-generational American lineages of African
     and mixed ancestry (Freedmen’s Bureau-era and earlier U.S. lineages)
     whose genealogical chains predominantly terminate in pre-1865 U.S. records.
     Continental-African framing is not the unmarked identity label for this group.

Usage:
  python bayesian_core.py --reliability 0.0
  python bayesian_core.py --reliability 1.0 --verbose
  python bayesian_core.py --list-streams
  python bayesian_core.py --self-test
  python bayesian_core.py --reliability 0.7 --no-strict   # disable language guard
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STREAMS_CSV = HERE / "evidence_streams.csv"
SURVIVING_MD = ROOT / "surviving" / "qualitative_claims.md"
CLAIMS_CI_CSV = ROOT / "data" / "sources_registry_with_ci.csv"

HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]
H_LABELS = {
    "H1": "Documented transatlantic arrivals + exceptional natural increase under U.S. conditions",
    "H2": "Classification / absorption processes operating on American soil",
    "H3": "Hybrid mechanisms (partial absorption + moderate structural advantage on American soil)",
    "H4": "U.S.-specific structural conditions (natural increase via local regime features)",
    "H5": "Mixed / undocumented mechanisms (honest uncertainty; residual includes possibility that administrative categories obscure distinct American trajectories)",
}

# RAW_PRIORS derivation (v5.3): uncertainty-favoring 8:15:20:20:47 / 110 parts.
# H1=8/110 … H5=47/110. Not fitted to data. At r≈0 posterior returns here.
RAW_PRIORS = {
    "H1": 0.0727,
    "H2": 0.1364,
    "H3": 0.1818,
    "H4": 0.1818,
    "H5": 0.4273,
}

REQUIRED_COLUMNS = {"stream_id", "name", "H1", "H2", "H3", "H4", "H5", "group", "is_quantitative"}

# Phrases that convert a biased-source estimate into a fact-like claim.
# Banned under --strict (default).
BANNED_PHRASES = [
    # Fact-conversion language
    "least-bad",
    "least bad",
    "best available",
    "best-available",
    "robust after correction",
    "robust after adjustment",
    "the historical consensus",
    "accepted fact",
    "established fact",
    "known fact",
    "as a fact",
    "is a fact",
    # Identity-proxy / continental collapse language (when used as unmarked label
    # for multi-generational U.S. lineages)
    "the african american population as africans",
    "black americans as africans",
    "african stock in america",
    "african stock in the united states",
    "perpetual african origin",
    "continental african identity for fba",
]

DISCLAIMER = (
    "CONDITIONAL ESTIMATE derived from biased administrative records "
    "(victors' paperwork). This is NOT A FACT."
)

# Preferred descriptors for the focal population (multi-generational U.S. lineages).
# Continental-African framing is reserved for documented arrivals or genetic reference panels.
POPULATION_DESCRIPTOR = (
    "multi-generational American lineages of African and mixed ancestry "
    "(Freedmen’s Bureau-era and earlier U.S. lineages whose genealogical chains "
    "predominantly terminate in pre-1865 U.S. records)"
)


class StreamLoadError(Exception):
    pass


class StrictLanguageError(Exception):
    pass


def load_streams(path: Path = STREAMS_CSV) -> List[Dict]:
    if not path.exists():
        raise StreamLoadError(f"Streams file not found: {path}")

    streams = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise StreamLoadError("CSV has no header row")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise StreamLoadError(f"Missing required columns: {sorted(missing)}")

        for i, row in enumerate(reader, start=2):
            try:
                sid = int(row["stream_id"])
                is_q = int(row.get("is_quantitative", 1))
                if is_q not in (0, 1):
                    raise ValueError("is_quantitative must be 0 or 1")

                lik = {}
                for h in HYPOTHESES:
                    val = float(row[h])
                    if not (0.0 <= val <= 1.0):
                        raise ValueError(f"{h}={val} outside [0,1]")
                    lik[h] = val

                streams.append({
                    "stream_id": sid,
                    "name": row["name"].strip(),
                    "group": row.get("group", "").strip(),
                    "coverage": row.get("coverage", "").strip(),
                    "provenance": row.get("provenance", "").strip(),
                    "is_quantitative": is_q,
                    **lik,
                })
            except (ValueError, KeyError) as e:
                raise StreamLoadError(f"Row {i}: {e}") from e

    if not streams:
        raise StreamLoadError("No streams loaded")
    return streams


def apply_reliability(streams: List[Dict], reliability: float) -> List[Dict]:
    r = max(0.0, min(1.0, reliability))
    scaled = []
    for s in streams:
        news = dict(s)
        if s["is_quantitative"] == 1:
            for h in HYPOTHESES:
                L = s[h]
                news[h] = r * L + (1.0 - r) * 0.5
        scaled.append(news)
    return scaled


def bayes_update(streams: List[Dict], priors: Dict[str, float]) -> Dict[str, float]:
    """Independent product of likelihoods in log-space. Explicit independence assumption."""
    log_post = {h: math.log(priors[h] + 1e-30) for h in HYPOTHESES}
    for s in streams:
        for h in HYPOTHESES:
            L = max(s[h], 1e-12)
            log_post[h] += math.log(L)
    max_log = max(log_post.values())
    unnorm = {h: math.exp(log_post[h] - max_log) for h in HYPOTHESES}
    total = sum(unnorm.values())
    return {h: unnorm[h] / total for h in HYPOTHESES}


def load_surviving_claims(path: Path = SURVIVING_MD) -> List[str]:
    if not path.exists():
        return ["[surviving/qualitative_claims.md not found]"]
    text = path.read_text(encoding="utf-8")
    claims = []
    for line in text.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if m:
            claims.append(m.group(2).strip())
    return claims


def print_surviving(claims: Optional[List[str]] = None):
    if claims is None:
        claims = load_surviving_claims()
    print("\n=== SURVIVING QUALITATIVE CLAIMS (reliability → 0) ===")
    print("(Loaded from surviving/qualitative_claims.md — strict filter applied)")
    for i, c in enumerate(claims, 1):
        print(f"  {i}. {c}")
    print()


def check_banned_language(text: str, strict: bool) -> None:
    """Raise if banned phrases appear under --strict."""
    if not strict:
        return
    lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            raise StrictLanguageError(
                f"Banned phrase detected under --strict: '{phrase}'. "
                "Estimates from biased administrative records are never facts."
            )



# ---------------------------------------------------------------------------
# Per-claim confidence (simple, transparent, rule-derived)
# ---------------------------------------------------------------------------
def load_claim_confidences(path: Path = CLAIMS_CI_CSV) -> list:
    """Return list of dicts with claim_id, claim, confidence_ci, provenance, enslaved_source."""
    if not path.exists():
        return []
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                row["confidence_ci"] = float(row["confidence_ci"])
            except (KeyError, ValueError):
                row["confidence_ci"] = 0.40
            rows.append(row)
    return rows


def summarize_confidences(rows: list, threshold: float = 0.70) -> None:
    if not rows:
        print("  [no claim confidence file]")
        return
    cis = [r["confidence_ci"] for r in rows]
    print(f"  Claims with c_i: {len(cis)}")
    print(f"  min={min(cis):.2f}  median={sorted(cis)[len(cis)//2]:.2f}  max={max(cis):.2f}  mean={sum(cis)/len(cis):.2f}")
    print(f"  c_i >= {threshold:.2f}: {sum(1 for c in cis if c >= threshold)}")


# ---------------------------------------------------------------------------
# Monte Carlo over reliability + modest likelihood noise
# ---------------------------------------------------------------------------
def monte_carlo_posteriors(
    streams: list,
    priors: dict,
    r_center: float,
    n_samples: int = 500,
    r_noise: float = 0.05,
    lik_noise: float = 0.03,
    seed: int = 42,
) -> dict:
    """
    Sample posteriors by:
      - drawing r ~ clipped Normal(r_center, r_noise)
      - adding small Gaussian noise to each likelihood (clipped to [0.01, 0.99])
      - running the existing Bayes update
    Returns dict of hypothesis -> list of posterior samples.
    At low r the mass still collapses toward the qualitative floor.
    Fully re-runnable by any agent with the same seed.
    """
    rng = random.Random(seed)
    samples = {h: [] for h in HYPOTHESES}

    for _ in range(n_samples):
        r = r_center + rng.gauss(0, r_noise)
        r = max(0.0, min(1.0, r))
        # perturb streams
        noisy = []
        for s in streams:
            news = dict(s)
            if s["is_quantitative"] == 1:
                for h in HYPOTHESES:
                    L = s[h] + rng.gauss(0, lik_noise)
                    L = max(0.01, min(0.99, L))
                    # then apply reliability
                    news[h] = r * L + (1.0 - r) * 0.5
            else:
                # non-quantitative: leave original (or tiny noise)
                for h in HYPOTHESES:
                    L = s[h] + rng.gauss(0, lik_noise * 0.3)
                    news[h] = max(0.01, min(0.99, L))
            noisy.append(news)
        post = bayes_update(noisy, priors)
        for h in HYPOTHESES:
            samples[h].append(post[h])
    return samples


def summarize_mc(samples: dict, quantiles=(0.05, 0.50, 0.95)) -> None:
    print("\nMonte Carlo posterior summary (quantiles):")
    print(f"{'H':<4} {'5%':>8} {'50%':>8} {'95%':>8} {'mean':>8}")
    for h in HYPOTHESES:
        xs = sorted(samples[h])
        n = len(xs)
        qvals = [xs[int(q * (n - 1))] for q in quantiles]
        mean = sum(xs) / n
        print(f"{h:<4} {qvals[0]:8.1%} {qvals[1]:8.1%} {qvals[2]:8.1%} {mean:8.1%}")
    print("(Independence of streams still assumed — known limitation.)")
    print(DISCLAIMER)



def run_self_test() -> bool:
    print("Running self-tests (v5.3)...")
    ok = True

    try:
        streams = load_streams()
        print(f"  [PASS] load_streams: {len(streams)} streams")
    except StreamLoadError as e:
        print(f"  [FAIL] load_streams: {e}")
        return False

    q_count = sum(1 for s in streams if s["is_quantitative"] == 1)
    nq_count = len(streams) - q_count
    print(f"  [INFO] quantitative={q_count}, non-quantitative={nq_count}")

    s0 = apply_reliability(streams, 0.0)
    s1 = apply_reliability(streams, 1.0)
    for orig, scaled0, scaled1 in zip(streams, s0, s1):
        if orig["is_quantitative"] == 1:
            for h in HYPOTHESES:
                if abs(scaled0[h] - 0.5) > 1e-9:
                    print(f"  [FAIL] reliability=0 should push quantitative to 0.5")
                    ok = False
                if abs(scaled1[h] - orig[h]) > 1e-9:
                    print(f"  [FAIL] reliability=1 should preserve original likelihoods")
                    ok = False
        else:
            for h in HYPOTHESES:
                if abs(scaled0[h] - orig[h]) > 1e-9 or abs(scaled1[h] - orig[h]) > 1e-9:
                    print(f"  [FAIL] non-quantitative streams must be unchanged by reliability")
                    ok = False
    if ok:
        print("  [PASS] apply_reliability extremes")

    post = bayes_update(streams, RAW_PRIORS)
    s = sum(post.values())
    if abs(s - 1.0) > 1e-6:
        print(f"  [FAIL] posterior sum = {s}")
        ok = False
    else:
        print(f"  [PASS] posterior sums to 1.0 (H5 ≈ {post['H5']:.1%})")

    claims = load_surviving_claims()
    if len(claims) < 5:
        print(f"  [FAIL] expected >=5 surviving claims, got {len(claims)}")
        ok = False
    else:
        print(f"  [PASS] load_surviving_claims: {len(claims)} claims")

    psum = sum(RAW_PRIORS.values())
    if abs(psum - 1.0) > 1e-4:
        print(f"  [FAIL] priors sum to {psum}")
        ok = False
    else:
        print("  [PASS] priors sum to 1.0")

    # New v5.1 checks
    try:
        check_banned_language("This is the least-bad source we have.", strict=True)
        print("  [FAIL] banned-phrase detector did not raise")
        ok = False
    except StrictLanguageError:
        print("  [PASS] banned-phrase detector raises on 'least-bad'")

    try:
        check_banned_language(DISCLAIMER, strict=True)
        print("  [PASS] disclaimer itself contains no banned phrases")
    except StrictLanguageError as e:
        print(f"  [FAIL] disclaimer triggered ban: {e}")
        ok = False

    # Ensure quantitative output path would include the disclaimer
    if "NOT A FACT" not in DISCLAIMER or "biased" not in DISCLAIMER.lower():
        print("  [FAIL] DISCLAIMER constant missing required language")
        ok = False
    else:
        print("  [PASS] DISCLAIMER constant contains required 'NOT A FACT' language")

    # Claim confidence file
    claims = load_claim_confidences()
    if len(claims) < 100:
        print(f"  [FAIL] expected >=100 claims with c_i, got {len(claims)}")
        ok = False
    else:
        print(f"  [PASS] load_claim_confidences: {len(claims)} claims")
        summarize_confidences(claims)

    # Monte Carlo smoke test
    try:
        streams = load_streams()
        mc = monte_carlo_posteriors(streams, RAW_PRIORS, r_center=0.8, n_samples=50, seed=1)
        if len(mc["H5"]) != 50:
            print("  [FAIL] MC sample count mismatch")
            ok = False
        else:
            print("  [PASS] monte_carlo_posteriors smoke (50 samples)")
    except Exception as e:
        print(f"  [FAIL] monte_carlo_posteriors: {e}")
        ok = False

    print("Self-test", "PASSED" if ok else "FAILED")
    return ok


def main():
    parser = argparse.ArgumentParser(
        description="TAST Bayesian Core v5.3 — reliability slider (0.0 = maximal skepticism)"
    )
    parser.add_argument("--reliability", type=float, default=1.0,
                        help="victors_reliability ∈ [0.0, 1.0] (default 1.0)")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--list-streams", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--strict", action="store_true", default=True,
                        help="Enforce language ban on fact-conversion phrases (default: on)")
    parser.add_argument("--no-strict", action="store_true",
                        help="Disable language ban (not recommended)")
    parser.add_argument("--monte-carlo", type=int, default=0, metavar="N",
                        help="Run N Monte Carlo samples over reliability + likelihood noise (0 = off)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for Monte Carlo")
    parser.add_argument("--show-claims", action="store_true",
                        help="Summarize per-claim confidence scores and exit")
    parser.add_argument("--dampen", type=float, default=0.0, metavar="S",
                        help="Group-level correlation damping strength in [0,1] (0=independent)")
    args = parser.parse_args()

    strict = not args.no_strict

    if args.self_test:
        sys.exit(0 if run_self_test() else 1)

    try:
        streams = load_streams()
    except StreamLoadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "dampen", 0) and args.dampen > 0:
        try:
            from inference_extensions import damp_correlated_streams
            streams = damp_correlated_streams(streams, strength=float(args.dampen))
            print(f"[info] correlation damping strength={args.dampen:.2f}")
        except Exception as e:
            print(f"[warn] dampen unavailable: {e}")

    r = max(0.0, min(1.0, args.reliability))

    if args.show_claims:
        claims = load_claim_confidences()
        summarize_confidences(claims)
        # show a few high and low
        if claims:
            sorted_c = sorted(claims, key=lambda x: x["confidence_ci"], reverse=True)
            print("\nTop 5 by c_i:")
            for row in sorted_c[:5]:
                print(f"  {row['confidence_ci']:.2f}  [{row['claim_id']}] {row['claim'][:70]}")
            print("\nBottom 5 by c_i:")
            for row in sorted_c[-5:]:
                print(f"  {row['confidence_ci']:.2f}  [{row['claim_id']}] {row['claim'][:70]}")
        return

    if args.list_streams:
        print(f"{'ID':>3}  {'Q':>1}  {'Group':>5}  Name")
        for s in streams:
            q = "Q" if s["is_quantitative"] else " "
            print(f"{s['stream_id']:3d}  {q}  {s['group']:>5}  {s['name']}")
        return

    print(f"TAST Bayesian Core v5.3  |  victors_reliability = {r:.2f}  |  strict={strict}")
    print("=" * 70)

    if r < 0.05:
        print("\n*** MAXIMAL SKEPTICISM MODE ***")
        print("Administrative head-counts, growth rates, and import totals")
        print("derived from owner/trader/enumerator records: UNDEFINED.")
        print("Physical and structural floor remains (see surviving/quantitative_floor.md).")
        print_surviving()
        # TRUE collapse (Claude Opus audit): when administrative reliability ≈ 0,
        # mechanism labels H1–H5 are not settled by hand-tuned floor likelihoods.
        # Posterior returns to the prior. Physical/structural presence remains
        # in the surviving claims + observable facts + physical_loglik report.
        print("\nMechanism posterior at r≈0: returns to PRIOR")
        print("(Administrative streams excluded; floor is not used to force H1–H5.)")
        for h in HYPOTHESES:
            bar = "█" * int(RAW_PRIORS[h] * 40)
            print(f"  {h}  {RAW_PRIORS[h]:6.1%}  {bar}")
        # Optional: report physical floor loglik as presence support, not mechanism ranking
        try:
            from physical_likelihoods import physical_loglik
            params = {
                "lambda_growth": 0.015,
                "rho_reclass": 0.25,
                "r_owner": 0.0,
                "r_enumerator": 0.0,
                "undercount": 0.15,
            }
            pll = physical_loglik(params)
            print(f"\nPhysical-floor log-likelihood (presence/structure support): {pll:.2f}")
            print("(Not used to rank H1–H5 at r≈0.)")
        except Exception as e:
            print(f"\nPhysical-floor loglik unavailable: {e}")
        print(f"\n  {DISCLAIMER}")
        print("Meta-claim: No national-scale administrative total is a fact.")
        return

    # Quantitative path — must carry the strong disclaimer
    scaled = apply_reliability(streams, r)
    post = bayes_update(scaled, RAW_PRIORS)

    print("\n" + DISCLAIMER)
    print("-" * 70)
    print("Hypothesis posteriors (conditioned on reliability):")
    print("(Independence of streams is assumed — a known modeling limitation.)")
    for h in HYPOTHESES:
        bar = "█" * int(post[h] * 40)
        print(f"  {h}  {post[h]:6.1%}  {bar}")
        if args.verbose:
            print(f"       {H_LABELS[h]}")

    print("\nConditioning statement:")
    print(f'  "If we treat the recorded population totals as approximately accurate')
    print(f'   (victors_reliability ≈ {r:.2f}), then the above posteriors obtain;')
    print(f'   if we do not, the quantitative claims are undefined."')
    print(f"\n  {DISCLAIMER}")

    if args.monte_carlo and args.monte_carlo > 0:
        print(f"\n--- Monte Carlo ({args.monte_carlo} samples, seed={args.seed}) ---")
        samples = monte_carlo_posteriors(
            streams, RAW_PRIORS, r_center=r,
            n_samples=args.monte_carlo, seed=args.seed
        )
        summarize_mc(samples)

    # Language guard on any verbose labels
    if strict:
        for label in H_LABELS.values():
            try:
                check_banned_language(label, strict=True)
            except StrictLanguageError as e:
                print(f"WARNING: {e}", file=sys.stderr)

    if r < 0.5:
        print("\n(Note: reliability < 0.5 → quantitative streams heavily diluted;")
        print(" physical burial, aDNA-site, and meta-skepticism streams dominate.)")
        print_surviving()


if __name__ == "__main__":
    main()
