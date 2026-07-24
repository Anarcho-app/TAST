#!/usr/bin/env python3
"""
Stream 1 complete generative row — symmetric rigor (Opus 4.8 Max).

- No MLE plug-in for H1.
- No hand-picked r_af for H2; marginalize.
- H2a = absorption *instead of* NI (low r_af prior).
- H2b = absorption *in addition to* NI (same r prior as H1) + NA constraint.
- Table cell H2 defaults to H2b (matches definition: classification on American soil
  does not entail denying NI). H2a reported separately.
- H5 Ockham: σ/√(σ²+τ²).
- No silent clamp: raw values printed; table uses max(1e-6, L) only for log-stability.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class AdminInputs:
    n_1790: float = 697_681.0
    n_1860: float = 3_953_760.0
    imports: float = 140_000.0


SIGMA = 0.15
# Shared NI-rate prior (A) for H1 and H2b
MU_R, SD_R = 0.022, 0.004
# H2a: suppressed NI prior
MU_R_H2A, SD_R_H2A = 0.005, 0.005
N_SOURCE_DEFAULT = 800_000.0
NA_CEILING = 0.02  # charitable above Bryc ~0.008


def forward(n0: float, imports: float, r: float, years: float = 70.0) -> float:
    return n0 * math.exp(r * years) + imports * math.exp(r * (years / 2.0))


def kernel(obs: float, pred: float, sigma: float) -> float:
    if obs <= 0 or pred <= 0 or sigma <= 0:
        return 0.0
    z = (math.log(obs) - math.log(pred)) / sigma
    return math.exp(-0.5 * z * z)


def _grid_normal(mu: float, sd: float, n: int = 81) -> List[Tuple[float, float]]:
    rs = [mu + sd * (-4.0 + 8.0 * i / (n - 1)) for i in range(n)]
    ws = [math.exp(-0.5 * ((r - mu) / sd) ** 2) for r in rs]
    s = sum(ws)
    return list(zip(rs, [w / s for w in ws]))


def L_H1(sigma: float = SIGMA) -> float:
    inp = AdminInputs()
    acc = 0.0
    for r, w in _grid_normal(MU_R, SD_R):
        pred = forward(inp.n_1790, inp.imports, r)
        acc += w * kernel(inp.n_1860, pred, sigma)
    return acc


def L_H4(sigma: float = SIGMA) -> float:
    return L_H1(sigma)


def L_H5(sigma: float = SIGMA, tau: float = 0.85) -> float:
    return sigma / math.sqrt(sigma * sigma + tau * tau)


def L_H2a(sigma: float = SIGMA, n_source: float = N_SOURCE_DEFAULT) -> float:
    """Absorption *instead of* exceptional NI — low r_af prior, marginalize r and α."""
    inp = AdminInputs()
    alphas = [i / 20 for i in range(21)]
    aw = [(a + 1e-6) * ((1 - a) ** 5) for a in alphas]
    aw = [x / sum(aw) for x in aw]
    acc = 0.0
    for r, rw in _grid_normal(MU_R_H2A, SD_R_H2A):
        n_af = forward(inp.n_1790, inp.imports, r)
        for a, a_w in zip(alphas, aw):
            pred = n_af + a * n_source
            implied_na = (a * n_source / pred) if pred > 0 else 1.0
            k = kernel(inp.n_1860, pred, sigma)
            if implied_na > NA_CEILING:
                k *= math.exp(-((implied_na - NA_CEILING) / 0.05) ** 2)
            acc += rw * a_w * k
    return acc


def L_H2b(sigma: float = SIGMA, n_source: float = N_SOURCE_DEFAULT) -> float:
    """Absorption *in addition to* NI — same r prior as H1, marginalize r and α, NA constraint."""
    inp = AdminInputs()
    alphas = [i / 20 for i in range(21)]
    aw = [(a + 1e-6) * ((1 - a) ** 5) for a in alphas]
    aw = [x / sum(aw) for x in aw]
    acc = 0.0
    for r, rw in _grid_normal(MU_R, SD_R):
        n_af = forward(inp.n_1790, inp.imports, r)
        for a, a_w in zip(alphas, aw):
            pred = n_af + a * n_source
            implied_na = (a * n_source / pred) if pred > 0 else 1.0
            k = kernel(inp.n_1860, pred, sigma)
            if implied_na > NA_CEILING:
                k *= math.exp(-((implied_na - NA_CEILING) / 0.05) ** 2)
            acc += rw * a_w * k
    return acc


def L_H3(sigma: float = SIGMA, n_source: float = N_SOURCE_DEFAULT) -> float:
    """Mixture of H1 and H2b predictives (linearity of expectation)."""
    return 0.5 * L_H1(sigma) + 0.5 * L_H2b(sigma, n_source)


def complete_row(sigma: float = SIGMA, n_source: float = N_SOURCE_DEFAULT) -> Dict:
    h1 = L_H1(sigma)
    h2a = L_H2a(sigma, n_source)
    h2b = L_H2b(sigma, n_source)
    h3 = 0.5 * h1 + 0.5 * h2b
    h4 = h1
    h5 = L_H5(sigma)
    # Table uses H2b for H2 (definitional match). eps only for log product stability.
    eps = 1e-6
    return {
        "H1": max(eps, h1),
        "H2": max(eps, h2b),  # default cell = H2b
        "H2a_raw": h2a,
        "H2b_raw": h2b,
        "H3": max(eps, h3),
        "H4": max(eps, h4),
        "H5": max(eps, h5),
        "sigma": sigma,
        "n_source": n_source,
    }


if __name__ == "__main__":
    for pool in (800_000, 2_000_000):
        row = complete_row(n_source=pool)
        print(f"pool={pool:,.0f}")
        print(
            f"  H1={row['H1']:.4f}  H2b={row['H2b_raw']:.4f}  H2a={row['H2a_raw']:.4e}  "
            f"H3={row['H3']:.4f}  H4={row['H4']:.4f}  H5={row['H5']:.4f}"
        )
        print(f"  ratio H1/H2b = {row['H1']/row['H2b_raw']:.3f}")
    print("\nNo clamp. H2 table cell = H2b (NI + absorption + NA). H2a reported separately.")
