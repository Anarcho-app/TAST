#!/usr/bin/env python3
"""
Joint model — α_admin vs α_I with category-exit honesty (Opus 4.8 High).

α_I = α_admin · f_I · d   — only quantity O3 constrains
α_admin                   — lookerism/admin; NOT identified by genomes

O3: modern cohort NA-component is a *lower bound* on historical retained
Indigenous-associated ancestry in lineages that stayed in the self-ID sample.
Category exit (reclassification out of AA) removes high-non-African tails
directionally — symmetric Gaussian on 0.8% overclaims.

DNA LIMITS: cohort n≪40M; K-cluster panel-relative; not national measurement;
not α_admin. See dna_sample_size_discipline.md, DNA_LIMITS.md.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional


N_US_1790 = 697_681.0
N_US_1810 = 1_191_362.0
N_US_1860 = 3_953_760.0
IMPORTS_POST_1790 = 140_000.0
N_CARIB_1807 = 775_000.0
N_CARIB_1834 = 665_000.0
YEARS_1790_1860 = 70.0
YEARS_1810_1860 = 50.0
YEARS_CARIB = 27.0

# In-cohort admixture summary (Bryc-class) — NOT a national measurement
BRYC_NA_FLOOR = 0.008  # observed cohort mean as lower-bound center
BRYC_NA_SD_BELOW = 0.002  # tight below the floor
# Above the floor: slow penalty only (category exit → historical α_I plausibly higher)
BRYC_NA_SD_ABOVE = 0.015


@dataclass
class Latents:
    r_us: float
    r_carib: float
    alpha_admin: float
    f_I: float   # panel-relative projection onto NA component under panel P — NOT ethnohistorical headcount fraction
    d: float
    log_sigma: float
    n_pool: float
    exit_bias: float  # ≥0; shifts effective O3 center upward (historical > observed cohort mean)

    @property
    def alpha_I(self) -> float:
        return self.alpha_admin * self.f_I * self.d


@dataclass
class PriorSpec:
    r_us_mu: float = 0.022
    r_us_sd: float = 0.004
    r_carib_mu: float = -0.008
    r_carib_sd: float = 0.010
    alpha_a: float = 1.0
    alpha_b: float = 20.0
    f_I_a: float = 1.0
    f_I_b: float = 1.0
    d_a: float = 1.0
    d_b: float = 1.0
    log_sigma_mu: float = 0.15
    log_sigma_sd: float = 0.05
    n_pool_mu_log: float = math.log(800_000.0)
    n_pool_sd_log: float = 0.5
    # exit_bias ~ Exponential-ish via half-normal scale
    exit_bias_scale: float = 0.01  # prior mass near 0, tail to a few pp


def _forward_us(r: float, alpha_admin: float) -> float:
    stock = N_US_1790 * math.exp(r * YEARS_1790_1860)
    imports = IMPORTS_POST_1790 * math.exp(r * (YEARS_1790_1860 / 2.0))
    african_path = stock + imports
    if alpha_admin >= 0.95:
        return 1e12
    return african_path / (1.0 - alpha_admin)


def _growth(n0, n1, years):
    return math.log(max(n1, 1.0) / max(n0, 1.0)) / years


def _ll_norm(obs, pred, sd):
    if sd <= 1e-12:
        return -1e12
    z = (obs - pred) / sd
    return -0.5 * z * z - math.log(sd) - 0.5 * math.log(2 * math.pi)


def _ll_o3_category_exit(alpha_I: float, exit_bias: float) -> float:
    """One-sided-ish: observed cohort mean is a floor; historical α_I can sit higher.

    Center = BRYC_NA_FLOOR + exit_bias (exit_bias ≥ 0).
    Below center: tight Gaussian. Above center: wide Gaussian (slow penalty).
    """
    center = BRYC_NA_FLOOR + max(exit_bias, 0.0)
    if alpha_I <= center:
        return _ll_norm(alpha_I, center, BRYC_NA_SD_BELOW)
    return _ll_norm(alpha_I, center, BRYC_NA_SD_ABOVE)


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
    # half-normal on exit_bias
    if th.exit_bias < 0:
        return -1e12
    scale = p.exit_bias_scale
    lp += -0.5 * (th.exit_bias / scale) ** 2 - math.log(scale) - 0.5 * math.log(2 * math.pi)
    return lp


def log_likelihood(th: Latents, use_o1=True, use_o2=True, use_o3=True) -> float:
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
        ll += _ll_o3_category_exit(th.alpha_I, th.exit_bias)
    return ll


def log_posterior(th, p, **flags):
    return log_prior(th, p) + log_likelihood(th, **flags)


def _beta(rng, a, b):
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
        exit_bias=abs(nrm(0.0, p.exit_bias_scale)),
    )


def mh_sample(
    n_samples=5000, burn=1500, thin=3, seed=42, prior=None,
    use_o1=True, use_o2=True, use_o3=True,
) -> List[Latents]:
    p = prior or PriorSpec()
    rng = random.Random(seed)
    th = sample_prior(p, rng)
    flags = dict(use_o1=use_o1, use_o2=use_o2, use_o3=use_o3)
    lp = log_posterior(th, p, **flags)
    draws = []
    for i in range(n_samples + burn):
        prop = Latents(
            r_us=th.r_us + 0.002 * rng.gauss(0, 1),
            r_carib=th.r_carib + 0.004 * rng.gauss(0, 1),
            alpha_admin=min(0.99, max(1e-4, th.alpha_admin + 0.03 * rng.gauss(0, 1))),
            f_I=min(0.99, max(1e-4, th.f_I + 0.05 * rng.gauss(0, 1))),
            d=min(0.99, max(1e-4, th.d + 0.05 * rng.gauss(0, 1))),
            log_sigma=max(0.04, th.log_sigma + 0.02 * rng.gauss(0, 1)),
            n_pool=math.exp(math.log(th.n_pool) + 0.3 * rng.gauss(0, 1)),
            exit_bias=max(0.0, th.exit_bias + 0.005 * rng.gauss(0, 1)),
        )
        lp_p = log_posterior(prop, p, **flags)
        if math.log(rng.random()) < lp_p - lp:
            th, lp = prop, lp_p
        if i >= burn and (i - burn) % thin == 0:
            draws.append(th)
    return draws


def summarize(draws: List[Latents], attr: str) -> Dict[str, float]:
    if attr == "alpha_I":
        xs = sorted(d.alpha_I for d in draws)
    else:
        xs = sorted(getattr(d, attr) for d in draws)
    n = len(xs)
    def q(p):
        return xs[min(n - 1, int(p * n))]
    return {"median": q(0.5), "p05": q(0.05), "p95": q(0.95), "p99": q(0.99), "mean": sum(xs)/n}


def _ks_stat(xs, ys) -> float:
    """Two-sample KS statistic (no p-value; threshold used as guardrail)."""
    xs, ys = sorted(xs), sorted(ys)
    grid = sorted(set(xs + ys))
    n, m = len(xs), len(ys)
    i = j = 0
    d = 0.0
    for v in grid:
        while i < n and xs[i] <= v:
            i += 1
        while j < m and ys[j] <= v:
            j += 1
        d = max(d, abs(i / n - j / m))
    return d


def guardrail_o3_decouples_alpha_admin(seed=42, n_samples=4000, burn=1000) -> bool:
    """Guardrail against implied_na = alpha_admin re-coupling.

    Legal: O3 constrains α_I = α_admin·f_I·d; with vague f_I/d, α_admin stays diffuse.
    Illegal: O3 pins α_admin near the Bryc floor (~0.008).

    PASS if under vague f_I/d:
      - α_admin median is not near BRYC_NA_FLOOR (distance > 0.01)
      - α_admin p95 - p05 width > 0.05 (still diffuse)
    And under forced f_I≈d≈1, α_admin *does* pin near the floor (sanity).
    """
    vague = PriorSpec()
    pinned = PriorSpec(f_I_a=40.0, f_I_b=1.2, d_a=40.0, d_b=1.2)
    d_v = mh_sample(n_samples, burn, 2, seed, vague, True, True, True)
    d_p = mh_sample(n_samples, burn, 2, seed + 3, pinned, True, True, True)
    sv = summarize(d_v, "alpha_admin")
    sp = summarize(d_p, "alpha_admin")
    width_v = sv["p95"] - sv["p05"]
    # vague: not pinned to floor, still wide
    not_pinned = abs(sv["median"] - BRYC_NA_FLOOR) > 0.01 and width_v > 0.05
    # forced identity: median near floor
    identity_pins = abs(sp["median"] - BRYC_NA_FLOOR) < 0.02
    ok = not_pinned and identity_pins
    print(
        f"GUARDRAIL: vague α_admin med={sv['median']:.4f} width90={width_v:.4f}  "
        f"pinned med={sp['median']:.4f}  {'PASS' if ok else 'FAIL'}"
    )
    print(
        f"  (vague must stay diffuse & off-floor; f_I≈d≈1 must pin near {BRYC_NA_FLOOR})"
    )
    return ok



def alpha_I_exit_sensitivity(seed=42) -> None:
    """α_I as a function of category-exit prior scale — the honest report form."""
    print("α_I sensitivity to exit_bias_scale (category-exit prior)")
    print(f"{'exit_scale':>12}  {'med':>8}  {'p05':>8}  {'p95':>8}  {'p99':>8}")
    for scale in (0.001, 0.01, 0.04):
        pr = PriorSpec(exit_bias_scale=scale)
        draws = mh_sample(4000, 1000, 2, seed, pr, True, True, True)
        s = summarize(draws, "alpha_I")
        print(
            f"{scale:12.3f}  {s['median']:8.4f}  {s['p05']:8.4f}  "
            f"{s['p95']:8.4f}  {s['p99']:8.4f}"
        )
    print("Report α_I as this table, not a single p99.")


def main():
    print("Joint model — category-exit O3 + α_admin/α_I split\n")
    p = PriorSpec()
    print("--- Full model, vague f_I/d ---")
    draws = mh_sample(5000, 1200, 3, 42, p)
    si = summarize(draws, "alpha_I")
    sa = summarize(draws, "alpha_admin")
    se = summarize(draws, "exit_bias")
    print(f"  α_I     med={si['median']:.4f}  90%CI [{si['p05']:.4f},{si['p95']:.4f}]  p99={si['p99']:.4f}")
    print(f"  α_admin med={sa['median']:.4f}  90%CI [{sa['p05']:.4f},{sa['p95']:.4f}]  p99={sa['p99']:.4f}  (NOT ID by O3)")
    print(f"  exit_bias med={se['median']:.4f}  p95={se['p95']:.4f}")
    print()
    print("--- O3 off (α_I should wander; α_admin similar if vague) ---")
    d2 = mh_sample(4000, 1000, 2, 42, p, True, True, False)
    print(f"  α_I     med={summarize(d2,'alpha_I')['median']:.4f} p99={summarize(d2,'alpha_I')['p99']:.4f}")
    print(f"  α_admin med={summarize(d2,'alpha_admin')['median']:.4f} p99={summarize(d2,'alpha_admin')['p99']:.4f}")
    print()
    guardrail_o3_decouples_alpha_admin()
    print()
    alpha_I_exit_sensitivity()
    print()
    print("Claim: α_I ≥ ~0.8% in-cohort (lower bound); upper end conditional on exit prior (~3–5%);")
    print("       α_admin unidentified by genomes; f_I panel-relative; n≪40M; not 5–7 race boxes.")


if __name__ == "__main__":
    main()
