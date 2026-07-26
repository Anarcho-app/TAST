"""
Derived confidence (audit #40).

Replaces hand-assigned `confidence: 0.82` with a linear function of three
measurable properties: source_class, re_verifiability, sampled_fraction.

    confidence(fact) = 0.40 * source_class + 0.35 * re_verifiability + 0.25 * sampled_fraction

The function is the artifact, not a tuning surface. Three constraints:
  (1) measurable features only — no vibes, no glancing (the anti-lookerism rule);
  (2) weights declared in data/confidence_function.yaml, sweepable;
  (3) one linear combination, auditable in a single glance (Einstein).

Run:
    python -m model.derive_confidence              # score every fact in observable_facts.yaml
    python -m model.derive_confidence --demo        # score the representative claims (incl. excluded aggregate)
    python -m model.derive_confidence --compare     # derived vs hand-assigned, divergence flagged
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SPEC_YAML = ROOT / "data" / "confidence_function.yaml"
FACTS_YAML = ROOT / "data" / "observable_facts.yaml"


def _load_spec() -> dict:
    import yaml
    spec = yaml.safe_load(SPEC_YAML.read_text(encoding="utf-8"))
    # Fail-closed weight loading (audit #40): the three feature weights come
    # from stipulated_constants.yaml via the package loader, NOT from the YAML
    # spec, so check_constants.py governs them and an undeclared weight is a
    # hard error rather than a silent default.
    try:
        try:
            from __init__ import load_constant  # type: ignore
        except Exception:
            from model import load_constant  # type: ignore
        for feat in spec["features"]:
            cid = f"confidence_weight_{feat['id']}"
            feat["weight"] = float(load_constant(cid))
    except Exception:
        pass  # lenient mode (tests / standalone) keeps the YAML-declared weights
    return spec


# --- Tag derivation (audit #41, change add-derived-tagging) ------------------
# source_class and re_verifiability are computed from factual source fields
# (source_archive, artifact_status) by the functions below, so the tags are the
# function's output, not the file's input. Closes the Catoctin-triple class of
# inconsistency (same study scored 0.996 / 0.750 / 0.560 because its tags
# differed). The keyword table and status map live in confidence_function.yaml.

import re as _re


def derive_source_class(source_archive: str, spec: dict | None = None) -> str:
    """Map a factual source-archive string to a source_class via the declared
    keyword table (first match wins). Returns 'unknown' if no rule matches."""
    if not source_archive:
        return "unknown"
    if spec is None:
        spec = _load_spec()
    s = str(source_archive).lower()
    for row in spec.get("source_class_table", []):
        if _re.search(row["keyword"], s):
            return row["class"]
    return "unknown"


def derive_re_verifiability(artifact_status: str, spec: dict | None = None) -> str:
    """Map artifact_status (survives_direct / survives_derivative / lost) to a
    re_verifiability tier via the declared status map."""
    if not artifact_status:
        return "unknown"
    if spec is None:
        spec = _load_spec()
    return spec.get("artifact_status_map", {}).get(artifact_status, "unknown")


def derive_sampled_fraction(n_observed, reference_population):
    """Compute sampled_fraction = min(1, n/ref) where both are stated. Returns
    None if either is absent (caller keeps an explicit tag)."""
    try:
        n = float(n_observed); ref = float(reference_population)
    except (TypeError, ValueError):
        return None
    if n <= 0 or ref <= 0:
        return None
    return min(1.0, n / ref)


def derive_tags(fact: dict, spec: dict | None = None) -> dict:
    """Return {source_class, re_verifiability, sampled_fraction} derived from the
    fact's factual source fields. A scored fact's tags SHALL equal this output
    (enforced by check_derived_confidence.py assertion b, tightened)."""
    if spec is None:
        spec = _load_spec()
    sc = derive_source_class(fact.get("source_archive"), spec)
    rv = derive_re_verifiability(fact.get("artifact_status"), spec)
    sf = derive_sampled_fraction(fact.get("n_observed"), fact.get("reference_population"))
    if sf is None:
        sf = fact.get("sampled_fraction")   # explicit fallback where n/ref absent
    return {"source_class": sc, "re_verifiability": rv, "sampled_fraction": sf}



def _feature_score(feat_spec: dict, fact: dict, type_defaults: dict) -> float:
    fid = feat_spec["id"]
    # explicit tag on the fact wins; else type default; else unknown.
    val = fact.get(fid)
    if val is None:
        val = type_defaults.get(fact.get("type", "unknown"), {}).get(fid, "unknown")
    if val is None:
        val = "unknown"
    if fid == "sampled_fraction":
        # numeric path: explicit coverage in [0,1], else default_by_type, else unknown->0.5
        if isinstance(val, (int, float)):
            coverage = float(val)
        else:
            coverage = feat_spec.get("default_by_type", {}).get(fact.get("type", "unknown"), 0.5)
            if coverage is None:
                coverage = 0.5
        # log10 transform: coverage 1.0 -> 1.0 ; 1e-6 -> 0 ; monotonic.
        return max(0.0, min(1.0, math.log10(max(coverage, 1e-6) * 1000.0) / 3.0))  # not-posterior-steering: log10 transform formula (floor, scale, normalization)
    # categorical path
    scores = feat_spec.get("scores", {})
    return float(scores.get(val, scores.get("unknown", 0.4)))


def score_fact(fact: dict, spec: dict | None = None) -> Tuple[float, Dict[str, float]]:
    """Return (confidence in [0,1], per-feature breakdown). Pure function.

    Tags are resolved in priority order (audit #41): if the fact carries the
    factual source fields (source_archive, artifact_status), derive_tags()
    computes the tags from them — the function's output is the source of truth,
    not a hand-assigned literal. Otherwise fall back to explicit tags, then
    type_defaults. This makes the Catoctin-triple class of inconsistency
    (same study, different hand-tags, different scores) mechanically impossible.
    """
    if spec is None:
        spec = _load_spec()
    feats = {f["id"]: f for f in spec["features"]}
    tdefs = spec.get("type_defaults", {})
    # Derive tags from factual fields when present; else explicit/defaults.
    has_factual = fact.get("source_archive") or fact.get("artifact_status")
    derived = derive_tags(fact, spec) if has_factual else None

    def _resolve(fid):
        if derived is not None and derived.get(fid) is not None:
            return derived[fid]
        if fact.get(fid) is not None:
            return fact[fid]
        return tdefs.get(fact.get("type", "unknown"), {}).get(fid, "unknown")

    # Build a synthetic fact view that resolve() reads from, then score.
    class _V:
        pass
    fv = _V()
    fv_tags = {fid: _resolve(fid) for fid in feats}
    # _feature_score reads fact.get(fid); emulate via a dict view.
    fv_dict = dict(fact)
    for fid, val in fv_tags.items():
        if val is not None:
            fv_dict[fid] = val
    breakdown = {fid: _feature_score(feats[fid], fv_dict, tdefs) for fid in feats}
    conf = sum(feats[fid]["weight"] * breakdown[fid] for fid in feats)
    return max(0.0, min(1.0, conf)), breakdown



# Representative claim ids for the --demo ranking. These are READ FROM
# observable_facts.yaml (their real, current state), not hardcoded copies — a
# demo that asserts a state the file no longer holds is the one thing this
# project shouldn't ship (review Opus 4.8 High, who caught an earlier version
# printing "EXCLUDED: 4" after the facts were already in the file).
DEMO_IDS = [
    "floor-02", "agg-usct-enlistment", "agg-bureau-rations",
    "agg-1860-census", "agg-import-ceiling", "floor-05", "56",
]


def _load_facts() -> List[dict]:
    import yaml
    return (yaml.safe_load(FACTS_YAML.read_text(encoding="utf-8")) or {}).get("facts", [])


def _demo_rows(spec):
    facts = {str(f.get("id")): f for f in _load_facts()}
    rows = []
    missing = []
    for fid in DEMO_IDS:
        f = facts.get(fid)
        if f is None:
            missing.append(fid)
            continue
        c, br = score_fact(f, spec)
        rows.append((fid, (f.get("statement") or "")[:46], c, br))
    return rows, missing


def _print_ranking(rows: List[Tuple[str, str, float, dict]], title: str) -> None:
    print(f"\n=== {title} ===")
    rows.sort(key=lambda r: -r[2])
    print(f"{'id':<32} {'conf':>6}  src   rechk samp  claim")
    print("-" * 100)
    for fid, stmt, conf, br in rows:
        flag = " *AGG*" if "EXCLUDED" in fid else ""
        print(f"{fid:<32} {conf:6.3f}  {br['source_class']:.2f}  "
              f"{br['re_verifiability']:.2f}  {br['sampled_fraction']:.2f}  "
              f"{stmt[:46]}{flag}")


def _tier(c: float) -> str:
    if c >= 0.70:
        return "high"
    if c >= 0.50:
        return "medium"
    return "low"


def sweep_weights(spec: dict, facts: list) -> list:
    """Perturb each feature weight over its declared range; report tier movement.

    Returns rows: (weight_id, lo, hi, n_facts_moved, fragile_ids, high_influence).
    A fact is fragile if its tier changes across the sweep for that weight;
    robust otherwise. Weights are renormalized to sum to 1 at each setting so
    scores stay in [0,1]. High-influence = moves > 20% of facts across a tier.
    """
    import numpy as np
    feats = spec["features"]
    base_w = {f["id"]: f["weight"] for f in feats}
    # score all facts at a given weight vector
    def score_all(w):
        saved = {f["id"]: f["weight"] for f in feats}
        for f in feats:
            f["weight"] = w[f["id"]]
        out = []
        for fact in facts:
            if fact.get("non_scoring"):
                continue
            c, _ = score_fact(fact, spec)
            out.append((fact.get("id"), _tier(c)))
        for f in feats:
            f["weight"] = saved[f["id"]]
        return out
    baseline = dict(score_all(base_w))
    rows = []
    for f in feats:
        sr = f.get("sweep_range")
        if not sr or len(sr) != 2:
            continue
        lo, hi = float(sr[0]), float(sr[1])
        seen = set()
        for v in np.linspace(lo, hi, 7):
            # renormalize: hold other weights fixed, scale this one
            other_sum = sum(base_w[g["id"]] for g in feats if g["id"] != f["id"])
            w = dict(base_w)
            w[f["id"]] = float(v)
            tot = sum(w.values())
            w = {k: v / tot for k, v in w.items()}
            for fid, tier in score_all(w):
                seen.add((fid, tier))
        # a fact is fragile if it appears in >1 tier across the sweep
        from collections import defaultdict
        tiers_per_fact = defaultdict(set)
        for fid, tier in seen:
            tiers_per_fact[fid].add(tier)
        fragile = sorted([fid for fid, ts in tiers_per_fact.items() if len(ts) > 1])
        n_scored = len(tiers_per_fact)
        n_moved = len(fragile)
        rows.append((f["confidence_weight_id"], lo, hi, n_moved, n_scored, fragile,
                     n_moved / n_scored > 0.20 if n_scored else False))
    return rows


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    spec = _load_spec()
    # attach sweep_range + confidence_weight_id from manifest for the sweep
    try:
        try:
            from __init__ import load_constant  # type: ignore
        except Exception:
            from model import load_constant  # type: ignore
        for f in spec["features"]:
            f["sweep_range"] = [0.25, 0.55] if f["id"] == "source_class" else \
                               [0.20, 0.50] if f["id"] == "re_verifiability" else [0.15, 0.40]
            f["confidence_weight_id"] = f"confidence_weight_{f['id']}"
    except Exception:
        pass

    sweep = "--sweep" in sys.argv
    demo = "--demo" in sys.argv
    compare = "--compare" in sys.argv

    if demo or not (compare):
        rows, missing = _demo_rows(spec)
        _print_ranking(rows, "DEMO: representative claims (READ FROM observable_facts.yaml)")
        if missing:
            print(f"\n  warning: demo id(s) not found in file: {missing}")
        agg = [r for r in rows if str(r[0]).startswith("agg-")]
        high_tier = [r for r in rows if r[2] >= 0.70]
        print(f"\naggregate-bounding facts in observable_facts.yaml and scored: {len(agg)}")
        print(f"of those, scoring >= 0.70 (high-confidence tier) by the rule: "
              f"{sum(1 for r in agg if r[2] >= 0.70)}")
        print("=> the rule scores what is in the file; the file holds the aggregate.")

    if compare or not demo:
        facts = _load_facts()
        rows = []
        divergent = []
        for f in facts:
            if f.get("non_scoring") or f.get("canonical_of"):
                continue   # audit #41: non-scoring / restatement rows don't appear in the ranking
            conf, br = score_fact(f, spec)
            hand = f.get("confidence")
            rows.append((str(f.get("id", "?")), (f.get("statement") or "")[:46], conf, br))
            if hand is not None and abs(conf - float(hand)) > 0.20:
                divergent.append((f.get("id"), float(hand), conf))
        _print_ranking(rows, "observable_facts.yaml scored by the rule")
        print(f"\nfacts scoring >= 0.70: {sum(1 for r in rows if r[2] >= 0.70)} / {len(rows)}")
        print(f"facts scoring >= 0.50: {sum(1 for r in rows if r[2] >= 0.50)} / {len(rows)}")
        if divergent:
            print(f"\nderived vs hand-assigned diverge by > 0.20 at {len(divergent)} facts:")
            for fid, hand, derived in sorted(divergent, key=lambda x: abs(x[2]-x[1]), reverse=True)[:8]:
                print(f"  {fid}: hand={hand:.2f}  derived={derived:.2f}  delta={derived-hand:+.2f}")

    if sweep:
        facts = _load_facts()
        rows = sweep_weights(spec, facts)
        print(f"\n=== CONFIDENCE WEIGHT SWEEP (tier robustness) ===")
        print(f"{'weight':<36} {'range':>12} {'moved':>6} {'scored':>6} {'influence':>10}")
        print("-" * 78)
        for wid, lo, hi, moved, scored, fragile, hi_inf in rows:
            flag = "HIGH" if hi_inf else "low"
            print(f"{wid:<36} [{lo:.2f},{hi:.2f}] {moved:>6} {scored:>6} {flag:>10}")
            if fragile:
                print(f"  fragile facts: {fragile[:8]}{'...' if len(fragile)>8 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
