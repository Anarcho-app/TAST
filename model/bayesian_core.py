#!/usr/bin/env python3
"""
TAST Bayesian Core — Skepticism-First Edition (v4.3)

Single parameter: victors_reliability ∈ [0.0, 1.0]
  1.0 = treat census / manifest / ledger counts as approximately accurate
  0.0 = maximal skepticism: all quantitative head-counts become UNDEFINED;
        only qualitative / physical / meta patterns survive.

Core epistemic rule (v4.3):
  Estimates calculated from the administrative records are CONDITIONAL
  ESTIMATES derived from biased sources (victors' paperwork).
  They are NEVER facts. Language that converts them into facts
  ("least-bad", "best available", "robust after correction", etc.)
  is forbidden under --strict (default on).

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
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STREAMS_CSV = HERE / "evidence_streams.csv"
SURVIVING_MD = ROOT / "surviving" / "qualitative_claims.md"

HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]
H_LABELS = {
    "H1": "Pure Conventional (African origin + exceptional fertility)",
    "H2": "Classification / Indigenous absorption dominant",
    "H3": "Hybrid (partial absorption + moderate advantage)",
    "H4": "U.S.-Specific Conditions (natural increase via structure)",
    "H5": "Mixed / Undocumented Mechanisms (honest uncertainty)",
}

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
]

DISCLAIMER = (
    "CONDITIONAL ESTIMATE derived from biased administrative records "
    "(victors' paperwork). This is NOT A FACT."
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


def run_self_test() -> bool:
    print("Running self-tests (v4.3)...")
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

    # New v4.3 checks
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

    print("Self-test", "PASSED" if ok else "FAILED")
    return ok


def main():
    parser = argparse.ArgumentParser(
        description="TAST Bayesian Core v4.3 — reliability slider (0.0 = maximal skepticism)"
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
    args = parser.parse_args()

    strict = not args.no_strict

    if args.self_test:
        sys.exit(0 if run_self_test() else 1)

    try:
        streams = load_streams()
    except StreamLoadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    r = max(0.0, min(1.0, args.reliability))

    if args.list_streams:
        print(f"{'ID':>3}  {'Q':>1}  {'Group':>5}  Name")
        for s in streams:
            q = "Q" if s["is_quantitative"] else " "
            print(f"{s['stream_id']:3d}  {q}  {s['group']:>5}  {s['name']}")
        return

    print(f"TAST Bayesian Core v4.3  |  victors_reliability = {r:.2f}  |  strict={strict}")
    print("=" * 70)

    if r < 0.05:
        print("\n*** MAXIMAL SKEPTICISM MODE ***")
        print("All quantitative head-counts, growth rates, and import totals")
        print("are treated as UNDEFINED / UNKNOWABLE.")
        print("Only qualitative / physical / meta patterns remain.")
        print_surviving()
        print("Posterior over mechanisms: UNDEFINABLE (no reliable likelihoods).")
        print("Deep American roots (qualitative): SUPPORTED by physical + genealogical patterns.")
        print("\nMeta-claim: No national-scale population total derived from the")
        print("administrative records constitutes a fact.")
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
