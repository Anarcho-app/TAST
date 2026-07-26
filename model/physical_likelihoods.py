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
VERIFIED_ADNA_YAML = ROOT / "data" / "verified_isotope_adna.yaml"


def _const(cid, fallback):
    """Declared-constant lookup with an explicit fallback (lenient-mode safe)."""
    try:
        try:
            from __init__ import load_constant  # type: ignore
        except Exception:
            from model import load_constant  # type: ignore
        return load_constant(cid)
    except Exception:
        return fallback


def _n_adna_from_verified_studies(path: Path = VERIFIED_ADNA_YAML):
    """Derive the aDNA individual count from data/verified_isotope_adna.yaml.

    Closes audit #36. Until 2026-07-25 this file was read by no code and
    `n_adna_individuals` was the hardcoded literal 66 ("Harney27+Fleskes36+
    Schroeder3"), which contradicted the replacement path declared inside that
    same file ("Harney 27 + Fleskes 18 genomes").

    Two policy flags govern the sum, both declared in stipulated_constants.yaml:
      adna_require_us_territory — drop studies with us_territory: false, because
        the floor statement is "interred on American soil" (excludes Schroeder
        n=3, Saint Martin).
      adna_prefer_genome_counts — use each study's declared `adna_count_field`.
        Individuals excavated and individuals with recovered genomes are
        different observables; loglik_adna_sample is about the latter (Fleskes
        contributes 18 genomes, not 36 excavated).

    Returns (count, basis_string, per_study_rows) or (None, reason, []) if the
    file is unavailable — caller keeps the dataclass fallback.
    """
    if not path.exists():
        return None, f"verified_isotope_adna.yaml not found at {path}", []
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, f"verified_isotope_adna.yaml unreadable: {e}", []

    require_us = bool(_const("adna_require_us_territory", 1))
    prefer_genomes = bool(_const("adna_prefer_genome_counts", 1))

    total, rows = 0, []
    for st in data.get("verified_studies", []) or []:
        sid = str(st.get("id"))
        field = st.get("adna_count_field")
        in_us = bool(st.get("us_territory", False))
        if not field:
            rows.append((sid, 0, "skipped: not an aDNA individual-recovery study"))
            continue
        if require_us and not in_us:
            rows.append((sid, 0, f"excluded: us_territory=false (site={st.get('site')!r})"))
            continue
        if not prefer_genomes and st.get("n_individuals") is not None:
            field = "n_individuals"
        n = st.get(field)
        if n is None:
            rows.append((sid, 0, f"skipped: field {field!r} absent"))
            continue
        total += int(n)
        rows.append((sid, int(n), f"counted via {field}"))

    basis = (f"derived from verified_isotope_adna.yaml "
             f"(require_us_territory={require_us}, prefer_genome_counts={prefer_genomes})")
    return total, basis, rows


def _n_distinct_burial_sites(by_id: dict, confidence_floor: float):
    """Count DISTINCT physical burial sites, not YAML rows.

    Closes audit #29/#37. The previous selector counted matching rows, so
    African Burial Ground NYC contributed 4 (floor-02, 23, 33, 67) and Harlem 2
    (50, 68) purely because they were written up more than once. A Poisson count
    inflated by documentation density is exactly the defect this project
    attributes to administrative records, reproduced inside the floor.

    Dedup is now data-driven via the `site_key` field on each fact row:
      site_role: aggregate_statement -> multi-site statement, survey, or
        database; not a distinct site.
      site_scope: comparative_control -> outside "the territory that became the
        United States" (Estate Little Princess, St. Croix — Danish colonial).

    Returns (count, sorted_keys, skipped_rows).
    """
    keys, skipped = set(), []
    for fid, f in by_id.items():
        stmt = (f.get("statement") or "").lower()
        if not any(k in stmt for k in ("burial", "cemetery", "adna", "remains")):
            continue
        if f.get("confidence", 0) < confidence_floor:
            skipped.append((fid, "below confidence floor"))
            continue
        if f.get("site_role"):
            skipped.append((fid, f"site_role={f['site_role']}"))
            continue
        if f.get("site_scope") == "comparative_control":
            skipped.append((fid, "site_scope=comparative_control"))
            continue
        key = f.get("site_key")
        if not key or key == "null":
            skipped.append((fid, "no site_key"))
            continue
        keys.add(key)
    return len(keys), sorted(keys), skipped


