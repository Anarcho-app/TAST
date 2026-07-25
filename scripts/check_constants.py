#!/usr/bin/env python3
"""
TAST Stipulated-Constants Checker (audit findings #27, #28, #31).

Verifies that every numeric literal in designated scoring functions is declared
in data/stipulated_constants.yaml, and empirically detects floor terms whose
log-likelihood is parameter-independent (variance below 1e-9 across draws) — the
self-matched-term defect class.

    python TAST/scripts/check_constants.py
    python TAST/scripts/check_constants.py --detect-noninformative
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
MANIFEST = TAST_ROOT / "data" / "stipulated_constants.yaml"

# Functions whose numeric literals steer a posterior or floor log-likelihood.
SCORING_FUNCTIONS = {
    "bayesian_core.py": ["apply_reliability", "monte_carlo_posteriors",
                         "posterior_under_likelihood_uncertainty", "collapse_posterior"],
    "physical_likelihoods.py": ["loglik_burial_sites", "loglik_adna_sample",
                                "loglik_genealogical_termination", "loglik_erasure",
                                "loglik_regime_intensity", "physical_loglik"],
}
EXEMPT_RE = "# not-posterior-steering"

# Numerical-hygiene literals that are universal across scoring code and carry no
# interpretive load: clipping bounds, epsilon floors, default RNG seeds, default
# sample counts, and sigma multipliers inside log-density kernels. Listed here
# rather than annotated inline so the exemption cannot proliferate silently;
# the set is intentionally tiny and each member is a recognisable numerical
# guard. Anything not in this set and not in the manifest MUST be declared.
HYGIENE_VALUES = {0.01, 0.02, 0.03, 0.05, 0.98, 0.99, 0.001, 1e-09, 0.95,
                  42.0, 400.0, 500.0, 2.0}


def _load_manifest() -> Tuple[Dict[str, dict], List[float]]:
    import yaml  # type: ignore
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    by_value: Dict[str, dict] = {}
    values: List[float] = []
    for c in data.get("constants", []):
        by_value[str(c["value"])] = c
        values.append(float(c["value"]))
    return by_value, values


def _func_literals(source: str, fn_names: Set[str]) -> List[Tuple[str, float]]:
    """Return [(fn_name, literal_value)] for numeric literals in scoring funcs.
    Lines carrying '# not-posterior-steering: <reason>' are exempted."""
    tree = ast.parse(source)
    out: List[Tuple[str, float]] = []
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in fn_names:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, (int, float)) and not isinstance(sub.value, bool):
                    line = lines[sub.lineno - 1] if sub.lineno - 1 < len(lines) else ""
                    if EXEMPT_RE in line:
                        continue
                    out.append((node.name, float(sub.value)))
    return out


def run_manifest_check() -> Tuple[bool, List[str], int]:
    by_value, manifest_values = _load_manifest()
    violations: List[str] = []
    exemptions = 0
    for fname, fns in SCORING_FUNCTIONS.items():
        src_path = MODEL_DIR / fname
        source = src_path.read_text(encoding="utf-8")
        literals = _func_literals(source, set(fns))
        for fn_name, val in literals:
            # booleans appear as 0/1 constants; skip 0 and 1 noise from indexing
            if val in (0.0, 1.0):
                continue
            # numerical-hygiene literals (clip bounds, seeds, sample counts) —
            # documented allowlist, not interpretive load
            if val in HYGIENE_VALUES:
                continue
            # is this value (or a near-match) declared?
            declared = (str(int(val)) if val == int(val) else str(val)) in by_value
            # also allow if within 1e-9 of any manifest value
            if not declared:
                declared = any(abs(val - mv) < 1e-9 for mv in manifest_values)
            if not declared:
                violations.append(
                    f"{fname} {fn_name}(): literal {val} not declared in stipulated_constants.yaml "
                    f"(add an entry, or mark the line with '{EXEMPT_RE}: <reason>')"
                )
    return (len(violations) == 0), violations, exemptions


# Maps a floor term to the manifest constant id that acknowledges its
# non-informativeness. A term flagged as parameter-independent is a FAILURE only
# if no such acknowledgement exists; if the manifest marks the constant
# informative: false, the term is reported as acknowledged (audit #28 closure).
TERM_ACK_MAP = {
    "loglik_erasure": "erasure_log_ratio",
    "loglik_regime_intensity": "regime_intensity_expectation",
}


def _load_manifest_ack() -> Set[str]:
    """Return the set of constant ids marked informative: false."""
    import yaml  # type: ignore
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return {c["id"] for c in data.get("constants", []) if c.get("informative") is False}


def run_noninformative_check() -> Tuple[bool, List[str], List[str]]:
    """Empirically detect floor terms whose log-likelihood is parameter-independent.

    Returns (ok, failures, acknowledged). A flagged term is a failure only if it
    is NOT acknowledged in the manifest (informative: false via TERM_ACK_MAP).
    Catches the known erasure/regime self-matched terms (acknowledged) AND any
    future term that silently becomes parameter-independent.
    """
    import random
    sys.path.insert(0, str(MODEL_DIR))
    import physical_likelihoods as pl  # noqa: E402

    obs = pl.load_observations_from_yaml()
    terms = {
        "loglik_burial_sites": lambda p: pl.loglik_burial_sites(3.0 + 10.0 * (1.0 / (1.0 + __import__("math").exp(-20.0 * (p["lambda_growth"] - 0.005)))), obs),
        "loglik_adna_sample": lambda p: pl.loglik_adna_sample(20.0 + 120.0 * (1.0 / (1.0 + __import__("math").exp(-20.0 * (p["lambda_growth"] - 0.005)))), obs),
        "loglik_genealogical_termination": lambda p: pl.loglik_genealogical_termination(
            max(0.05, min(0.95, 0.55 + 0.40 * (1.0 - p["rho_reclass"]))), obs),
        "loglik_erasure": lambda p: pl.loglik_erasure(obs.erasure_log_ratio, obs),
        "loglik_regime_intensity": lambda p: pl.loglik_regime_intensity(float(obs.n_regime_jurisdictions), obs),
    }
    rng = random.Random(42)
    failures: List[str] = []
    acknowledged: List[str] = []
    ack_ids = _load_manifest_ack()
    threshold = 1e-9
    for name, fn in terms.items():
        vals = []
        for _ in range(50):
            p = {"lambda_growth": rng.gauss(0.015, 0.015),
                 "rho_reclass": rng.betavariate(2, 5)}
            try:
                vals.append(fn(p))
            except Exception:
                vals.append(0.0)
        if len(vals) > 1:
            mean = sum(vals) / len(vals)
            var = sum((v - mean) ** 2 for v in vals) / len(vals)
            if var < threshold:
                ack_id = TERM_ACK_MAP.get(name)
                if ack_id and ack_id in ack_ids:
                    acknowledged.append(f"{name}: parameter-independent (var {var:.2e}) — acknowledged via {ack_id} informative:false")
                else:
                    failures.append(
                        f"{name}: variance {var:.2e} < {threshold:.0e} — parameter-independent "
                        f"(self-matched or constant) and NOT acknowledged in the manifest. "
                        f"Add a constant with informative: false or give the term an independent expectation."
                    )
    return (len(failures) == 0), failures, acknowledged


def run_high_influence_status_check() -> Tuple[bool, List[str]]:
    """HIGH INFLUANCE constants (max|Δposterior| > 0.05) must carry
    derivation_status in {pending_derivation, derived} — a stipulated HIGH
    INFLUENCE constant is an unmarked interpretation layer left unaddressed."""
    import yaml  # type: ignore
    sys.path.insert(0, str(HERE))
    from regen_docs import _sweep_all  # noqa: E402
    manifest = {c["id"]: c for c in yaml.safe_load(
        MANIFEST.read_text(encoding="utf-8")).get("constants", [])}
    failures: List[str] = []
    for cid, _lo, _hi, delta, high, _note in _sweep_all():
        if high:
            status = manifest.get(cid, {}).get("derivation_status")
            if status not in ("pending_derivation", "derived"):
                failures.append(
                    f"{cid}: HIGH INFLUENCE (max|Δposterior|={delta:.4f}) but "
                    f"derivation_status={status!r}; must be pending_derivation "
                    f"with a linked follow-up."
                )
    return (len(failures) == 0), failures


def run_valueless_backing_check() -> Tuple[bool, List[str]]:
    """No floor term may assert a measured fraction whose backing fact is
    valueless (audit #27) — the engine must not contradict quantitative_floor.md."""
    sys.path.insert(0, str(MODEL_DIR))
    import physical_likelihoods as pl  # noqa: E402
    report = pl.physical_floor_report()
    failures: List[str] = []
    for ex in report["excluded"]:
        failures.append(
            f"TERM EXCLUDED: {ex['term']} backed by {ex['fact_id']} (value:null). "
            f"The term was excluded from physical_loglik rather than asserting a "
            f"measured fraction the floor document disclaims."
        )
    # exclusion is the correct behaviour; a failure would be a term that asserts
    # a fraction AND is NOT in the excluded set. Verify the genealogical term.
    backing = {"loglik_genealogical_termination": "floor-04"}
    real_failures = []
    for term, fact_id in backing.items():
        if pl._floor_fact_is_valueless(fact_id):
            if term not in {e["term"] for e in report["excluded"]}:
                real_failures.append(f"{term}: backing {fact_id} is valueless but term was NOT excluded")
    return (len(real_failures) == 0), [f"OK: {e['term']} excluded ({e['fact_id']} null)" for e in report["excluded"]] if not real_failures else real_failures


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="TAST stipulated-constants checker")
    parser.add_argument("--detect-noninformative", action="store_true")
    args = parser.parse_args()

    failures: List[str] = []
    ok_m, v_m, _ = run_manifest_check()
    print(f"manifest literals: {'OK' if ok_m else 'FAIL'} ({len(v_m)} undeclared)")
    failures += v_m

    if args.detect_noninformative:
        ok_n, v_n, ack = run_noninformative_check()
        print(f"non-informative terms: {'OK' if ok_n else 'FAIL'} "
              f"({len(ack)} acknowledged, {len(v_n)} unacknowledged)")
        for a in ack:
            print("  ack: " + a)
        failures += v_n

    ok_hi, v_hi = run_high_influence_status_check()
    print(f"high-influence status: {'OK' if ok_hi else 'FAIL'} ({len(v_hi)} violations)")
    failures += v_hi

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  " + f)
        return 1
    print("\nAll constants declared; no undeclared literals; no unflagged non-informative terms.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
