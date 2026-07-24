#!/usr/bin/env python3
"""
Stream 1 generative likelihood — documented arrivals + natural increase.

Computes P(observed terminal counts | H1-style demographic path) with an
explicit error model. Inputs are CONDITIONAL administrative quantities
(census schedules, voyage estimates) — the same class Hacker/cliometric
literature models. They are NOT facts under TAST's epistemic rule.

At r=1 this is the mainstream computation made transparent.
At r→0 this stream is diluted like other admin quant streams.

Credit for prioritization: Claude Opus 4.8 (Stream 1 sole remaining move).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class AdminInputs:
    """Conditional admin inputs — labeled, not asserted as facts."""
    n_1790: float = 697_681.0          # U.S. Census 1790 enslaved (published schedule total)
    n_1860: float = 3_953_760.0        # U.S. Census 1860 enslaved (published schedule total)
    imports_pre_1790: float = 300_000.0  # order-of-magnitude mainland disembarkations to 1790 (SlaveVoyages-class totals; wide uncertainty)
    imports_1790_1808: float = 90_000.0  # residual legal trade window (order-of-magnitude)
    imports_post_1808: float = 50_000.0  # illegal/smuggling upper-ish order (highly uncertain; literature ranges widely)
    note: str = (
        "All count inputs are published administrative/voyage-estimate series. "
        "TAST treats them as conditional under victors_reliability, not as facts."
    )


@dataclass
class H1Params:
    """Natural-increase path under documented arrivals + U.S. conditions."""
    # Effective annual growth of the enslaved population 1790–1860 under NI-dominant account.
    # Observed admin growth is roughly (3953760/697681)^(1/70) - 1 ≈ 2.5%/yr.
    # H1 says this is achievable via NI + modest residual imports.
    r_ni_annual: float = 0.025
    # Observation error: lognormal σ on terminal count (multiplicative).
    # σ=0.15 ≈ factor-of-1.16 uncertainty — wide enough to be non-dogmatic.
    log_sigma: float = 0.15


def forward_H1(inp: AdminInputs, p: H1Params) -> float:
    """Predict 1860 count from 1790 stock + residual imports + NI.

    Crude two-block model:
      - Grow 1790 stock for 70 years at r_ni
      - Add post-1790 imports grown for half-period on average (midpoint approximation)
    """
    years = 70.0
    stock = inp.n_1790 * math.exp(p.r_ni_annual * years)
    residual_imports = inp.imports_1790_1808 + inp.imports_post_1808
    # midpoint growth for residual imports
    imports_contrib = residual_imports * math.exp(p.r_ni_annual * (years / 2.0))
    return stock + imports_contrib


def loglik_terminal(observed: float, predicted: float, log_sigma: float) -> float:
    """Normal likelihood on log counts."""
    if observed <= 0 or predicted <= 0 or log_sigma <= 0:
        return -1e9
    z = (math.log(observed) - math.log(predicted)) / log_sigma
    return -0.5 * z * z - math.log(log_sigma) - 0.5 * math.log(2 * math.pi)


def likelihood_H1(inp: AdminInputs | None = None, p: H1Params | None = None) -> Dict:
    """Return predicted count, loglik, and a [0,1]-mapped likelihood for Stream 1."""
    inp = inp or AdminInputs()
    p = p or H1Params()
    pred = forward_H1(inp, p)
    ll = loglik_terminal(inp.n_1860, pred, p.log_sigma)
    # Map loglik to (0,1) for the table via logistic on standardized residual.
    # residual in log space:
    resid = abs(math.log(inp.n_1860) - math.log(pred)) / p.log_sigma
    # L = exp(-0.5 * resid^2) is the kernel without the constant; in (0,1]
    L_kernel = math.exp(-0.5 * resid * resid)
    return {
        "n_1790": inp.n_1790,
        "n_1860_obs": inp.n_1860,
        "n_1860_pred": pred,
        "ratio_obs_pred": inp.n_1860 / pred,
        "loglik": ll,
        "L_H1_kernel": L_kernel,
        "r_ni_annual": p.r_ni_annual,
        "log_sigma": p.log_sigma,
        "inputs_note": inp.note,
    }


def likelihood_table_row(
    inp: AdminInputs | None = None,
    p: H1Params | None = None,
) -> Dict[str, float]:
    """Propose Stream 1 likelihoods under a generative H1 path.

    H1: high if observed terminal is near NI+arrivals prediction.
    H2: classification/absorption does not by itself predict this growth path —
        mild/neutral.
    H5: residual — moderate (model could be wrong in several ways).
    """
    res = likelihood_H1(inp, p)
    L_h1 = float(res["L_H1_kernel"])
    # Floor/ceiling for table stability
    L_h1 = max(0.05, min(0.95, L_h1))
    return {
        "H1": round(L_h1, 4),
        "H2": 0.40,  # growth path not the natural prediction of pure reclassification
        "H3": 0.55,
        "H4": round(max(0.05, min(0.95, L_h1 * 0.95)), 4),  # H4 is NI-via-local-regime; similar
        "H5": 0.50,
        "meta": res,
    }


if __name__ == "__main__":
    row = likelihood_table_row()
    meta = row.pop("meta")
    print("Stream 1 generative proposal")
    print(f"  1790 admin N = {meta['n_1790']:,.0f}")
    print(f"  1860 admin N obs = {meta['n_1860_obs']:,.0f}")
    print(f"  1860 admin N pred (H1 NI+arrivals) = {meta['n_1860_pred']:,.0f}")
    print(f"  obs/pred = {meta['ratio_obs_pred']:.3f}")
    print(f"  L_H1 kernel = {meta['L_H1_kernel']:.4f}")
    print(f"  proposed table row: H1={row['H1']} H2={row['H2']} H3={row['H3']} H4={row['H4']} H5={row['H5']}")
    print(f"  note: {meta['inputs_note']}")
