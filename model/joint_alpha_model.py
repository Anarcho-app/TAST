#!/usr/bin/env python3
"""
Joint absorption-fraction model (Path A).

Estimand: posterior on α = fraction of the 1860 enslaved population
attributable to absorption/reclassification — NOT a five-way H1–H5 horse race.

Shared latents
  r_us      annual NI rate, US-like class
  r_carib   annual NI rate, sugar-colony class
  alpha     absorption fraction of 1860 stock (the estimand)
  log_sigma census log-error
  n_pool    absorbable source-pool size (prior; charitable default)

Observables (conditioned on the same latents; likelihood evaluated once)
  O1  US 1790→1860 terminal count under NI + residual imports + absorption
  O2  Post-trade closed-window growth gap US vs British Caribbean
  O3  Autosomal NA ancestry ceiling (Bryc-class ~0.8%; soft upper ~2%)

Product-of-stream architecture is intentionally NOT used here.
Streams 1, 2, 31 become observables in one joint likelihood.

All count inputs remain CONDITIONAL administrative/voyage series.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# ── Conditional admin anchors (not facts) ──────────────────────────────────
N_US_1790 = 697_681.0
N_US_1810 = 1_191_362.0
N_US_1860 = 3_953_760.0
IMPORTS_POST_1790 = 140_000.0
N_CARIB_1807 = 775_000.0
N_CARIB_1834 = 665_000.0
YEARS_1790_1860 = 70.0
YEARS_1810_1860 = 50.0
YEARS_CARIB = 27.0
BRYC_NA_MEAN = 0.008  # Bryc et al. order
NA_SOFT_CEILING = 0.02  # charitable


@dataclass
class Latents:
    r_us: float
    r_carib: float
    alpha: float
    log_sigma: float
    n_pool: float


@dataclass
class PriorSpec:
    # r_us ~ N(0.022, 0.004)  US vital-rate class (Stream 1 prior A)
    r_us_mu: float = 0.022
    r_us_sd: float = 0.004
    # r_carib ~ N(-0.008, 0.010) sugar-colony class
    r_carib_mu: float = -0.008
    r_carib_sd: float = 0.010
    # alpha ~ Beta(1, 20)  — skeptical of large absorption a priori (mean ~0.048)
    alpha_a: float = 1.0
    alpha_b: float = 20.0
    # log_sigma ~ LogNormal-ish clamped; default center 0.15
    log_sigma_mu: float = 0.15
    log_sigma_sd: float = 0.05
    # n_pool log-uniform-ish around charitable 800k
    n_pool_mu_log: float = math.log(800_000.0)
    n_pool_sd_log: float = 0.5


def _forward_us(r: float, alpha: float, n_pool: float) -> float:
    """Predicted 1860 stock: NI path on 1790 + residual imports + absorption."""
    stock = N_US_1790 * math.exp(r * YEARS_1790_1860)
    imports = IMPORTS_POST_1790 * math.exp(r * (YEARS_1790_1860 / 2.0))
    african_path = stock + imports
    # alpha is fraction of terminal attributable to absorption
    # terminal ≈ african_path / (1 - alpha)  if absorption added on top
    if alpha >= 0.95:
        return 1e12
    return african_path / (1.0 - alpha)


def _growth(n0: float, n1: float, years: float) -> float:
    return math.log(max(n1, 1.0) / max(n0, 1.0)) / years


def _loglik_normal(obs: float, pred: float, sd: float) -> float:
    if sd <= 1e-12:
        return -1e12
    z = (obs - pred) / sd
    return -0.5 * z * z - math.log(sd) - 0.5 * math.log(2 * math.pi)


def log_prior(theta: Latents, prior: PriorSpec) -> float:
    lp = 0.0
    # Normal priors on rates
    for x, mu, sd in (
        (theta.r_us, prior.r_us_mu, prior.r_us_sd),
        (theta.r_carib, prior.r_carib_mu, prior.r_carib_sd),
        (theta.log_sigma, prior.log_sigma_mu, prior.log_sigma_sd),
    ):
        z = (x - mu) / sd
        lp += -0.5 * z * z - math.log(sd)
    # Beta prior on alpha via log
    a, b = prior.alpha_a, prior.alpha_b
    if not (0.0 < theta.alpha < 1.0):
        return -1e12
    lp += (a - 1) * math.log(theta.alpha) + (b - 1) * math.log(1 - theta.alpha)
    # log-normal on pool
    log_n = math.log(max(theta.n_pool, 1.0))
    z = (log_n - prior.n_pool_mu_log) / prior.n_pool_sd_log
    lp += -0.5 * z * z - math.log(prior.n_pool_sd_log) - log_n
    return lp


def log_likelihood(theta: Latents) -> float:
    """Joint loglik of all observables given shared latents."""
    ll = 0.0
    sig = max(theta.log_sigma, 0.02)

    # O1: US 1860 count (log space)
    pred_1860 = _forward_us(theta.r_us, theta.alpha, theta.n_pool)
    ll += _loglik_normal(math.log(N_US_1860), math.log(max(pred_1860, 1.0)), sig)

    # O2: post-trade growth gap
    g_us = _growth(N_US_1810, N_US_1860, YEARS_1810_1860)
    g_carib = _growth(N_CARIB_1807, N_CARIB_1834, YEARS_CARIB)
    obs_gap = g_us - g_carib
    # Predicted gap ≈ r_us - r_carib, with small absorption adjustment on US side
    # Absorption inflates apparent growth; adjust predicted US rate upward by ~alpha effect
    # Approximate: extra growth from alpha over 50y ≈ -log(1-alpha)/50
    extra = -math.log(max(1.0 - theta.alpha, 1e-6)) / YEARS_1810_1860
    pred_gap = (theta.r_us + extra) - theta.r_carib
    # σ_gap from census error on four endpoints
    sig_gap = math.sqrt(
        2 * sig * sig / (YEARS_1810_1860 ** 2) + 2 * sig * sig / (YEARS_CARIB ** 2)
    )
    ll += _loglik_normal(obs_gap, pred_gap, max(sig_gap, 1e-4))

    # O3: NA ancestry — implied NA ≈ alpha * (pool contribution share)
    # Simple: if alpha of terminal is absorbed Indigenous-associated, modern NA
    # under dilution still tracks alpha order of magnitude for soft constraint.
    implied_na = theta.alpha  # upper-bound style: alpha cannot much exceed NA ceiling
    # Soft hinge: likelihood drops when alpha >> NA_SOFT_CEILING
    if implied_na > NA_SOFT_CEILING:
        excess = (implied_na - NA_SOFT_CEILING) / 0.02
        ll += -0.5 * excess * excess
    # Also mild preference near Bryc mean only if alpha is the sole source of NA
    # (weak — do not force alpha = 0.008)
    ll += _loglik_normal(implied_na, BRYC_NA_MEAN, 0.05) * 0.15  # weak weight

    return ll


def log_posterior(theta: Latents, prior: PriorSpec) -> float:
    return log_prior(theta, prior) + log_likelihood(theta)


def sample_prior(prior: PriorSpec, rng: random.Random) -> Latents:
    def nrm(mu, sd):
        return mu + sd * rng.gauss(0, 1)

    # Beta via gamma ratio
    def beta(a, b):
        x = rng.gammavariate(a, 1)
        y = rng.gammavariate(b, 1)
        return x / (x + y)

    return Latents(
        r_us=nrm(prior.r_us_mu, prior.r_us_sd),
        r_carib=nrm(prior.r_carib_mu, prior.r_carib_sd),
        alpha=beta(prior.alpha_a, prior.alpha_b),
        log_sigma=max(0.05, nrm(prior.log_sigma_mu, prior.log_sigma_sd)),
        n_pool=math.exp(nrm(prior.n_pool_mu_log, prior.n_pool_sd_log)),
    )


def mh_sample(
    n_samples: int = 4000,
    burn: int = 1000,
    thin: int = 2,
    seed: int = 42,
    prior: PriorSpec | None = None,
) -> List[Latents]:
    """Random-walk Metropolis on latents; returns posterior draws."""
    prior = prior or PriorSpec()
    rng = random.Random(seed)
    theta = sample_prior(prior, rng)
    lp = log_posterior(theta, prior)
    draws: List[Latents] = []
    # proposal scales
    scales = dict(r_us=0.002, r_carib=0.004, alpha=0.02, log_sigma=0.02, n_pool_log=0.3)
    accepted = 0
    total = n_samples + burn
    for i in range(total):
        prop = Latents(
            r_us=theta.r_us + scales["r_us"] * rng.gauss(0, 1),
            r_carib=theta.r_carib + scales["r_carib"] * rng.gauss(0, 1),
            alpha=min(0.99, max(1e-4, theta.alpha + scales["alpha"] * rng.gauss(0, 1))),
            log_sigma=max(0.04, theta.log_sigma + scales["log_sigma"] * rng.gauss(0, 1)),
            n_pool=math.exp(math.log(theta.n_pool) + scales["n_pool_log"] * rng.gauss(0, 1)),
        )
        lp_prop = log_posterior(prop, prior)
        if math.log(rng.random()) < lp_prop - lp:
            theta, lp = prop, lp_prop
            accepted += 1
        if i >= burn and (i - burn) % thin == 0:
            draws.append(theta)
    return draws


def summarize_alpha(draws: List[Latents]) -> Dict[str, float]:
    alphas = sorted(d.alpha for d in draws)
    n = len(alphas)
    def q(p):
        return alphas[min(n - 1, int(p * n))]
    return {
        "n_draws": float(n),
        "mean": sum(alphas) / n,
        "median": q(0.50),
        "p05": q(0.05),
        "p25": q(0.25),
        "p75": q(0.75),
        "p95": q(0.95),
        "p99": q(0.99),
    }


def main():
    print("Joint α model — absorption fraction of 1860 population")
    print("Latents: r_us, r_carib, alpha, log_sigma, n_pool")
    print("Observables: O1 US counts | O2 post-trade gap | O3 NA ceiling")
    print()
    draws = mh_sample(n_samples=6000, burn=1500, thin=3, seed=42)
    s = summarize_alpha(draws)
    print(f"Posterior α  (n={int(s['n_draws'])} draws)")
    print(f"  mean   {s['mean']:.4f}")
    print(f"  median {s['median']:.4f}")
    print(f"  90% CI [{s['p05']:.4f}, {s['p95']:.4f}]")
    print(f"  50% CI [{s['p25']:.4f}, {s['p75']:.4f}]")
    print(f"  p99    {s['p99']:.4f}")
    print()
    print("Reading: α is the fraction of 1860 stock attributed to absorption.")
    print("Physical/genomic ceiling and growth observables bound α near low values")
    print("under the stated priors — without a five-way categorical product.")
    # also report r_us marginal
    rus = sorted(d.r_us for d in draws)
    n = len(rus)
    print(f"Marginal r_us median {rus[n//2]*100:.2f}%/yr  "
          f"90% CI [{rus[int(0.05*n)]*100:.2f}, {rus[int(0.95*n)]*100:.2f}]")


if __name__ == "__main__":
    main()
