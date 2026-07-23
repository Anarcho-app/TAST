#!/usr/bin/env python3
"""
TAST Hierarchical Skeleton (v5.0-alpha)

First concrete step toward retiring fixed RAW_PRIORS and discrete H1–H5
as the objects of inference.

What this module does
---------------------
1. Treats the current stream likelihood values as means of Beta distributions
   whose concentration (kappa) carries a hierarchical hyperprior.
2. Defines continuous latent demographic parameters (growth rate, import
   volume scale, reclassification rate, undercount) with weakly informative
   hyperpriors.
3. Shows how the old discrete hypotheses become derived region probabilities
   over the continuous parameters (not the primary objects of inference).
4. Provides a pure-numpy Monte-Carlo / importance-style sampler so any agent
   can re-run the inference without external MCMC libraries.
5. Keeps the zero-weight collapse: when reliability mass concentrates near 0,
   administrative quantitative claims remain UNDEFINED; only the physical
   floor survives.

What it deliberately does not yet do
------------------------------------
- Full NumPyro / PyMC / Stan HMC or NUTS sampling of a joint hierarchical model.
- Data-level likelihoods for every primary series (census Poisson, burial
  Poisson, etc.). Those are the next increment after this skeleton is stable.
- Fitted (posterior) estimates of the continuous parameters from real data.
  Current draws are prior + likelihood-mean driven illustrations.

Einstein constraint: the interface stays small and the collapse rule remains absolute.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    from physical_likelihoods import physical_loglik
except ImportError:
    physical_loglik = None

HERE = Path(__file__).resolve().parent
STREAMS_CSV = HERE / "evidence_streams.csv"

HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]

# ---------------------------------------------------------------------------
# Continuous latent parameters (the new objects of inference)
# ---------------------------------------------------------------------------
# lambda_growth : annual growth rate (log scale friendly)
# I_scale       : post-1808 import / inflow scale (relative)
# rho_reclass   : reclassification / absorption rate
# undercount    : undercount factor on administrative series
# r_vec         : source-group reliability components

CONTINUOUS_PARAMS = [
    "lambda_growth",
    "I_scale",
    "rho_reclass",
    "undercount",
    "r_owner",
    "r_enumerator",
    "r_coverage",
]


def sample_hyperpriors(rng: np.random.Generator, n: int = 1) -> Dict[str, np.ndarray]:
    """
    Weakly informative hyperpriors (deliberately diffuse).
    These replace the old fixed RAW_PRIORS vector.
    """
    return {
        # growth rate around 0–3 %; half-normal-ish on positive side
        "lambda_growth": rng.normal(0.015, 0.02, size=n),
        # import scale (relative); log-normal around documented order of magnitude
        "I_scale": rng.lognormal(mean=12.5, sigma=1.0, size=n),  # ~e^12.5 ≈ 2.7e5
        # reclassification rate
        "rho_reclass": rng.beta(2, 5, size=n),
        # undercount factor (0 = none, higher = more missing)
        "undercount": rng.beta(2, 8, size=n),
        # reliability components
        "r_owner": rng.beta(2, 2, size=n),
        "r_enumerator": rng.beta(2, 2, size=n),
        "r_coverage": rng.beta(3, 2, size=n),
        # hierarchical concentration for stream likelihoods
        "kappa": rng.gamma(5.0, 2.0, size=n),  # mean ≈ 10
    }


def load_stream_means() -> List[Dict]:
    """Load the existing point likelihoods as means of Beta distributions."""
    rows = []
    with open(STREAMS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for h in HYPOTHESES:
                row[h] = float(row[h])
            row["is_quantitative"] = int(row.get("is_quantitative", 1))
            rows.append(row)
    return rows


def beta_from_mean_kappa(mean: float, kappa: float, rng: np.random.Generator) -> float:
    """Sample from Beta whose mean is the old point likelihood and concentration is kappa."""
    mean = float(np.clip(mean, 0.02, 0.98))
    kappa = max(kappa, 2.0)
    a = mean * kappa
    b = (1.0 - mean) * kappa
    return float(rng.beta(a, b))


def draw_likelihood_table(streams: List[Dict], kappa: float,
                          rng: np.random.Generator) -> List[Dict]:
    """Replace each point L with a draw from Beta(mean=L, concentration=kappa)."""
    out = []
    for s in streams:
        news = dict(s)
        for h in HYPOTHESES:
            news[h] = beta_from_mean_kappa(s[h], kappa, rng)
        out.append(news)
    return out


def reliability_scalar(params: Dict[str, float]) -> float:
    """Reduce multi-axis reliability to the scalar used by the collapse rule."""
    w = np.array([0.4, 0.4, 0.2])
    v = np.array([params["r_owner"], params["r_enumerator"], params["r_coverage"]])
    return float(np.clip(w @ v, 0.0, 1.0))


def apply_reliability_to_streams(streams: List[Dict], r: float) -> List[Dict]:
    scaled = []
    for s in streams:
        news = dict(s)
        if s["is_quantitative"] == 1:
            for h in HYPOTHESES:
                L = s[h]
                news[h] = r * L + (1.0 - r) * 0.5
        scaled.append(news)
    return scaled


def bayes_update_log(streams: List[Dict],
                     log_prior: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Log-space product update.
    If log_prior is None we use a flat prior over the five regions
    (i.e. the old RAW_PRIORS are no longer required).
    """
    if log_prior is None:
        log_prior = {h: -math.log(5.0) for h in HYPOTHESES}
    log_post = {h: log_prior[h] for h in HYPOTHESES}
    for s in streams:
        for h in HYPOTHESES:
            L = max(s[h], 1e-12)
            log_post[h] += math.log(L)
    max_log = max(log_post.values())
    unnorm = {h: math.exp(log_post[h] - max_log) for h in HYPOTHESES}
    total = sum(unnorm.values())
    return {h: unnorm[h] / total for h in HYPOTHESES}