def _n_regime_from_inventory() -> int:
    """Prefer counted inventory over stipulated 12."""
    inv = ROOT / "data" / "jurisdiction_inventory.yaml"
    if inv.exists():
        try:
            import yaml
            data = yaml.safe_load(inv.read_text(encoding="utf-8"))
            n = int(data.get("summary", {}).get("n_regime_jurisdictions_verified", 0) or 0)
            if n > 0:
                return n
        except Exception:
            pass
    return 12  # stipulated fallback


@dataclass
class PhysicalObservations:
    n_burial_sites: int = 8
    n_individuals_lower: float = 15000.0
    # Upper bound of the anchor-site interment interval (audit #39). floor-02
    # reads "15,000-20,000 (estimate)"; storing only the lower bound discarded
    # the uncertainty. The interval is what makes this the floor's strongest
    # observable, so both bounds are now parsed and reported.
    n_individuals_upper: float = 20000.0
    n_individuals_source: str = "floor-02 (dataclass fallback)"
    # Derived at load from verified_isotope_adna.yaml (audit #36). The fallback
    # is the US-territory genome sum (Harney 27 + Fleskes 18 genomes), NOT the
    # former literal 66 which counted Fleskes' 36 excavated plus Schroeder's 3
    # Saint Martin individuals.
    n_adna_individuals: int = 45
    termin_in_us_frac: float = 0.85
    erasure_log_ratio: float = 4.5
    n_regime_jurisdictions: int = 12  # overridden at load from inventory when present
    source_note: str = "fallback defaults (YAML not loaded)"
    # Derivation provenance — so a reader can see WHERE each count came from
    # instead of trusting a comment next to a literal.
    n_adna_basis: str = "dataclass fallback (verified_isotope_adna.yaml not loaded)"
    n_adna_rows: tuple = ()
    n_burial_sites_basis: str = "dataclass fallback (observable_facts.yaml not loaded)"
    n_burial_site_keys: tuple = ()


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


def _parse_number_interval(text: Optional[str]):
    """Return (lo, hi) from a string like '15,000-20,000 (estimate)'.

    Returns (None, None) if no interval is present, (n, n) if a single number.
    Both en-dash (U+2013) and ASCII hyphen are accepted as the separator.
    """
    if not text:
        return None, None
    s = str(text).replace(",", "").replace("\u2013", "-").replace("\u2014", "-")
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    nums = [float(n) for n in nums if float(n) > 0]
    if not nums:
        return None, None
    if len(nums) >= 2:
        return min(nums[:2]), max(nums[:2])
    return nums[0], nums[0]


