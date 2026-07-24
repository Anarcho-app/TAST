#!/usr/bin/env python3
"""
TAST Continuous Sensitivity Map (v5.0)

Demonstrates that mainstream ("Helper") point-estimate reconstructions
are a special case of TAST at victors_reliability r ≈ 1.0.

As r moves from 1.0 → 0.0:
  - Administrative quantitative path remains defined only while r is high
  - At low r the administrative path becomes UNDEFINED
  - Physical/structural floor likelihoods remain active throughout

This is the minimal bridge: one continuous curve, not a competing national total.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List

import numpy as np

# Reuse core pieces
from bayesian_core import (
    load_streams,
    apply_reliability,
    bayes_update,
    RAW_PRIORS,
    HYPOTHESES,
    DISCLAIMER,
)

try:
    from physical_likelihoods import physical_loglik
except ImportError:
    physical_loglik = None


def run_at_r(streams, r: float) -> Dict:
    """Single evaluation at a fixed reliability."""
    if r < 0.05:
        return {
            "r": r,
            "admin_path": "UNDEFINED",
            "posteriors": None,
            "physical_ll": None,
            "note": "Administrative head-counts / growth rates / imports UNDEFINED. Physical floor only.",
        }

    scaled = apply_reliability(streams, r)
    post = bayes_update(scaled, RAW_PRIORS)

    pll = None
    if physical_loglik is not None:
        # illustrative continuous params consistent with moderate presence
        params = {
            "lambda_growth": 0.015,
            "rho_reclass": 0.25,
            "r_owner": r,
            "r_enumerator": r,
            "undercount": 0.15,
        }
        try:
            pll = physical_loglik(params)
        except Exception:
            pll = None

    return {
        "r": r,
        "admin_path": "DEFINED (conditional)",
        "posteriors": post,
        "physical_ll": pll,
        "note": DISCLAIMER,
    }


def sensitivity_sweep(
    r_values: List[float] | None = None,
    streams=None,
) -> List[Dict]:
    if streams is None:
        streams = load_streams()
    if r_values is None:
        r_values = [1.0, 0.9, 0.7, 0.5, 0.3, 0.1, 0.0]
    return [run_at_r(streams, r) for r in r_values]


def print_sensitivity_table(results: List[Dict]) -> None:
    print("TAST Continuous Sensitivity Map (v5.0)")
    print("=" * 72)
    print("Mainstream ('Helper') point estimates ≈ special case at r = 1.0")
    print("As r → 0, administrative path → UNDEFINED; physical floor remains.")
    print()
    print(f"{'r':>6}  {'Admin path':<22}  {'H5':>8}  {'H3':>8}  {'Phys LL':>10}")
    print("-" * 72)
    for res in results:
        r = res["r"]
        admin = res["admin_path"]
        if res["posteriors"] is None:
            h5 = h3 = "  —"
        else:
            h5 = f"{res['posteriors']['H5']:7.1%}"
            h3 = f"{res['posteriors']['H3']:7.1%}"
        pll = f"{res['physical_ll']:10.1f}" if res["physical_ll"] is not None else "       —"
        print(f"{r:6.2f}  {admin:<22}  {h5:>8}  {h3:>8}  {pll}")
    print()
    print("Interpretation:")
    print("  r = 1.00  →  closest to mainstream baseline (Helper as boundary case)")
    print("  r → 0.00  →  administrative totals UNDEFINED; only physical/structural floor speaks")
    print()
    print(DISCLAIMER)
    print("Physical-floor terms do not depend on administrative head-counts.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TAST sensitivity map v5.0")
    parser.add_argument(
        "--r",
        type=float,
        nargs="*",
        default=None,
        help="Custom reliability values to evaluate (default: 1.0 0.9 0.7 0.5 0.3 0.1 0.0)",
    )
    args = parser.parse_args()
    results = sensitivity_sweep(r_values=args.r)
    print_sensitivity_table(results)


if __name__ == "__main__":
    main()