def region_probabilities(params: Dict[str, float]) -> Dict[str, float]:
    """
    Derive the old discrete labels as posterior mass on regions of the
    continuous parameter space. This is illustrative; a full model would
    integrate the continuous posterior over these regions.
    """
    # Extremely simple region definitions for demonstration
    g = params["lambda_growth"]
    rho = params["rho_reclass"]
    und = params["undercount"]
    # Heuristic mapping (replace with proper indicator integrals later)
    scores = {
        "H1": max(0.0, 0.4 - abs(g - 0.025)) * (1.0 - rho),
        "H2": rho * 0.8,
        "H3": 0.3 + 0.4 * (1.0 - abs(g - 0.015)),
        "H4": max(0.0, g) * (1.0 - und),
        "H5": 0.5 + 0.3 * und,  # residual / uncertainty region
    }
    total = sum(scores.values()) + 1e-12
    return {h: scores[h] / total for h in HYPOTHESES}


def hierarchical_monte_carlo(n_samples: int = 400, seed: int = 42) -> Dict:
    """
    Minimal hierarchical Monte Carlo:
      - draw continuous parameters from hyperpriors
      - draw stream likelihoods from Beta(mean=old L, kappa)
      - apply reliability scalar derived from the continuous r-vector
      - obtain both a discrete-region posterior and the continuous draws
    When the reliability scalar is near 0 the administrative path is flagged UNDEFINED.
    """
    rng = np.random.default_rng(seed)
    streams0 = load_stream_means()
    hyper = sample_hyperpriors(rng, n=n_samples)

    post_samples = {h: [] for h in HYPOTHESES}
    r_samples = []
    undefined_count = 0

    physical_lls = []
    for i in range(n_samples):
        params = {k: float(hyper[k][i]) for k in CONTINUOUS_PARAMS}
        kappa = float(hyper["kappa"][i])
        r = reliability_scalar(params)
        r_samples.append(r)

        # Physical-floor log-likelihood (always active)
        pll = 0.0
        if physical_loglik is not None:
            try:
                pll = physical_loglik(params)
            except Exception:
                pll = 0.0
        physical_lls.append(pll)

        if r < 0.05:
            undefined_count += 1
            reg = region_probabilities(params)
            # reweight region probabilities by physical evidence (simple softmax)
            if physical_loglik is not None:
                # boost H5 / continuity-friendly regions when physical ll is high
                reg = {h: reg[h] * math.exp(0.01 * pll * (0.6 if h == "H5" else 0.3)) for h in HYPOTHESES}
                tot = sum(reg.values()) + 1e-12
                reg = {h: reg[h] / tot for h in HYPOTHESES}
            for h in HYPOTHESES:
                post_samples[h].append(reg[h])
            continue

        lik_table = draw_likelihood_table(streams0, kappa, rng)
        scaled = apply_reliability_to_streams(lik_table, r)
        post = bayes_update_log(scaled, log_prior=None)
        # light physical reweight
        if physical_loglik is not None:
            post = {h: post[h] * math.exp(0.005 * pll * (0.5 if h in ("H5", "H3") else 0.2)) for h in HYPOTHESES}
            tot = sum(post.values()) + 1e-12
            post = {h: post[h] / tot for h in HYPOTHESES}
        for h in HYPOTHESES:
            post_samples[h].append(post[h])

    summary = {}
    for h in HYPOTHESES:
        xs = np.array(post_samples[h])
        summary[h] = {
            "mean": float(xs.mean()),
            "q05": float(np.quantile(xs, 0.05)),
            "q50": float(np.quantile(xs, 0.50)),
            "q95": float(np.quantile(xs, 0.95)),
        }

    phys_arr = np.array(physical_lls) if physical_lls else np.array([0.0])
    return {
        "n_samples": n_samples,
        "undefined_fraction": undefined_count / n_samples,
        "r_mean": float(np.mean(r_samples)),
        "r_q05": float(np.quantile(r_samples, 0.05)),
        "r_q95": float(np.quantile(r_samples, 0.95)),
        "physical_ll_mean": float(phys_arr.mean()),
        "physical_ll_std": float(phys_arr.std()),
        "posterior_regions": summary,
        "note": (
            "Discrete H1–H5 are derived region summaries over continuous "
            "parameters. Fixed RAW_PRIORS are no longer used. Physical-floor "
            "likelihoods (burial, aDNA, termination, erasure, regime) are "
            "now active and remain so at r → 0. Full NumPyro/PyMC data-level "
            "models remain the next increment."
        ),
    }