def load_observations_from_yaml(path: Path = FACTS_YAML) -> PhysicalObservations:
    """
    Map high-confidence floor facts into PhysicalObservations.
    Missing fields keep conservative defaults. Fully inspectable.

    Posterior-steering scalars (erasure_log_ratio, genealogical_n_eff) are
    sourced from data/stipulated_constants.yaml via load_constant() so they are
    declared rather than hardcoded (audit #27/#28). Fail-closed: an undeclared
    id raises unless TAST_CONSTANTS_LENIENT is set.
    """
    try:
        from __init__ import load_constant  # type: ignore
    except Exception:
        from model import load_constant  # type: ignore
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
    # burial individuals interval from floor-02 or claim 33 (audit #39):
    # parse BOTH bounds, not just the lower. "15,000-20,000 (estimate)" carries
    # an interval and the interval is what makes this the floor's strongest
    # observable.
    for key in ("floor-02", "33", "23"):
        f = by_id.get(key)
        if f and f.get("value"):
            lo, hi = _parse_number_interval(f["value"])
            if lo and lo > 1000:
                obs.n_individuals_lower = lo
                obs.n_individuals_upper = max(hi, lo)
                obs.n_individuals_source = f"{key} ({f.get('source','?')})"
                notes.append(f"n_individuals[{lo:.0f},{hi:.0f}]<-{key}")
                break

    # presence sites: count DISTINCT sites via site_key, not matching rows
    # (audit #29/#37). Confidence floor is a declared constant.
    conf_floor = float(_const("burial_site_confidence_floor", 0.85))
    n_sites, site_keys, _skipped = _n_distinct_burial_sites(by_id, conf_floor)
    if n_sites > 0:
        obs.n_burial_sites = n_sites
        obs.n_burial_site_keys = tuple(site_keys)
        obs.n_burial_sites_basis = (
            f"{n_sites} distinct site_key values at confidence >= {conf_floor} "
            f"(deduplicated from matching rows; audit #29/#37)"
        )
        notes.append(f"n_burial_sites<-{n_sites} distinct sites")

    # aDNA: derive from the verified-study table rather than asserting a literal
    # (audit #36). verified_isotope_adna.yaml was previously read by no code.
    n_adna, adna_basis, adna_rows = _n_adna_from_verified_studies()
    if n_adna is not None and n_adna > 0:
        obs.n_adna_individuals = n_adna
        obs.n_adna_basis = adna_basis
        obs.n_adna_rows = tuple(adna_rows)
        notes.append(f"n_adna<-{n_adna} (verified studies, US territory, genome counts)")
    else:
        obs.n_adna_basis = f"fallback {obs.n_adna_individuals}: {adna_basis}"

    # genealogical termination
    if "floor-04" in by_id and by_id["floor-04"].get("confidence", 0) >= 0.85:
        obs.termin_in_us_frac = 0.85
        notes.append("termin_in_us_frac<-floor-04")

    # structural silence / regime: keep structural constants (not functions of r)
    if "floor-05" in by_id or "floor-06" in by_id:
        try:
            obs.erasure_log_ratio = float(load_constant("erasure_log_ratio"))
        except Exception:
            pass  # keep dataclass default under lenient mode
        obs.n_regime_jurisdictions = _n_regime_from_inventory()
        notes.append("erasure/regime<-floor-05/06")

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
    try:
        from __init__ import load_constant  # type: ignore
    except Exception:
        from model import load_constant  # type: ignore
    try:
        n_eff = float(load_constant("genealogical_n_eff"))
    except Exception:
        n_eff = 200.0
    p = float(np.clip(p_term, 1e-3, 1.0 - 1e-3))
    k = obs.termin_in_us_frac * n_eff
    return k * math.log(p) + (n_eff - k) * math.log(1.0 - p)


def loglik_erasure(asymmetry: float, obs: PhysicalObservations = OBS) -> float:
    try:
        from __init__ import load_constant  # type: ignore
    except Exception:
        from model import load_constant  # type: ignore
    try:
        sigma = float(load_constant("erasure_sigma"))
    except Exception:
        sigma = 1.2
    mu = asymmetry
    x = obs.erasure_log_ratio
    return -0.5 * math.log(2 * math.pi * sigma**2) - 0.5 * ((x - mu) / sigma) ** 2


def loglik_regime_intensity(n_expected: float, obs: PhysicalObservations = OBS) -> float:
    lam = max(n_expected, 0.5)
    k = obs.n_regime_jurisdictions
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def _floor_fact_is_valueless(fact_id: str) -> bool:
    """True if the backing observable_fact carries no numeric value (audit #27).

    A floor term whose backing fact is valueless MUST be excluded from the
    evidential total: the engine cannot assert a measured quantity the floor
    document disclaims. Currently floor-04 (genealogical termination) is null.
    """
    try:
        import yaml
        data = yaml.safe_load(FACTS_YAML.read_text(encoding="utf-8"))
        for f in data.get("facts", []):
            if str(f.get("id")) == fact_id:
                return f.get("value") in (None, "", "null")
    except Exception:
        pass
    return False


