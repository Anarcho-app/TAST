#!/usr/bin/env python3
"""

# DNA LIMITS (do not remove):
# BRYC_NA_MEAN is a cohort admixture summary (n~5e3 order), NOT a measurement
# on ~40M+ people. K-cluster components are model output, not racial ontology.
# O3 constrains alpha_I only; never identify with alpha_admin (lookerism).
# See dna_sample_size_discipline.md and model/DNA_LIMITS.md.

Joint model with split estimands (Opus 4.8 High identification diagnostics).

α_I     = Indigenous-associated ancestry retained in modern self-ID AA cohort
          Identified by O3 (genomic). Robust ~0.8%.

α_admin = administrative absorption/reclassification share of 1860 category stock
          NOT identified by O3. Lookerism ≠ genome.
          identity: modern_NA_signal ≈ α_admin · f_I · d
          O3 constrains only that product (= α_I), never α_admin by identity.

Race on schedules is lookerism, not genomic reality.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


N_US_1790 = 697_681.0
N_US_1810 = 1_191_362.0
N_US_1860 = 3_953_760.0
IMPORTS_POST_1790 = 140_000.0
N_CARIB_1807 = 775_000.0
N_CARIB_1834 = 665_000.0
YEARS_1790_1860 = 70.0
YEARS_1810_1860 = 50.0
YEARS_CARIB = 27.0
BRYC_NA_MEAN = 0.008
# SE of mean at n≈5269 is tiny (~0.0003); use slightly wider for cohort/model error
BRYC_NA_SD = 0.002


@dataclass
class Latents:
    r_us: float
    r_carib: float
    alpha_admin: float
    f_I: float          # Indigenous share of absorbed pool
    d: float            # retention into modern self-ID cohort
    log_sigma: float
    n_pool: float

    @property
    def alpha_I(self) -> float:
        """Genomically constrained product — the identified quantity."""
        return self.alpha_admin * self.f_I * self.d


@dataclass
class PriorSpec:
    r_us_mu: float = 0.022
    r_us_sd: float = 0.004
    r_carib_mu: float = -0.008
    r_carib_sd: float = 0.010
    # α_admin: default mildly skeptical; sweep in diagnostics
    alpha_a: float = 1.0
    alpha_b: float = 20.0
    # f_I, d: vague by default (honest ignorance)
    f_I_a: float = 1.0
    f_I_b: float = 1.0
    d_a: float = 1.0
    d_b: float = 1.0
    log_sigma_mu: float = 0.15
    log_sigma_sd: float = 0.05
    n_pool_mu_log: float = math.log(800_000.0)
    n_pool_sd_log: float = 0.5


def _forward_us(r: float, alpha_admin: float) -> float:
    stock = N_US_1790 * math.exp(r * YEARS_1790_1860)
    imports = IMPORTS_POST_1790 * math.exp(r * (YEARS_1790_1860 / 2.0))
    african_path = stock + imports
    if alpha_admin >= 0.95:
        return 1e12
    return african_path / (1.0 - alpha_admin)


def _growth(n0: float, n1: float, years: float) -> float:
    return math.log(max(n1, 1.0) / max(n0, 1.0)) / years


def _ll_norm(obs: float, pred: float, sd: float) -> float:
    if sd <= 1e-12:
        return -1e12
    z = (obs - pred) / sd
    return -0.5 * z * z - math.log(sd) - 0.5 * math.log(2 * math.pi)


def log_prior(th: Latents, p: PriorSpec) -> float:
    lp = 0.0
    for x, mu, sd in (
        (th.r_us, p.r_us_mu, p.r_us_sd),
        (th.r_carib, p.r_carib_mu, p.r_carib_sd),
        (th.log_sigma, p.log_sigma_mu, p.log_sigma_sd),
    ):
        z = (x - mu) / sd
        lp += -0.5 * z * z - math.log(sd)
    def beta_lp(x, a, b):
        if not (0.0 < x < 1.0):
            return -1e12
        return (a - 1) * math.log(x) + (b - 1) * math.log(1 - x)
    lp += beta_lp(th.alpha_admin, p.alpha_a, p.alpha_b)
    lp += beta_lp(th.f_I, p.f_I_a, p.f_I_b)
    lp += beta_lp(th.d, p.d_a, p.d_b)
    log_n = math.log(max(th.n_pool, 1.0))
    z = (log_n - p.n_pool_mu_log) / p.n_pool_sd_log
    lp += -0.5 * z * z - math.log(p.n_pool_sd_log) - log_n
    return lp


def log_likelihood(
    th: Latents,
    use_o1: bool = True,
    use_o2: bool = True,
    use_o3: bool = True,
) -> float:
    ll = 0.0
    sig = max(th.log_sigma, 0.02)
    if use_o1:
        pred = _forward_us(th.r_us, th.alpha_admin)
        ll += _ll_norm(math.log(N_US_1860), math.log(max(pred, 1.0)), sig)
    if use_o2:
        g_us = _growth(N_US_1810, N_US_1860, YEARS_1810_1860)
        g_carib = _growth(N_CARIB_1807, N_CARIB_1834, YEARS_CARIB)
        obs_gap = g_us - g_carib
        extra = -math.log(max(1.0 - th.alpha_admin, 1e-6)) / YEARS_1810_1860
        pred_gap = (th.r_us + extra) - th.r_carib
        sig_gap = math.sqrt(
            2 * sig * sig / (YEARS_1810_1860 ** 2)
            + 2 * sig * sig / (YEARS_CARIB ** 2)
        )
        ll += _ll_norm(obs_gap, pred_gap, max(sig_gap, 1e-4))
    if use_o3:
        # O3 constrains α_I = α_admin · f_I · d  — NOT α_admin
        implied = th.alpha_I
        ll += _ll_norm(implied, BRYC_NA_MEAN, BRYC_NA_SD)
    return ll


def log_posterior(th: Latents, p: PriorSpec, **obs_flags) -> float:
    return log_prior(th, p) + log_likelihood(th, **obs_flags)


def _beta(rng: random.Random, a: float, b: float) -> float:
    x = rng.gammavariate(max(a, 1e-3), 1)
    y = rng.gammavariate(max(b, 1e-3), 1)
    return x / (x + y)


def sample_prior(p: PriorSpec, rng: random.Random) -> Latents:
    def nrm(mu, sd):
        return mu + sd * rng.gauss(0, 1)
    return Latents(
        r_us=nrm(p.r_us_mu, p.r_us_sd),
        r_carib=nrm(p.r_carib_mu, p.r_carib_sd),
        alpha_admin=_beta(rng, p.alpha_a, p.alpha_b),
        f_I=_beta(rng, p.f_I_a, p.f_I_b),
        d=_beta(rng, p.d_a, p.d_b),
        log_sigma=max(0.05, nrm(p.log_sigma_mu, p.log_sigma_sd)),
        n_pool=math.exp(nrm(p.n_pool_mu_log, p.n_pool_sd_log)),
    )


def mh_sample(
    n_samples: int = 5000,
    burn: int = 1500,
    thin: int = 3,
    seed: int = 42,
    prior: Optional[PriorSpec] = None,
    use_o1: bool = True,
    use_o2: bool = True,
    use_o3: bool = True,
) -> List[Latents]:
    p = prior or PriorSpec()
    rng = random.Random(seed)
    th = sample_prior(p, rng)
    flags = dict(use_o1=use_o1, use_o2=use_o2, use_o3=use_o3)
    lp = log_posterior(th, p, **flags)
    draws: List[Latents] = []
    for i in range(n_samples + burn):
        prop = Latents(
            r_us=th.r_us + 0.002 * rng.gauss(0, 1),
            r_carib=th.r_carib + 0.004 * rng.gauss(0, 1),
            alpha_admin=min(0.99, max(1e-4, th.alpha_admin + 0.03 * rng.gauss(0, 1))),
            f_I=min(0.99, max(1e-4, th.f_I + 0.05 * rng.gauss(0, 1))),
            d=min(0.99, max(1e-4, th.d + 0.05 * rng.gauss(0, 1))),
            log_sigma=max(0.04, th.log_sigma + 0.02 * rng.gauss(0, 1)),
            n_pool=math.exp(math.log(th.n_pool) + 0.3 * rng.gauss(0, 1)),
        )
        lp_p = log_posterior(prop, p, **flags)
        if math.log(rng.random()) < lp_p - lp:
            th, lp = prop, lp_p
        if i >= burn and (i - burn) % thin == 0:
            draws.append(th)
    return draws


def summarize(draws: List[Latents], attr: str = "alpha_I") -> Dict[str, float]:
    xs = sorted(getattr(d, attr) if attr != "alpha_I" else d.alpha_I for d in draws)
    n = len(xs)
    def q(p):
        return xs[min(n - 1, int(p * n))]
    return {
        "n": float(n),
        "mean": sum(xs) / n,
        "median": q(0.50),
        "p05": q(0.05),
        "p95": q(0.95),
        "p99": q(0.99),
    }


def diagnostics(seed: int = 42) -> None:
    print("=== Observable ablation (α_admin, prior Beta(1,20), f_I/d vague) ===")
    p = PriorSpec()
    for name, o1, o2, o3 in (
        ("prior only", False, False, False),
        ("O1+O2", True, True, False),
        ("full O1+O2+O3", True, True, True),
    ):
        draws = mh_sample(4000, 1000, 2, seed, p, o1, o2, o3)
        sa = summarize(draws, "alpha_admin")
        si = summarize(draws, "alpha_I")
        print(
            f"  {name:<16} α_admin med={sa['median']:.4f} p99={sa['p99']:.4f}  |  "
            f"α_I med={si['median']:.4f} p99={si['p99']:.4f}"
        )
    print()
    print("=== α_admin under honest f_I/d (full model) ===")
    scenarios = [
        ("f_I,d vague (uniform)", PriorSpec()),
        ("f_I~Beta(1,3), d~Beta(2,2)", PriorSpec(f_I_a=1, f_I_b=3, d_a=2, d_b=2)),
        ("old identity f_I≈1,d≈1", PriorSpec(f_I_a=50, f_I_b=1.01, d_a=50, d_b=1.01)),
    ]
    for name, pr in scenarios:
        draws = mh_sample(4000, 1000, 2, seed, pr, True, True, True)
        sa = summarize(draws, "alpha_admin")
        si = summarize(draws, "alpha_I")
        print(
            f"  {name:<32} α_admin med={sa['median']:.4f} p95={sa['p95']:.4f} p99={sa['p99']:.4f}  |  "
            f"α_I med={si['median']:.4f}"
        )
    print()
    print("Claim: publish α_I (~0.8%). Do NOT claim α_admin is genomically bounded.")


def main():
    print("Joint model — split α_admin vs α_I")
    print("O3 constrains α_I = α_admin · f_I · d  only\n")
    diagnostics()
    print()
    draws = mh_sample(6000, 1500, 3, 42, PriorSpec())
    si = summarize(draws, "alpha_I")
    sa = summarize(draws, "alpha_admin")
    print("Default vague f_I,d — reportable:")
    print(f"  α_I     median {si['median']:.4f}  90%CI [{si['p05']:.4f}, {si['p95']:.4f}]  p99 {si['p99']:.4f}")
    print(f"  α_admin median {sa['median']:.4f}  90%CI [{sa['p05']:.4f}, {sa['p95']:.4f}]  p99 {sa['p99']:.4f}  (NOT identified by O3)")


if __name__ == "__main__":
    main()
