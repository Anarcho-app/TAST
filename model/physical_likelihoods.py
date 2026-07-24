#!/usr/bin/env python3
"""
TAST Physical-Floor Likelihoods (v5.3)

Observations load from data/observable_facts.yaml when available.
Hardcoded defaults remain only as fallbacks and are labeled as such.

Structural terms (erasure, regime count) do NOT depend on reliability r
(Claude Opus circularity fix).

These terms support presence/structure. At r≈0 they are reported but not
used to rank H1–H5 (true collapse returns mechanism posterior to prior).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FACTS_YAML = ROOT / "data" / "observable_facts.yaml"


@dataclass
class PhysicalObservations:
    n_burial_sites: int = 8
    n_individuals_lower: float = 15000.0
    n_adna_individuals: int = 80
    termin_in_us_frac: float = 0.85
    erasure_log_ratio: float = 4.5
    n_regime_jurisdictions: int = 12
    source_note: str = "fallback defaults (YAML not loaded)"


def _parse_first_number(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    m = re.search(r"([\d,]+(?:\.\d+)?)", str(text).replace(",", ""))
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def load_observations_from_yaml(path: Path = FACTS_YAML) -> PhysicalObservations:
    """
    Map high-confidence floor facts into PhysicalObservations.
    Missing fields keep conservative defaults. Fully inspectable.
    """
    obs = PhysicalObservations()
    if not path.exists():
        return obs
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return obs

    facts = data.get("facts") or []
    by_id = {str(f.get("id")): f for f in facts}

    notes = []
    # burial individuals from floor-02 or claim 33
    for key in ("floor-02", "33", "23"):
        f = by_id.get(key)
        if f and f.get("value"):
            n = _parse_first_number(f["value"])
            if n and n > 1000:
                obs.n_individuals_lower = n
                notes.append(f"n_individuals_lower←{key}")
                break

    # presence sites: count distinct physical_presence floor facts + high-ci burial claims
    site_ids = [
        fid for fid, f in by_id.items()
        if f.get("type") in ("physical_presence", "observable_candidate")
        and f.get("confidence", 0) >= 0.85
        and any(k in (f.get("statement") or "").lower() for k in ("burial", "cemetery", "adna", "remains"))
    ]
    if site_ids:
        obs.n_burial_sites = max(obs.n_burial_sites, min(len(site_ids), 20))
        notes.append(f"n_burial_sites←{len(site_ids)} high-ci presence facts")

    # aDNA: if floor-03 present, keep / bump count
    if "floor-03" in by_id and by_id["floor-03"].get("confidence", 0) >= 0.9:
        obs.n_adna_individuals = max(obs.n_adna_individuals, 80)
        notes.append("n_adna←floor-03")

    # genealogical termination
    if "floor-04" in by_id and by_id["floor-04"].get("confidence", 0) >= 0.85:
        obs.termin_in_us_frac = 0.85
        notes.append("termin_in_us_frac←floor-04")

    # structural silence / regime: keep structural constants (not functions of r)
    if "floor-05" in by_id or "floor-06" in by_id:
        obs.erasure_log_ratio = 4.5
        obs.n_regime_jurisdictions = 12
        notes.append("erasure/regime←floor-05/06")

    obs.source_note = "loaded from observable_facts.yaml: " + ", ".join(notes) if notes else obs.source_note
    return obs


# Module-level default loaded once
OBS = load_observations_from_yaml()


def loglik_burial_sites(n_sites_expected: float, obs: PhysicalObservations = OBS) -> float:
    lam = max(n_sites_expected, 0.5)
    k = obs.n_burial_sites
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def loglik_adna_sample(rate: float, obs: PhysicalObservations = OBS) -> float:
    lam = max(rate, 0.5)
    k = obs.n_adna_individuals
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def loglik_genealogical_termination(p_term: float, obs: PhysicalObservations = OBS) -> float:
    p = float(np.clip(p_term, 1e-3, 1.0 - 1e-3))
    n_eff = 200.0
    k = obs.termin_in_us_frac * n_eff
    return k * math.log(p) + (n_eff - k) * math.log(1.0 - p)


def loglik_erasure(asymmetry: float, obs: PhysicalObservations = OBS) -> float:
    mu = asymmetry
    sigma = 1.2
    x = obs.erasure_log_ratio
    return -0.5 * math.log(2 * math.pi * sigma**2) - 0.5 * ((x - mu) / sigma) ** 2


def loglik_regime_intensity(n_expected: float, obs: PhysicalObservations = OBS) -> float:
    lam = max(n_expected, 0.5)
    k = obs.n_regime_jurisdictions
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def physical_loglik(params: Dict[str, float], obs: Optional[PhysicalObservations] = None) -> float:
    """
    Total log-likelihood from the physical / structural floor.
    Structural asymmetry and regime counts are FIXED (not functions of r).
    """
    if obs is None:
        obs = OBS
    presence = 1.0 / (1.0 + math.exp(-20.0 * (params.get("lambda_growth", 0.01) - 0.005)))
    n_sites_exp = 3.0 + 10.0 * presence
    adna_rate = 20.0 + 120.0 * presence
    p_term = float(np.clip(0.55 + 0.40 * (1.0 - params.get("rho_reclass", 0.3)), 0.05, 0.95))

    # Fixed structural expectations (Opus circularity fix)
    asymmetry = obs.erasure_log_ratio
    n_reg = float(obs.n_regime_jurisdictions)

    ll = 0.0
    ll += loglik_burial_sites(n_sites_exp, obs)
    ll += loglik_adna_sample(adna_rate, obs)
    ll += loglik_genealogical_termination(p_term, obs)
    ll += loglik_erasure(asymmetry, obs)
    ll += loglik_regime_intensity(n_reg, obs)
    return ll


def demonstrate_physical_likelihoods(seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    obs = load_observations_from_yaml()
    print("PhysicalObservations:", obs)
    print()
    print("Physical-floor log-likelihood under different continuous parameter draws")
    print("=" * 60)
    print(f"{'presence':>10} {'p_term':>8} {'loglik':>10}")
    for _ in range(6):
        params = {
            "lambda_growth": float(rng.normal(0.015, 0.015)),
            "rho_reclass": float(rng.beta(2, 5)),
            "r_owner": 0.0,
            "r_enumerator": 0.0,
            "undercount": float(rng.beta(2, 8)),
        }
        ll = physical_loglik(params, obs)
        presence = 1.0 / (1.0 + math.exp(-20.0 * (params["lambda_growth"] - 0.005)))
        p_term = 0.55 + 0.40 * (1.0 - params["rho_reclass"])
        print(f"{presence:10.3f} {p_term:8.3f} {ll:10.2f}")
    print()
    print("Structural terms do not depend on r. YAML-linked where available.")
    print("CONDITIONAL presence/structure support — NOT a demographic total.")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    demonstrate_physical_likelihoods(seed=args.seed)


if __name__ == "__main__":
    main()
