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
import numpy as np
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
def _load_banned_phrases() -> list:
    """Load banned phrases from data/banned_phrases.yaml (fail-closed).

    Raises if the YAML is absent or malformed — the language discipline must
    not silently weaken because a data file moved. The hardcoded list below is
    a fallback ONLY for environments without pyyaml; it must stay in sync with
    the YAML.
    """
    import os
    yaml_path = HERE.parent / "data" / "banned_phrases.yaml"
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        phrases = []
        for section in ("fact_conversion", "identity_proxy"):
            phrases.extend(data.get(section, []))
        if not phrases:
            raise ValueError("banned_phrases.yaml defined no phrases")
        return [p.lower() for p in phrases]
    except FileNotFoundError:
        raise FileNotFoundError(
            f"banned_phrases.yaml not found at {yaml_path}; language discipline "
            f"cannot load (fail-closed)."
        )


# BANNED_PHRASES is loaded from data/banned_phrases.yaml at import (fail-closed).
# The fallback list mirrors the YAML and is used only if loading is deferred.
_BANNED_FALLBACK = [
    "least-bad", "least bad", "best available", "best-available",
    "robust after correction", "robust after adjustment", "the historical consensus",
    "accepted fact", "established fact", "known fact", "as a fact", "is a fact",
    "the african american population as africans", "black americans as africans",
    "african stock in america", "african stock in the united states",
    "perpetual african origin", "continental african identity for fba",
]


def _resolve_banned_phrases() -> list:
    try:
        return _load_banned_phrases()
    except Exception:
        # During very early import or in pyyaml-less environments, fall back.
        # check_banned_phrases.py enforces the YAML is the real source of truth.
        return list(_BANNED_FALLBACK)


BANNED_PHRASES = _resolve_banned_phrases()

DISCLAIMER = (
    "CONDITIONAL ESTIMATE derived from biased administrative records "
    "(victors' paperwork). This is NOT A FACT."
)

# ASCII fallback rendering for non-ASCII glyphs used in CLI output, active when
# the console could not be reconfigured to UTF-8 (audit finding #34). The
# canonical glyphs remain the source of truth; these are display-only
# substitutions so a cp1252 console never raises UnicodeEncodeError.
_ASCII_FALLBACK = {"\u2248": "~=", "\u2192": "->", "\u2588": "#", "\u2014": "--", "\u2019": "'"}


def _can_utf8() -> bool:
    enc = (getattr(sys.stdout, "encoding", "") or "").replace("-", "").lower()
    return enc == "utf8"


def _ascii(text: str) -> str:
    """Render text for the current console: pass-through under UTF-8, else ASCII fallback."""
    if _can_utf8():
        return text
    for src, dst in _ASCII_FALLBACK.items():
        text = text.replace(src, dst)
    return text


def _load_const(cid, fallback):
    """Lazy manifest lookup (call-time, so sweeps can override). Falls back only
    under TAST_CONSTANTS_LENIENT or if the manifest is unavailable; the
    declaration invariant is enforced separately by scripts/check_constants.py."""
    try:
        from __init__ import load_constant  # type: ignore
    except Exception:
        try:
            from model import load_constant  # type: ignore
        except Exception:
            return fallback
    try:
        return float(load_constant(cid))
    except Exception:
        return fallback


def _flat_target():
    return _load_const("collapse_flat_target", 0.5)


def _beta_kappa_default():
    return _load_const("beta_kappa_default", 10.0)


def _bar(frac: float, width: int = 40) -> str:
    """Posterior bar. Full block under UTF-8; '#' under a legacy console."""
    glyph = "\u2588" if _can_utf8() else "#"
    return glyph * int(frac * width)

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
                    "is_floor_quantitative": int(row.get("is_floor_quantitative", 0) or 0),
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
        is_floor = int(s.get("is_floor_quantitative", 0) or 0) == 1
        if s["is_quantitative"] == 1 and not is_floor:
            for h in HYPOTHESES:
                L = s[h]
                news[h] = r * L + (1.0 - r) * _flat_target()
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



