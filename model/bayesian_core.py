#!/usr/bin/env python3
"""
TAST Bayesian Core — Skepticism-First Edition (v4.0)

Single parameter: victors_reliability ∈ [0.0, 1.0]
  1.0 = treat census / manifest / ledger counts as approximately accurate
  0.0 = maximal skepticism: all quantitative head-counts become undefined;
        only qualitative / physical / meta patterns survive.

Usage:
  python -m bayesian_core --reliability 0.0
  python -m bayesian_core --reliability 1.0 --verbose
  python -m bayesian_core --list-streams
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
STREAMS_CSV = HERE / "evidence_streams.csv"

# ---------------------------------------------------------------------------
# Hypotheses (fixed labels)
# ---------------------------------------------------------------------------
HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]
H_LABELS = {
    "H1": "Pure Conventional (African origin + exceptional fertility)",
    "H2": "Classification / Indigenous absorption dominant",
    "H3": "Hybrid (partial absorption + moderate advantage)",
    "H4": "U.S.-Specific Conditions (natural increase via structure)",
    "H5": "Mixed / Undocumented Mechanisms (honest uncertainty)",
}

# Normalized priors (from v2.6.3 / v3.0)
RAW_PRIORS = {
    "H1": 0.0727,
    "H2": 0.1364,
    "H3": 0.1818,
    "H4": 0.1818,
    "H5": 0.4273,
}

# ---------------------------------------------------------------------------
# Load streams
# ---------------------------------------------------------------------------
def load_streams() -> List[Dict]:
    streams = []
    with open(STREAMS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["stream_id"] = int(row["stream_id"])
            for h in HYPOTHESES:
                row[h] = float(row[h])
            row["is_quantitative"] = int(row.get("is_quantitative", 1))
            streams.append(row)
    return streams


# ---------------------------------------------------------------------------
# Core update with reliability scaling
# ---------------------------------------------------------------------------
def apply_reliability(
    streams: List[Dict],
    reliability: float,
) -> List[Dict]:
    """
    Scale likelihoods of quantitative streams toward 0.5 (non-informative)
    as reliability → 0.0. Qualitative / physical / meta streams keep full weight.
    """
    scaled = []
    for s in streams:
        news = s.copy()
        if s["is_quantitative"] == 1:
            # Linear interpolation: at r=1 keep original L; at r=0 push to 0.5
            for h in HYPOTHESES:
                L = s[h]
                news[h] = reliability * L + (1.0 - reliability) * 0.5
        # else: leave unchanged (physical, meta, genetic-method, etc.)
        scaled.append(news)
    return scaled


def bayes_update(
    streams: List[Dict],
    priors: Dict[str, float],
) -> Dict[str, float]:
    """Simple independent product of likelihoods (log-space for stability)."""
    log_post = {h: math.log(priors[h] + 1e-30) for h in HYPOTHESES}
    for s in streams:
        for h in HYPOTHESES:
            L = max(s[h], 1e-12)  # floor
            log_post[h] += math.log(L)
    # normalize
    max_log = max(log_post.values())
    unnorm = {h: math.exp(log_post[h] - max_log) for h in HYPOTHESES}
    total = sum(unnorm.values())
    return {h: unnorm[h] / total for h in HYPOTHESES}


# ---------------------------------------------------------------------------
# Qualitative survivors (hard-coded from surviving/ layer)
# ---------------------------------------------------------------------------
SURVIVING_CLAIMS = [
    "People of African and mixed descent were present on the territory that became the United States for multiple generations prior to 1865.",
    "Physical burial grounds and archaeological sites document multi-generational presence of these populations on American soil.",
    "Genealogical chains for the large majority of documented Black American lineages terminate in U.S. records (church, county, plantation, Freedmen’s Bureau).",
    "Forced labor regimes, family separation practices, and legal non-personhood existed and left documentary and physical traces.",
    "Racial classification on U.S. censuses and vital records was enumerator-driven (“lookerism”) rather than self-reported for most of the period.",
    "Comparable Caribbean and Brazilian slave societies showed net natural decrease and required continuous imports; the U.S. pattern (if the counts are taken at face value) is an outlier.",
    "Ancient DNA sampling of historical populations remains <0.0001 % of humans who ever lived and cannot by itself ground origin narratives.",
    "The majority of quantifiable demographic records were produced by owners, traders, or colonial administrators; systematic pre-1865 testimony from the enslaved population is essentially absent (~2,300 WPA interviews from ~0.02 % of the formerly enslaved).",
]


def print_surviving():
    print("\n=== SURVIVING QUALITATIVE CLAIMS (reliability → 0) ===")
    for i, c in enumerate(SURVIVING_CLAIMS, 1):
        print(f"  {i}. {c}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="TAST Bayesian Core — reliability slider (0.0 = maximal skepticism)"
    )
    parser.add_argument(
        "--reliability",
        type=float,
        default=1.0,
        help="victors_reliability ∈ [0.0, 1.0]  (default 1.0)",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--list-streams", action="store_true")
    args = parser.parse_args()

    r = max(0.0, min(1.0, args.reliability))
    streams = load_streams()

    if args.list_streams:
        print(f"{'ID':>3}  {'Q':>1}  {'Group':>5}  Name")
        for s in streams:
            q = "Q" if s["is_quantitative"] else " "
            print(f"{s['stream_id']:3d}  {q}  {s['group']:>5}  {s['name']}")
        return

    print(f"TAST Bayesian Core v4.0  |  victors_reliability = {r:.2f}")
    print("=" * 60)

    if r < 0.05:
        print("\n*** MAXIMAL SKEPTICISM MODE ***")
        print("All quantitative head-counts, growth rates, and import totals")
        print("are treated as UNDEFINED / UNKNOWABLE.")
        print("Only qualitative / physical / meta patterns remain.")
        print_surviving()
        print("Posterior over mechanisms: UNDEFINABLE (no reliable likelihoods).")
        print("Deep American roots (qualitative): SUPPORTED by physical + genealogical patterns.")
        return

    scaled = apply_reliability(streams, r)
    post = bayes_update(scaled, RAW_PRIORS)

    print("\nHypothesis posteriors (conditioned on reliability):")
    for h in HYPOTHESES:
        bar = "█" * int(post[h] * 40)
        print(f"  {h}  {post[h]:6.1%}  {bar}")
        if args.verbose:
            print(f"       {H_LABELS[h]}")

    print("\nConditioning statement:")
    print(f'  "If we treat the recorded population totals as approximately accurate')
    print(f'   (victors_reliability ≈ {r:.2f}), then the above posteriors obtain;')
    print(f'   if we do not, the quantitative claims are undefined."')

    if r < 0.5:
        print("\n(Note: reliability < 0.5 → quantitative streams heavily diluted;")
        print(" physical burial, aDNA-site, and meta-skepticism streams dominate.)")
        print_surviving()


if __name__ == "__main__":
    main()
