#!/usr/bin/env python3
"""
TAST Physical-Floor Likelihoods (v5.0-alpha)

First data-level likelihood terms that remain fully active when
victors_reliability → 0. These are the quantities that can actually
constrain inference after the administrative path collapses.

Series currently encoded
------------------------
1. Burial / aDNA site presence and sample sizes
2. Genealogical termination pattern (structural coverage)
3. Erasure / structural silence index
4. Regime intensity (legal + spatial)

Each term returns a log-likelihood contribution under a simple
generative story. The stories are deliberately minimal and inspectable.
They are not yet fitted hierarchical models; they are the first
replacement for purely hand-assigned point likelihoods on the
physical floor.

Einstein constraint: small, transparent, re-runnable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Observed physical / structural data (primary-linked, lower-bound style)
# ---------------------------------------------------------------------------
# These are deliberately conservative summaries of the primary sources
# already inventoried in raw/ and the quantitative floor. They are not
# national population totals.

@dataclass
class PhysicalObservations:
    # Number of major documented burial grounds with African / mixed ancestry remains
    n_burial_sites: int = 8
    # Approximate total individuals recovered / estimated across key sites
    # (African Burial Ground estimate is itself a range; we use a lower-bound
    # order-of-magnitude for the likelihood illustration)
    n_individuals_lower: float = 15000.0
    # Number of published aDNA individuals from U.S. historical contexts
    # (Catoctin, Anson, Chesapeake, etc.)
    n_adna_individuals: int = 80
    # Genealogical termination: fraction of documented FBA-style lineages
    # that terminate in U.S. records (structural, not a head-count)
    termin_in_us_frac: float = 0.85
    # Erasure index proxy: log-ratio of owner/enumerator quantitative volume
    # vs. pre-1865 enslaved quantitative testimony (high = strong asymmetry)
    erasure_log_ratio: float = 4.5  # ~90:1 illustrative order
    # Number of distinct colonies/states with anti-literacy or racial-integrity
    # statutes that shaped the record environment
    n_regime_jurisdictions: int = 12


OBS = PhysicalObservations()


# ---------------------------------------------------------------------------
# Simple generative likelihoods (log space)
# ---------------------------------------------------------------------------

def loglik_burial_sites(n_sites_expected: float, obs: PhysicalObservations = OBS) -> float:
    """
    Poisson-style lower-bound on number of distinct burial sites.
    Supports multi-generational presence without needing a national total.
    """
    lam = max(n_sites_expected, 0.5)
    k = obs.n_burial_sites
    # log Poisson(k | lam)
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def loglik_adna_sample(rate: float, obs: PhysicalObservations = OBS) -> float:
    """
    Poisson on published aDNA individuals. Rate is expected recoverable
    sample size under a given presence / research-intensity model.
    """
    lam = max(rate, 0.5)
    k = obs.n_adna_individuals
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def loglik_genealogical_termination(p_term: float, obs: PhysicalObservations = OBS) -> float:
    """
    Bernoulli / binomial style on the observed fraction of documented
    lineages that terminate in U.S. records. High p_term supports
    multi-generational American rootedness as a structural pattern.
    """
    p = float(np.clip(p_term, 1e-3, 1.0 - 1e-3))
    # treat observed fraction as if arising from a large effective sample
    n_eff = 200.0
    k = obs.termin_in_us_frac * n_eff
    return k * math.log(p) + (n_eff - k) * math.log(1.0 - p)


def loglik_erasure(asymmetry: float, obs: PhysicalObservations = OBS) -> float:
    """
    The observed high log-ratio of owner/enumerator quantitative material
    vs. enslaved quantitative testimony is treated as positive evidence of
    structural silence. Higher modeled asymmetry fits the observed index.
    """
    # Normal on the log-ratio
    mu = asymmetry
    sigma = 1.2
    x = obs.erasure_log_ratio
    return -0.5 * math.log(2 * math.pi * sigma**2) - 0.5 * ((x - mu) / sigma) ** 2


def loglik_regime_intensity(n_expected: float, obs: PhysicalObservations = OBS) -> float:
    """Poisson on number of jurisdictions with documented coercive record regimes."""
    lam = max(n_expected, 0.5)
    k = obs.n_regime_jurisdictions
    return k * math.log(lam) - lam - math.lgamma(k + 1)


# ---------------------------------------------------------------------------
# Parameter → likelihood mapping (continuous parameters from hierarchical skeleton)
# ---------------------------------------------------------------------------

def physical_loglik(params: Dict[str, float], obs: PhysicalObservations = OBS) -> float:
    """
    Total log-likelihood from the physical / structural floor.

    params expected keys (subset of hierarchical continuous parameters):
      lambda_growth, rho_reclass, undercount, r_owner, r_enumerator, ...
    Mapping is deliberately simple and inspectable.
    """
    # Presence intensity drives expected burial sites and aDNA recovery
    # Higher multi-generational presence → more sites / more recoverable remains
    presence = 1.0 / (1.0 + math.exp(-20.0 * (params.get("lambda_growth", 0.01) - 0.005)))
    n_sites_exp = 3.0 + 10.0 * presence
    adna_rate = 20.0 + 120.0 * presence

    # Termination probability rises with American-soil continuity
    # and falls with pure recent-arrival narratives
    p_term = 0.55 + 0.40 * (1.0 - params.get("rho_reclass", 0.3))
    p_term = float(np.clip(p_term, 0.05, 0.95))

    # Erasure asymmetry is higher when owner/enumerator reliability is
    # low relative to the existence of a coercive regime
    r_rec = 0.5 * (params.get("r_owner", 0.5) + params.get("r_enumerator", 0.5))
    asymmetry = 2.0 + 4.0 * (1.0 - r_rec)

    # Regime intensity
    n_reg = 6.0 + 10.0 * (1.0 - r_rec)

    ll = 0.0
    ll += loglik_burial_sites(n_sites_exp, obs)
    ll += loglik_adna_sample(adna_rate, obs)
    ll += loglik_genealogical_termination(p_term, obs)
    ll += loglik_erasure(asymmetry, obs)
    ll += loglik_regime_intensity(n_reg, obs)
    return ll


def demonstrate_physical_likelihoods(seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    print("Physical-floor log-likelihood under different continuous parameter draws")
    print("=" * 60)
    print(f"{'presence':>10} {'p_term':>8} {'asym':>8} {'loglik':>10}")
    for _ in range(6):
        params = {
            "lambda_growth": float(rng.normal(0.015, 0.015)),
            "rho_reclass": float(rng.beta(2, 5)),
            "r_owner": float(rng.beta(2, 2)),
            "r_enumerator": float(rng.beta(2, 2)),
            "undercount": float(rng.beta(2, 8)),
        }
        ll = physical_loglik(params)
        presence = 1.0 / (1.0 + math.exp(-20.0 * (params["lambda_growth"] - 0.005)))
        p_term = 0.55 + 0.40 * (1.0 - params["rho_reclass"])
        r_rec = 0.5 * (params["r_owner"] + params["r_enumerator"])
        asym = 2.0 + 4.0 * (1.0 - r_rec)
        print(f"{presence:10.3f} {p_term:8.3f} {asym:8.3f} {ll:10.2f}")
    print()
    print("These terms remain fully active at reliability → 0.")
    print("They do not depend on administrative head-counts.")
    print("CONDITIONAL estimates grounded in physical / structural primaries.")
    print("They are still NOT facts — but they are the floor that survives skepticism.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TAST physical-floor likelihoods v5.0-alpha")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    demonstrate_physical_likelihoods(seed=args.seed)


if __name__ == "__main__":
    main()