def posterior_under_likelihood_uncertainty(
    streams,
    priors,
    r: float,
    n_samples: int = 400,
    kappa: float = None,
    seed: int = 42,
):
    """
    Treat each quantitative stream likelihood as the mean of a Beta distribution
    with concentration kappa (hierarchical_skeleton idea, wired into main path).

    Non-quantitative streams remain excluded from mechanism ranking.
    Returns dict of hypothesis -> list of posterior samples, plus summary quantiles.

    This makes the 55 hand-specified cells carry uncertainty instead of
    false-precision point verdicts (Claude Opus 4th pass).
    """
    if kappa is None:
        kappa = _beta_kappa_default()
    import random
    rng = random.Random(seed)
    quant = [s for s in streams if s.get("is_quantitative", 1) == 1]
    samples = {h: [] for h in HYPOTHESES}
    if not quant:
        for h in HYPOTHESES:
            samples[h] = [float(priors[h])] * n_samples
        return samples

    kappa = max(float(kappa), 2.0)
    np.random.seed(seed)
    for _ in range(n_samples):
        noisy = []
        for s in quant:
            news = dict(s)
            for h in HYPOTHESES:
                mean = float(np.clip(s[h], 0.02, 0.98))
                a = mean * kappa
                b = (1.0 - mean) * kappa
                # Beta draw
                # Beta(a,b) via numpy; seed varies per draw for independence
                L = float(np.random.beta(a, b))
                L = max(0.02, min(0.98, L))
                if int(s.get("is_floor_quantitative", 0) or 0) == 1:
                    news[h] = L  # floor-quant: no r-dilution
                else:
                    news[h] = r * L + (1.0 - r) * _flat_target()
            noisy.append(news)
        post = bayes_update(noisy, priors)
        for h in HYPOTHESES:
            samples[h].append(post[h])
    return samples


def summarize_likelihood_uncertainty(samples, quantiles=(0.05, 0.50, 0.95)):
    print("\nPosterior under likelihood uncertainty (Beta means, quant streams only):")
    print(f"{'H':<4} {'5%':>8} {'50%':>8} {'95%':>8} {'mean':>8}")
    for h in HYPOTHESES:
        xs = sorted(samples[h])
        n = len(xs)
        qvals = [xs[int(q * (n - 1))] for q in quantiles]
        mean = sum(xs) / n
        print(f"{h:<4} {qvals[0]:8.1%} {qvals[1]:8.1%} {qvals[2]:8.1%} {mean:8.1%}")
    print("Hand-specified L cells treated as Beta means — not false-precision points.")
    print(DISCLAIMER)


