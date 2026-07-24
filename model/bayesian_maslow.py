#!/usr/bin/env python3
"""
Bayesian Maslow metric (lean) — v5.0 companion module

Purpose
-------
Game-theoretic / behavioral layer for historical agents and regimes.
Need-states are latent; physical and structural observables (shared with
the TAST floor) update posteriors over which needs were binding.

This module does NOT feed demographic head-counts. It answers a different
question: given the same physical/structural evidence, what constraints
and payoffs were likely in play?

Levels (simplified, ordered)
----------------------------
  L1  physiological / survival
  L2  safety / security / control
  L3  belonging / kin / community
  L4  esteem / status / legitimacy
  L5  autonomy / self-direction / actualization

Evidence types (tied to TAST floor observables)
-----------------------------------------------
  burial_investment, family_separation, anti_literacy, flight_resistance,
  market_accumulation, record_silence, regime_statutes, ...

Monte Carlo
-----------
  - Draws over evidence reliability and likelihood noise
  - Returns posterior mean + quantiles over need levels
  - Same discipline: conditional estimates, not facts

Einstein constraint: small state space, transparent update, shared floor.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import numpy as np

LEVELS = ["L1_survival", "L2_safety", "L3_belonging", "L4_esteem", "L5_autonomy"]

# Default weakly informative prior (slightly higher mass on safety/survival
# for coercive historical regimes; still diffuse)
DEFAULT_PRIOR = np.array([0.22, 0.28, 0.20, 0.18, 0.12])

# Evidence → likelihood multipliers per level (hand-specified but inspectable;
# replace with data-level terms as floor densifies)
# Rows = evidence keys; cols = L1..L5. Higher = more consistent with that level binding.
EVIDENCE_LIK = {
    # Physical presence / burial investment → survival + belonging + some esteem
    "burial_presence":      np.array([0.85, 0.70, 0.80, 0.55, 0.40]),
    # Anti-literacy / record control → safety/control for regime; blocks autonomy
    "anti_literacy":        np.array([0.50, 0.90, 0.45, 0.60, 0.25]),
    # Family separation practices → safety/control weaponized; hits belonging
    "family_separation":    np.array([0.55, 0.88, 0.30, 0.50, 0.35]),
    # Structural silence / erasure of enslaved quantitative voice
    "record_silence":       np.array([0.45, 0.85, 0.40, 0.55, 0.30]),
    # Genealogical termination in U.S. records → belonging + multi-gen continuity
    "genealogical_us":      np.array([0.60, 0.65, 0.90, 0.50, 0.55]),
    # Market / accumulation strategies (traders, planters)
    "market_accumulation":  np.array([0.40, 0.70, 0.45, 0.85, 0.50]),
    # Flight / resistance (when attested) → survival + autonomy
    "flight_resistance":    np.array([0.80, 0.75, 0.55, 0.45, 0.85]),
}


def normalize(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return v / s if s > 0 else np.ones_like(v) / len(v)


def update_posterior(
    prior: np.ndarray,
    evidence_keys: List[str],
    evidence_weights: Optional[Dict[str, float]] = None,
) -> np.ndarray:
    """
    Simple independent likelihood product over evidence keys.
    evidence_weights in [0,1] can down-weight noisy or low-confidence items
    (ties to facts YAML confidence).
    """
    log_post = np.log(prior + 1e-12)
    weights = evidence_weights or {}
    for key in evidence_keys:
        if key not in EVIDENCE_LIK:
            continue
        w = float(np.clip(weights.get(key, 1.0), 0.0, 1.0))
        lik = EVIDENCE_LIK[key] ** w  # weight as power → w=0 leaves uniform influence
        log_post = log_post + np.log(lik + 1e-12)
    return normalize(np.exp(log_post - log_post.max()))


def monte_carlo_maslow(
    evidence_keys: List[str],
    evidence_weights: Optional[Dict[str, float]] = None,
    n_samples: int = 400,
    weight_noise: float = 0.08,
    prior: Optional[np.ndarray] = None,
    seed: int = 42,
) -> Dict:
    """
    Monte Carlo over evidence weights (noise around reported confidence/weight)
    and slight prior noise. Returns mean posterior and quantiles per level.
    """
    rng = np.random.default_rng(seed)
    prior = prior if prior is not None else DEFAULT_PRIOR.copy()
    weights = dict(evidence_weights or {k: 1.0 for k in evidence_keys})

    samples = []
    for _ in range(n_samples):
        # noisy weights
        w_noisy = {
            k: float(np.clip(weights.get(k, 1.0) + rng.normal(0, weight_noise), 0.05, 1.0))
            for k in evidence_keys
        }
        # slight prior jitter
        p = prior * np.exp(rng.normal(0, 0.05, size=len(prior)))
        p = normalize(p)
        post = update_posterior(p, evidence_keys, w_noisy)
        samples.append(post)

    arr = np.stack(samples, axis=0)  # (n, 5)
    summary = {}
    for i, name in enumerate(LEVELS):
        col = arr[:, i]
        summary[name] = {
            "mean": float(col.mean()),
            "q05": float(np.quantile(col, 0.05)),
            "q50": float(np.quantile(col, 0.50)),
            "q95": float(np.quantile(col, 0.95)),
        }
    return {
        "n_samples": n_samples,
        "evidence": evidence_keys,
        "levels": summary,
        "note": (
            "CONDITIONAL behavioral/strategic estimate. "
            "Not a demographic total. Not a fact. "
            "Shares physical/structural observables with the TAST floor."
        ),
    }


def print_maslow(result: Dict) -> None:
    print("Bayesian Maslow (lean) — posterior over binding need levels")
    print("=" * 60)
    print(f"Evidence: {', '.join(result['evidence'])}")
    print(f"Samples: {result['n_samples']}")
    print()
    print(f"{'Level':<16} {'5%':>8} {'50%':>8} {'95%':>8} {'mean':>8}")
    for name in LEVELS:
        s = result["levels"][name]
        print(f"{name:<16} {s['q05']:8.1%} {s['q50']:8.1%} {s['q95']:8.1%} {s['mean']:8.1%}")
    print()
    print(result["note"])


def demo_regime_vs_enslaved(seed: int = 42) -> None:
    """Two illustrative agent-frames using the same floor-linked evidence."""
    print("\n--- Frame: coercive regime / owners-traders ---")
    reg = monte_carlo_maslow(
        evidence_keys=["anti_literacy", "family_separation", "record_silence", "market_accumulation"],
        evidence_weights={
            "anti_literacy": 0.92,
            "family_separation": 0.88,
            "record_silence": 0.90,
            "market_accumulation": 0.75,
        },
        seed=seed,
    )
    print_maslow(reg)

    print("\n--- Frame: multi-generational bound population ---")
    bound = monte_carlo_maslow(
        evidence_keys=["burial_presence", "genealogical_us", "flight_resistance", "family_separation"],
        evidence_weights={
            "burial_presence": 0.95,
            "genealogical_us": 0.88,
            "flight_resistance": 0.70,
            "family_separation": 0.85,
        },
        seed=seed + 1,
    )
    print_maslow(bound)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bayesian Maslow lean module")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--samples", type=int, default=400)
    args = parser.parse_args()
    if args.demo:
        demo_regime_vs_enslaved(seed=args.seed)


if __name__ == "__main__":
    main()
