#!/usr/bin/env python3
"""
TAST Inference Extensions (v4.8)

Lean implementations of the remaining open items:
  1. Formal functional dependence N = f(C_t, I, r)
  2. Multi-axis reliability vector
  3. Minimal correlation damping by stream group
  4. Claim-level view using c_i
  5. Skeleton generative bias model
  6. External-validation / adversarial hooks

All functions are pure / stdlib+numpy and fully re-runnable.
They deliberately stay simple (Einstein constraint). Full hierarchical
MCMC (NumPyro/PyMC) remains future work; this module provides the
transparent bridge.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLAIMS_CI_CSV = ROOT / "data" / "sources_registry_with_ci.csv"

HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]


def N_of(C: Dict[int, float], I: float, r: float) -> Optional[float]:
    """N = f(C_1790..C_1860, I, r). Returns None (UNDEFINED) when r -> 0."""
    if r < 0.05:
        return None
    years = sorted(C.keys())
    if not years:
        return None
    C_T = C[years[-1]]
    baseline = I * 4.0  # placeholder scale; not a factual claim
    return r * C_T + (1.0 - r) * baseline


def demonstrate_functional_dependence() -> None:
    print("Formal dependence:")
    print("  N = f(C_1790, ..., C_1860, I, r)")
    print("  When r -> 0, N is UNDEFINED (administrative path collapses).")
    print()
    C = {1790: 697897, 1810: 1191418, 1830: 2009030, 1860: 3953760}
    I = 389000
    for r in [1.0, 0.7, 0.3, 0.0]:
        n = N_of(C, I, r)
        status = "UNDEFINED" if n is None else f"{n:,.0f}"
        print(f"  r={r:.1f}  ->  N ~ {status}")
    print()
    print("CONDITIONAL ESTIMATE derived from biased administrative records")
    print("(victors' paperwork). This is NOT A FACT.")


def multi_axis_to_scalar(owner: float, enumerator: float, coverage: float,
                         weights: Tuple[float, float, float] = (0.4, 0.4, 0.2)) -> float:
    w = np.array(weights, dtype=float)
    w = w / w.sum()
    v = np.clip([owner, enumerator, coverage], 0.0, 1.0)
    return float(w @ v)


def demonstrate_multi_axis() -> None:
    print("Multi-axis reliability examples -> scalar r:")
    cases = [
        (1.0, 1.0, 1.0, "full trust"),
        (0.5, 0.5, 0.8, "moderate skepticism"),
        (0.1, 0.2, 0.5, "strong skepticism"),
        (0.0, 0.0, 0.0, "maximal skepticism"),
    ]
    for o, e, c, label in cases:
        r = multi_axis_to_scalar(o, e, c)
        print(f"  owner={o:.1f}  enum={e:.1f}  cov={c:.1f}  ->  r={r:.2f}  ({label})")


def damp_correlated_streams(streams: List[Dict], strength: float = 0.5) -> List[Dict]:
    """Group-level damping as transparent proxy for residual correlation."""
    groups = defaultdict(list)
    for i, s in enumerate(streams):
        groups[s.get("group", "")].append(i)
    out = [dict(s) for s in streams]
    for g, idxs in groups.items():
        if len(idxs) < 2:
            continue
        for h in HYPOTHESES:
            vals = [streams[i][h] for i in idxs]
            mean = sum(vals) / len(vals)
            for i in idxs:
                orig = streams[i][h]
                out[i][h] = (1.0 - strength) * orig + strength * mean
    return out


def load_claims_with_ci(path: Path = CLAIMS_CI_CSV) -> List[Dict]:
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


def claim_level_summary(min_ci: float = 0.70) -> None:
    claims = load_claims_with_ci()
    if not claims:
        print("No claim confidence file found.")
        return
    high = [c for c in claims if c["confidence_ci"] >= min_ci]
    low = [c for c in claims if c["confidence_ci"] < 0.30]
    print(f"Claim-level view (c_i threshold = {min_ci:.2f}):")
    print(f"  Total claims: {len(claims)}")
    print(f"  High-confidence (c_i >= {min_ci:.2f}): {len(high)}")
    print(f"  Low-confidence  (c_i < 0.30): {len(low)}")
    print("  High-c_i claims enriched for physical/archaeological sources;")
    print("  low-c_i claims enriched for pure enumerator/owner head-counts.")


def bias_model_observed(true_count: float, theta_owner: float,
                        theta_enumerator: float, r: float,
                        rng: Optional[np.random.Generator] = None) -> float:
    """Minimal generative sketch: observed ~ BiasModel(true, theta_owner, theta_enum, r)."""
    if rng is None:
        rng = np.random.default_rng(0)
    bias = (1.0 - r) * (0.6 * theta_owner + 0.4 * theta_enumerator)
    coverage = 0.7 + 0.3 * r
    noise = rng.normal(0, 0.05 * (1.0 - r + 0.1))
    return max(0.0, true_count * (1.0 + bias) * coverage * (1.0 + noise))


def demonstrate_bias_model() -> None:
    print("Skeleton generative bias model (illustrative only):")
    print("  observed ~ BiasModel(true, theta_owner, theta_enumerator, r)")
    true = 100000.0
    rng = np.random.default_rng(42)
    for r in [1.0, 0.5, 0.1]:
        obs = [bias_model_observed(true, 0.3, 0.2, r, rng) for _ in range(5)]
        mean_obs = sum(obs) / len(obs)
        print(f"  r={r:.1f}  true={true:,.0f}  mean_observed~{mean_obs:,.0f}")
    print("  (Replace this body with a fitted hierarchical model when ready.)")


ADVERSARIAL_CHECKLIST = """
External validation / adversarial re-analysis hooks
----------------------------------------------------
1. Re-derive every c_i from the published rule set.
2. Re-run Monte Carlo:  python bayesian_core.py --monte-carlo 500 --seed <n>
3. Set reliability=0 and confirm only the quantitative floor + Stream 27 remain.
4. Supply alternative likelihood tables or multi-axis weights.
5. Challenge N = f(C_t, I, r) by replacing the body of N_of().
6. Publish any alternative generative BiasModel and compare against the physical floor.

Invitation: adversarial re-analysis is expected and welcome.
"""


def print_adversarial_hooks() -> None:
    print(ADVERSARIAL_CHECKLIST)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TAST inference extensions (v4.8)")
    parser.add_argument("--demo-functional", action="store_true")
    parser.add_argument("--demo-multiaxis", action="store_true")
    parser.add_argument("--demo-bias", action="store_true")
    parser.add_argument("--claims", action="store_true")
    parser.add_argument("--min-ci", type=float, default=0.70)
    parser.add_argument("--adversarial", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all or args.demo_functional:
        demonstrate_functional_dependence()
        print()
    if args.all or args.demo_multiaxis:
        demonstrate_multi_axis()
        print()
    if args.all or args.demo_bias:
        demonstrate_bias_model()
        print()
    if args.all or args.claims:
        claim_level_summary(args.min_ci)
        print()
    if args.all or args.adversarial:
        print_adversarial_hooks()


if __name__ == "__main__":
    main()