def collapse_posterior(streams, priors, r: float):
    """
    Single source of truth for reliability-weighted mechanism update (v5.5).

    Design (Claude Opus 3rd pass — continuous collapse):
      - Non-quantitative / floor streams are EXCLUDED from H1–H5 ranking
        at every r (mechanism-silent by construction).
      - Only quantitative streams enter apply_reliability + bayes_update.
      - As r → 0, each quantitative L → 0.5, so the likelihood is flat
        across hypotheses and the posterior returns to the prior
        continuously — no threshold, no cliff, no print substitution.
      - Presence/structure remain in surviving claims, observable_facts,
        and physical_loglik — not in the mechanism ranking.

    Returns (posterior_dict, mode) where mode is "PRIOR" if max|post-prior|<1e-9
    else "UPDATED".
    """
    quant = [s for s in streams if s.get("is_quantitative", 1) == 1]
    if not quant:
        post = {h: float(priors[h]) for h in HYPOTHESES}
        return post, "PRIOR"
    scaled = apply_reliability(quant, r)
    post = bayes_update(scaled, priors)
    # Continuous collapse: at low r, post ≈ prior
    if max(abs(post[h] - priors[h]) for h in HYPOTHESES) < 1e-9:
        return post, "PRIOR"
    return post, "UPDATED"


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
    print(_ascii("\n=== SURVIVING QUALITATIVE CLAIMS (reliability → 0) ==="))
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

    Mechanism ranking uses ONLY quantitative streams, matching
    `collapse_posterior` and `posterior_under_likelihood_uncertainty`.
    Non-quantitative streams are mechanism-silent at every r. Prior to this
    fix (audit finding #24), this path perturbed and multiplied all streams
    including non-quantitative ones, which reproduced the H5~=88%-at-r=0
    regression that `collapse_posterior` had already eliminated.
    Fully re-runnable by any agent with the same seed.
    """
    rng = random.Random(seed)
    samples = {h: [] for h in HYPOTHESES}

    # Mechanism ranking is quantitative-only across all three paths (audit #24).
    quant_streams = [s for s in streams if s.get("is_quantitative", 1) == 1]

    for _ in range(n_samples):
        r = r_center + rng.gauss(0, r_noise)
        r = max(0.0, min(1.0, r))
        # perturb quantitative streams only
        noisy = []
        for s in quant_streams:
            news = dict(s)
            for h in HYPOTHESES:
                L = s[h] + rng.gauss(0, lik_noise)
                L = max(0.01, min(0.99, L))
                if int(s.get("is_floor_quantitative", 0) or 0) == 1:
                    news[h] = L
                else:
                    news[h] = r * L + (1.0 - r) * _flat_target()
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
    print("Running self-tests (v5.6)...")
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
        if orig["is_quantitative"] == 1 and not int(orig.get("is_floor_quantitative", 0) or 0):
            for h in HYPOTHESES:
                if abs(scaled0[h] - 0.5) > 1e-9:
                    print(f"  [FAIL] reliability=0 should push admin quantitative to 0.5")
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
        print(_ascii(f"  [PASS] posterior sums to 1.0 (H5 ≈ {post['H5']:.1%})"))

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

    # Continuous collapse: quantitative-only update → prior at r=0 when no
    # floor-quant streams active; otherwise smoothly transitions with slope
    # governed by admin-quant contributions. We check for a *mathematical*
    # discontinuity (cliff at r=0.05) not the slope magnitude, which can be
    # large by design when floor-quant streams discriminate strongly.
    try:
        streams_st = load_streams()
        post0, mode0 = collapse_posterior(streams_st, RAW_PRIORS, 0.0)
        post_eps, _ = collapse_posterior(streams_st, RAW_PRIORS, 1e-4)
        post_below, _ = collapse_posterior(streams_st, RAW_PRIORS, 0.049)
        post_above, mode_hi = collapse_posterior(streams_st, RAW_PRIORS, 0.05)
        has_floor = any(int(s.get("is_floor_quantitative", 0) or 0) for s in streams_st)
        if not has_floor and max(abs(post0[h] - RAW_PRIORS[h]) for h in HYPOTHESES) > 1e-9:
            print(f"  [FAIL] r=0 post != prior (admin-only): {post0}")
            ok = False
        elif max(abs(post0[h] - post_eps[h]) for h in HYPOTHESES) > 1e-3:
            print(f"  [FAIL] mathematical discontinuity at r=0 (delta > 1e-3 for r=1e-4)")
            ok = False
        elif max(abs(post_below[h] - post_above[h]) for h in HYPOTHESES) > 1e-2:
            print(f"  [FAIL] cliff at r=0.05 threshold (delta > 0.01 between 0.049 and 0.050)")
            ok = False
        else:
            print(f"  [PASS] continuous collapse: r=0 mode={mode0} has_floor={has_floor}; no cliff at 0.05")
            print(f"         r=0 H5={post0['H5']:.4f}  r=0.05 mode={mode_hi} H5={post_above['H5']:.4f}")
            if has_floor:
                slope0 = max(abs(post0[h] - post_below[h]) for h in HYPOTHESES)
                print(_ascii(f"         floor-quant slope r=0→0.049: max |Δposterior| = {slope0:.4f} (informational)"))
    except Exception as e:
        print(f"  [FAIL] collapse_posterior self-test: {e}")
        ok = False

    # Path parity (audit #24): collapse / MC / BetaLU must agree, consume the
    # same quantitative-only stream set, and report bands containing their point
    # estimate. Shipped inside run_self_test so a fresh-clone reviewer learns
    # whether the paths agree without knowing CI exists.
    try:
        sys.path.insert(0, str(HERE.parent / "scripts"))
        try:
            from check_path_parity import (run_parity_check, run_interval_check,
                                           run_stream_set_check)
        except Exception as imp_err:
            print(f"  [INFO] path-parity checker unavailable: {imp_err}")
        else:
            streams_pp = load_streams()
            ok_p, max_div, _ = run_parity_check(streams_pp)
            ok_i, _ = run_interval_check(streams_pp)
            ok_s, quant, _ = run_stream_set_check(streams_pp)
            parity_ok = ok_p and ok_i and ok_s
            ok = ok and parity_ok
            label = "PASS" if parity_ok else "FAIL"
            print(f"  [{label}] path parity: max|path-collapse|={max_div:.4f} "
                  f"stream_set=quant({quant}) intervals={'ok' if ok_i else 'FAIL'}")
    except Exception as e:
        print(f"  [FAIL] path parity self-test: {e}")
        ok = False

    print("Self-test", "PASSED" if ok else "FAILED")
    return ok


def main():
    try:
        from __init__ import configure_utf8_console
        configure_utf8_console()
    except Exception:
        try:
            from model import configure_utf8_console
            configure_utf8_console()
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        description="TAST Bayesian Core v5.6 — reliability slider (0.0 = maximal skepticism)"
    )
    parser.add_argument("--reliability", type=float, default=1.0,
                        help="victors_reliability ∈ [0.0, 1.0] (default 1.0)")
    parser.add_argument("--streams", type=str, default=None,
                        help="Path to an alternative likelihood table CSV (default: evidence_streams.csv). "
                             "Missing file or missing columns raise StreamLoadError — no silent fallback.")
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
                        help="Group-mean shrink strength [0,1] (NOT effective-N; relabeled pending ESS fix)")
    parser.add_argument("--lik-uncertainty", type=int, default=0, metavar="N",
                        help="Monte Carlo N draws treating quant L as Beta means (0=off)")
    parser.add_argument("--kappa", type=float, default=10.0,
                        help="Beta concentration for likelihood uncertainty (default 10)")
    args = parser.parse_args()

    strict = not args.no_strict

    if args.self_test:
        sys.exit(0 if run_self_test() else 1)

    streams_path = Path(args.streams) if args.streams else STREAMS_CSV
    try:
        streams = load_streams(streams_path)
    except StreamLoadError as e:
        print(f"ERROR loading stream table {streams_path}: {e}", file=sys.stderr)
        print("No silent fallback to the default table (fail-closed).", file=sys.stderr)
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

    print(f"TAST Bayesian Core v5.6  |  victors_reliability = {r:.2f}  |  strict={strict}")
    try:
        import hashlib as _hl
        _cksum = _hl.sha256(streams_path.read_bytes()).hexdigest()[:16]
    except Exception:
        _cksum = "?"
    print(f"streams: {streams_path.name}  (sha256:{_cksum})  quant={sum(1 for s in streams if s['is_quantitative']==1)}/{len(streams)}")
    print("=" * 70)

    if r < 0.05:
        print("\n*** MAXIMAL SKEPTICISM MODE ***")
        print("Administrative head-counts, growth rates, and import totals")
        print("derived from owner/trader/enumerator records: UNDEFINED as estimands.")
        print("(Mechanism ranking can still exist; it is prior or floor-updated, not a national total.)")
        print("Physical and structural floor remains (see surviving/quantitative_floor.md).")
        print_surviving()
        post, mode = collapse_posterior(streams, RAW_PRIORS, r)
        if mode == "PRIOR":
            print(_ascii("\nMechanism posterior at r≈0: returns to PRIOR (no floor-quant active)"))
            print(">>> This is the PRIOR (RAW_PRIORS), displayed — not a data-fitted result.")
        else:
            print(_ascii("\nMechanism posterior at r≈0: UPDATED (floor-quantitative stream(s) active)"))
            print(">>> Differs from prior because is_floor_quantitative terms bypass the r-blend.")
        print(_ascii("(Administrative quant → flat at r=0; floor-quant preserved when present.)"))
        for h in HYPOTHESES:
            bar = _bar(post[h])
            print(_ascii(f"  {h}  {post[h]:6.1%}  {bar}"))
        try:
            try:
                from physical_likelihoods import physical_floor_report
            except ImportError:
                from model.physical_likelihoods import physical_floor_report
            rep = physical_floor_report({
                "lambda_growth": 0.015, "rho_reclass": 0.25,
                "r_owner": 0.0, "r_enumerator": 0.0, "undercount": 0.15,
            })
            print(_ascii(f"\nPhysical floor — observables that survive r->0 (PRIMARY):"))
            for ob in rep.get("observables", []):
                val = ob["value"]
                if isinstance(val, float):
                    val = f"{val:,.0f}"
                print(_ascii(f"  - {ob['name']}: {val}"))
                print(_ascii(f"      source: {ob['source']}"))
                print(_ascii(f"      role:   {ob['role']}"))
                if ob.get("in_bf"):
                    print(_ascii(f"      [enters the Bayes factor below]"))
                elif ob.get("not_in_bf_reason"):
                    print(_ascii(f"      [NOT in the BF — {ob['not_in_bf_reason']}]"))
            print(_ascii(f"\nPhysical floor — Bayes factor (SECONDARY; upper bound vs straw null):"))
            print(_ascii(f"  null: {rep['null_name']}"))
            print(_ascii(f"  log BF(floor | presence) vs (floor | null) = {rep['log_bayes_factor']:.2f}"))
            print(_ascii(f"  caveat: {rep.get('bf_caveat','')}"))
            print(_ascii(f"  (informative ll={rep['ll_informative']:.2f}; non-informative constants ll={rep['ll_noninformative']:.2f})"))
            for ex in rep["excluded"]:
                print(_ascii(f"  EXCLUDED: {ex['term']} ({ex['fact_id']} value:null) — {ex['reason']}"))
            for uo in rep.get("unused_observables", []):
                print(_ascii(f"  NOT WIRED: {uo['field']} = {uo['value']:.0f} ({uo['backing_fact']}) — {uo['reason']}"))
            print(_ascii("(The floor is mechanism-silent by construction; it does not rank H1-H5 at any r.)"))
        except Exception as e:
            print(f"\nPhysical-floor report unavailable: {e}")
        print(f"\n  {DISCLAIMER}")
        print("Meta-claim: No national-scale administrative total is a fact.")
        return


    # Quantitative path — must carry the strong disclaimer
    post, mode = collapse_posterior(streams, RAW_PRIORS, r)

    print("\n" + DISCLAIMER)
    print("-" * 70)
    print("Hypothesis posteriors (conditioned on reliability):")
    print("(Independence of streams is assumed — a known modeling limitation.)")
    for h in HYPOTHESES:
        bar = _bar(post[h])
        print(_ascii(f"  {h}  {post[h]:6.1%}  {bar}"))
        if args.verbose:
            print(_ascii(f"       {H_LABELS[h]}"))

    print("\nConditioning statement:")
    print(f'  "If we treat the recorded population totals as approximately accurate')
    print(_ascii(f'   (victors_reliability ≈ {r:.2f}), then the above posteriors obtain;'))
    print(f'   if we do not, the quantitative claims are undefined."')
    print(f"\n  {DISCLAIMER}")

    if getattr(args, "lik_uncertainty", 0) and args.lik_uncertainty > 0:
        samples_lu = posterior_under_likelihood_uncertainty(
            streams, RAW_PRIORS, r,
            n_samples=args.lik_uncertainty,
            kappa=getattr(args, "kappa", 10.0),
            seed=getattr(args, "seed", 42),
        )
        summarize_likelihood_uncertainty(samples_lu)

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
        print(_ascii("\n(Note: reliability < 0.5 → quantitative streams heavily diluted;"))
        print(" physical burial, aDNA-site, and meta-skepticism streams dominate.)")
        print_surviving()


if __name__ == "__main__":
    main()
