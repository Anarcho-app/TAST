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
try:
    from bayesian_core import (
        load_streams,
        apply_reliability,
        bayes_update,
        collapse_posterior,
        RAW_PRIORS,
        HYPOTHESES,
        DISCLAIMER,
    )
except ImportError:
    from model.bayesian_core import (
        load_streams,
        apply_reliability,
        bayes_update,
        collapse_posterior,
        RAW_PRIORS,
        HYPOTHESES,
        DISCLAIMER,
    )

try:
    from physical_likelihoods import physical_loglik
except ImportError:
    try:
        from model.physical_likelihoods import physical_loglik
    except ImportError:
        physical_loglik = None


def run_at_r(streams, r: float) -> Dict:
    """Single evaluation at a fixed reliability — uses shared collapse_posterior."""
    post, mode = collapse_posterior(streams, RAW_PRIORS, r)
    pll = None
    if physical_loglik is not None:
        params = {
            "lambda_growth": 0.015,
            "rho_reclass": 0.25,
            "r_owner": max(r, 0.0),
            "r_enumerator": max(r, 0.0),
            "undercount": 0.15,
        }
        try:
            pll = physical_loglik(params)
        except Exception:
            pll = None

    if mode == "PRIOR" or r < 0.05:
        return {
            "r": r,
            "admin_path": "UNDEFINED",
            "posteriors": post,
            "physical_ll": pll,
            "note": (
                "Admin totals UNDEFINED. Mechanism posterior = PRIOR "
                "(floor excluded from H1–H5 by construction)."
            ),
        }
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
    print("TAST Continuous Sensitivity Map (v5.1)")
    print("=" * 78)
    print("Continuous collapse: as r→0, admin quant L→0.5 (flat); posterior → RAW_PRIORS")
    print("plus is_floor_quantitative offsets. Helper-equivalence claim RETRACTED at r=1.")
    print("As r → 0, administrative path → UNDEFINED; physical/genomic floor remains.")
    print()
    print(f"{'r':>6}  {'Admin path':<22}  {'H1':>7}  {'H2':>7}  {'H3':>7}  {'H4':>7}  {'H5':>7}  {'Phys LL':>9}")
    print("-" * 78)
    for res in results:
        r = res["r"]
        admin = res["admin_path"]
        if res["posteriors"] is None:
            h1 = h2 = h3 = h4 = h5 = "   —"
        else:
            h1 = f"{res['posteriors']['H1']:6.1%}"
            h2 = f"{res['posteriors']['H2']:6.1%}"
            h3 = f"{res['posteriors']['H3']:6.1%}"
            h4 = f"{res['posteriors']['H4']:6.1%}"
            h5 = f"{res['posteriors']['H5']:6.1%}"
        pll = f"{res['physical_ll']:9.1f}" if res["physical_ll"] is not None else "        —"
        print(f"{r:6.2f}  {admin:<22}  {h1:>7}  {h2:>7}  {h3:>7}  {h4:>7}  {h5:>7}  {pll}")
    print()
    print("Interpretation:")
    print("  r = 1.00  →  admin path DEFINED (conditional); not claimed equal to mainstream H1 posteriors")
    print("  r → 0.00  →  admin UNDEFINED; mechanism posterior = RAW_PRIORS + floor-quant offset")
    print("             (Stream 30 NYABG isotope, Stream 31 autosomal ancestry ceiling)")
    print("             The floor-quant offset is the physical/genomic evidence that survives")
    print("             zero-weight on the administrative series. See stream30/31 .md files.")
    print("             Without floor-quant streams, r=0 = RAW_PRIORS exactly (no discrimination).")
    print()
    print(DISCLAIMER)
    print("Physical-floor terms do not depend on administrative head-counts.")


def main():
    try:
        from __init__ import configure_utf8_console
    except Exception:
        from model import configure_utf8_console
    configure_utf8_console()
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