def _primary_observables(obs: PhysicalObservations) -> list:
    """The load-bearing content of the floor: what survives victors_reliability -> 0.

    Ordered by evidential force, not by which term feeds the Bayes factor.
    The floor's job (per README/METHODS) is to report the observables that
    survive maximal skepticism of the administrative series. The Bayes factor
    against the straw null is a secondary, explicitly-caveated quantity; THESE
    are the primary content.

    The interment estimate is listed FIRST and deliberately not folded into the
    BF. See `not_in_bf_reason` for the reductio that justifies that choice.
    """
    mid = (obs.n_individuals_lower + obs.n_individuals_upper) / 2.0
    span = obs.n_individuals_upper - obs.n_individuals_lower
    return [
        {
            "name": "ABG NYC interment estimate (anchor site)",
            "value": f"{obs.n_individuals_lower:,.0f}-{obs.n_individuals_upper:,.0f} (midpoint ~{mid:,.0f})",
            "source": obs.n_individuals_source,
            "role": "primary presence evidence; decisive by inspection",
            "in_bf": False,
            "not_in_bf_reason": (
                "Correctly encoded as a lognormal measurement-error term, this one "
                "observable moves the straw-null Bayes factor from ~3.5 to ~3,190 nats "
                f"(the tightly-measured ~{mid:,.0f} is an ~80-sigma mismatch against the "
                "null's expected ~50 scattered burials). That number is not information; "
                "it is the null being a straw. Reported as decisive-by-inspection instead."
            ),
        },
        {
            "name": "distinct U.S. burial sites (site_key-deduplicated)",
            "value": obs.n_burial_sites,
            "source": obs.n_burial_sites_basis,
            "role": "presence",
            "in_bf": True,
            "site_keys": list(obs.n_burial_site_keys),
        },
        {
            "name": "aDNA individuals (U.S. territory, recovered genomes)",
            "value": obs.n_adna_individuals,
            "source": obs.n_adna_basis,
            "role": "presence + ancestry composition",
            "in_bf": True,
            "per_study": list(obs.n_adna_rows),
        },
    ]


# Terms marked informative:false in the manifest are constants, not evidence;
# physical_floor_report lists them separately from the evidential total.
NONINFORMATIVE_TERMS = ("loglik_erasure", "loglik_regime_intensity")


def _unused_observables(obs: PhysicalObservations) -> list:
    """Observations that are loaded but feed NO likelihood term.

    Audit #39 originally flagged `n_individuals_lower` (the 15,000-20,000 ABG
    interment estimate) here. It has since been PROMOTED to the primary
    `observables` list — see `_primary_observables()` — because the floor's
    strongest observable should be the floor's lead item, not a dead-code
    footnote. It is still not wired into any likelihood term, for the reason
    recorded in its `not_in_bf_reason`: correctly encoding it as a lognormal
    measurement-error term moves the straw-null Bayes factor from ~3.5 to
    ~3,190 nats (the tightly-measured 17,500 is an ~80-sigma mismatch against
    the null's expected ~50). That number is not information; it is the null
    being a straw. So the observable is reported, not encoded.

    Returns any remaining genuinely-unused observables. Currently empty.
    """
    return []


def physical_loglik(params: Dict[str, float], obs: Optional[PhysicalObservations] = None) -> float:
    """
    Total log-likelihood from the physical / structural floor.
    Structural asymmetry and regime counts are FIXED (not functions of r).

    Valueless-backed terms (their observable_fact has value: null) are EXCLUDED
    so the engine does not assert a measured quantity the floor document
    disclaims (audit #27). The genealogical term is excluded because floor-04
    carries no numeric value.
    """
    if obs is None:
        obs = OBS
    report = physical_floor_report(params, obs)
    return report["ll_informative"] + report["ll_noninformative"]


