#!/usr/bin/env python3
"""Stream 2 — post-trade growth gap. H2=H2b; Bryc-derived delta (not 0.85 fudge)."""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict

@dataclass
class ClosedWindow:
    us_1810: float = 1_191_362.0
    us_1860: float = 3_953_760.0
    years_us: float = 50.0
    carib_1807: float = 775_000.0
    carib_1834: float = 665_000.0
    years_carib: float = 27.0
    log_sigma_census: float = 0.15

def growth(n0, n1, years):
    return math.log(n1 / n0) / years

def sigma_growth(years, log_sigma):
    return math.sqrt(2.0) * log_sigma / years

def expected_kernel_gap(obs, mu, tau, sigma):
    se = math.sqrt(sigma * sigma + tau * tau)
    return math.exp(-0.5 * ((obs - mu) / se) ** 2) * (sigma / se)

def complete_row() -> Dict:
    w = ClosedWindow()
    g_us = growth(w.us_1810, w.us_1860, w.years_us)
    g_carib = growth(w.carib_1807, w.carib_1834, w.years_carib)
    obs_gap = g_us - g_carib
    sigma_gap = math.sqrt(
        sigma_growth(w.years_us, w.log_sigma_census)**2
        + sigma_growth(w.years_carib, w.log_sigma_census)**2
    )
    mu_us, sd_us = 0.022, 0.004
    mu_sugar, sd_sugar = -0.008, 0.010
    mu_h1 = mu_us - mu_sugar
    tau_h1 = math.sqrt(sd_us**2 + sd_sugar**2)
    mu_h2a, tau_h2a = 0.0, 0.015
    # Bryc α≤2% over 50y → delta_g ≈ -log(1-0.02)/50 ≈ 0.000404
    bryc_delta = -math.log(1 - 0.02) / 50.0
    mu_h2b = mu_h1 - bryc_delta
    tau_h2b = tau_h1 * 1.05
    mu_h5, tau_h5 = 0.015, 0.04
    L_h1 = expected_kernel_gap(obs_gap, mu_h1, tau_h1, sigma_gap)
    L_h2a = expected_kernel_gap(obs_gap, mu_h2a, tau_h2a, sigma_gap)
    L_h2b = expected_kernel_gap(obs_gap, mu_h2b, tau_h2b, sigma_gap)
    L_h4 = L_h1
    L_h3 = 0.5 * L_h1 + 0.5 * L_h2b
    L_h5 = expected_kernel_gap(obs_gap, mu_h5, tau_h5, sigma_gap)
    eps = 1e-6
    return {
        "H1": max(eps, L_h1), "H2": max(eps, L_h2b), "H3": max(eps, L_h3),
        "H4": max(eps, L_h4), "H5": max(eps, L_h5),
        "meta": {
            "obs_gap_pp": obs_gap*100, "sigma_gap_pp": sigma_gap*100,
            "mu_h1_pp": mu_h1*100, "mu_h2b_pp": mu_h2b*100,
            "bryc_delta_pp": bryc_delta*100, "L_h2a": L_h2a, "L_h2b": L_h2b,
        },
    }

if __name__ == "__main__":
    row = complete_row(); m = row["meta"]
    print(f"H1={row['H1']:.4f} H2b={m['L_h2b']:.4f} H2a={m['L_h2a']:.4f} H3={row['H3']:.4f} H5={row['H5']:.4f}")
    print(f"H1/H2b={row['H1']/m['L_h2b']:.2f}  bryc_delta={m['bryc_delta_pp']:.3f} pp")