def print_hierarchical_summary(result: Dict) -> None:
    print("TAST Hierarchical Skeleton (v5.0-alpha)")
    print("=" * 60)
    print(f"Samples: {result['n_samples']}")
    print(f"Mean reliability scalar: {result['r_mean']:.3f} "
          f"(5%={result['r_q05']:.3f}, 95%={result['r_q95']:.3f})")
    print(f"Fraction of draws with r < 0.05 (UNDEFINED admin path): "
          f"{result['undefined_fraction']:.1%}")
    if "physical_ll_mean" in result:
        print(f"Physical-floor loglik (mean ± std): "
              f"{result['physical_ll_mean']:.2f} ± {result['physical_ll_std']:.2f}")
    print()
    print("Derived region probabilities (H1–H5 as continuous-parameter regions):")
    print(f"{'H':<4} {'5%':>8} {'50%':>8} {'95%':>8} {'mean':>8}")
    for h in HYPOTHESES:
        s = result["posterior_regions"][h]
        print(f"{h:<4} {s['q05']:8.1%} {s['q50']:8.1%} {s['q95']:8.1%} {s['mean']:8.1%}")
    print()
    print(result["note"])
    print()
    print("CONDITIONAL ESTIMATE. Administrative totals remain NOT A FACT.")
    print("Physical / structural floor is the only layer that survives r → 0.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TAST hierarchical skeleton v5.0-alpha")
    parser.add_argument("--samples", type=int, default=400)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    result = hierarchical_monte_carlo(n_samples=args.samples, seed=args.seed)
    print_hierarchical_summary(result)


if __name__ == "__main__":
    main()