def physical_floor_report(
    params: Optional[Dict[str, float]] = None,
    obs: Optional[PhysicalObservations] = None,
) -> Dict[str, object]:
    """Detailed floor evaluation for honest reporting (audit #27, #28, #30).

    Returns a dict with:
      ll_informative        : sum of informative, value-backed terms
      ll_noninformative     : sum of terms marked informative:false (constants)
      excluded              : [{term, fact_id, reason}] valueless-backed exclusions
      ll_null               : floor under the named null model (for Bayes factor)
      null_name             : the declared null
      log_bayes_factor      : ll_informative - ll_null  (support vs null)
    """
    if obs is None:
        obs = OBS
    if params is None:
        params = {"lambda_growth": 0.015, "rho_reclass": 0.25}

    presence = 1.0 / (1.0 + math.exp(-20.0 * (params.get("lambda_growth", 0.01) - 0.005)))
    n_sites_exp = 3.0 + 10.0 * presence
    adna_rate = 20.0 + 120.0 * presence
    p_term = float(np.clip(0.55 + 0.40 * (1.0 - params.get("rho_reclass", 0.3)), 0.05, 0.95))
    asymmetry = obs.erasure_log_ratio
    n_reg = float(obs.n_regime_jurisdictions)

    term_values = {
        "loglik_burial_sites": loglik_burial_sites(n_sites_exp, obs),
        "loglik_adna_sample": loglik_adna_sample(adna_rate, obs),
        "loglik_genealogical_termination": loglik_genealogical_termination(p_term, obs),
        "loglik_erasure": loglik_erasure(asymmetry, obs),
        "loglik_regime_intensity": loglik_regime_intensity(n_reg, obs),
    }

    # valueless-backed exclusions (audit #27)
    backing = {"loglik_genealogical_termination": "floor-04"}
    excluded = []
    for term, fact_id in backing.items():
        if _floor_fact_is_valueless(fact_id):
            excluded.append({"term": term, "fact_id": fact_id,
                             "reason": "backing fact has value: null; term asserts a measured quantity the floor document disclaims"})

    excluded_terms = {e["term"] for e in excluded}
    ll_informative = 0.0
    ll_noninformative = 0.0
    for term, val in term_values.items():
        if term in excluded_terms:
            continue
        if term in NONINFORMATIVE_TERMS:
            ll_noninformative += val
        else:
            ll_informative += val

    # Named null: "no sustained multi-generational presence" (presence -> 0).
    # ADOPTED DEFAULT (design.md open question), reversible pending maintainer
    # refinement. This is close to a straw null and the Bayes factor against it
    # is therefore an upper bound on the floor's evidential support.
    # ll_null uses the SAME presence-dependent informative terms (burial, aDNA)
    # evaluated at the null, so the BF is a clean presence-vs-no-presence contrast.
    null_presence = 0.0
    null_n_sites = 3.0 + 10.0 * null_presence
    null_adna = 20.0 + 120.0 * null_presence
    ll_null = loglik_burial_sites(null_n_sites, obs) + loglik_adna_sample(null_adna, obs)

    return {
        "ll_informative": ll_informative,
        "ll_noninformative": ll_noninformative,
        "excluded": excluded,
        "unused_observables": _unused_observables(obs),
        "observables": _primary_observables(obs),
        "term_values": term_values,
        "ll_null": ll_null,
        "null_name": "no sustained multi-generational presence (straw null; reversible default)",
        "log_bayes_factor": ll_informative - ll_null,
        "bf_caveat": (
            "UPPER BOUND vs a self-declared straw null. The absolute value is not "
            "load-bearing: correctly encoding the ABG interment estimate alone moves "
            "this number from ~3.5 to ~3,190 nats, which is the reductio. The "
            "observables list is the primary content; this BF is secondary."
        ),
        "counts": {
            "n_burial_sites": obs.n_burial_sites,
            "n_burial_sites_basis": obs.n_burial_sites_basis,
            "n_burial_site_keys": list(obs.n_burial_site_keys),
            "n_adna_individuals": obs.n_adna_individuals,
            "n_adna_basis": obs.n_adna_basis,
            "n_adna_rows": list(obs.n_adna_rows),
            "n_individuals_interval": [obs.n_individuals_lower, obs.n_individuals_upper],
            "n_individuals_source": obs.n_individuals_source,
        },
    }


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
    try:
        from __init__ import configure_utf8_console
    except Exception:
        from model import configure_utf8_console
    configure_utf8_console()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    demonstrate_physical_likelihoods(seed=args.seed)


if __name__ == "__main__":
    main()
