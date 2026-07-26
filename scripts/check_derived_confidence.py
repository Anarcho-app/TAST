#!/usr/bin/env python3
"""
TAST Derived-Confidence Symmetry Gate (audit #40, change add-derived-confidence).

Three assertions that prevent the hand-exclusion asymmetry from recurring:

  (a) no scored fact carries a hand-assigned `confidence:` literal
  (b) no scored fact resolves a feature via the type_defaults fallback
  (c) no scored-fact class is categorically excluded (the four aggregate-bounding
      facts must be present and scored)

The gate asserts the RULE was applied, not any particular outcome. A rigged
result would require rigging the function (one swept file), not the gate.

    python TAST/scripts/check_derived_confidence.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAST_ROOT = HERE.parent
MODEL_DIR = TAST_ROOT / "model"
FACTS_YAML = TAST_ROOT / "data" / "observable_facts.yaml"

# The aggregate-bounding fact ids that the asymmetry critique identified as
# wrongly excluded. Their presence is the symmetry guarantee.
REQUIRED_AGGREGATE_IDS = {
    "agg-usct-enlistment",
    "agg-bureau-rations",
    "agg-import-ceiling",
    "agg-1860-census",
}


def _is_scored(fact: dict) -> bool:
    """A fact is scored if it is not marked non_scoring."""
    return not fact.get("non_scoring")


def _feature_resolves_via_default(fact: dict, feature: str, spec: dict) -> bool:
    """True if the feature would resolve from type_defaults rather than the fact's own tag."""
    if fact.get(feature) is not None:
        return False
    tdef = spec.get("type_defaults", {}).get(fact.get("type", "unknown"), {})
    return feature in tdef


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.path.insert(0, str(MODEL_DIR))
    import yaml  # noqa: E402
    import derive_confidence as dc  # noqa: E402

    spec = dc._load_spec()
    facts = yaml.safe_load(FACTS_YAML.read_text(encoding="utf-8"))["facts"]
    by_id = {str(f.get("id")): f for f in facts}

    failures = []

    # (a) no scored fact carries a hand-assigned confidence literal
    hand_confidence = [str(f.get("id")) for f in facts
                       if _is_scored(f) and f.get("confidence") is not None]
    if hand_confidence:
        failures.append(
            f"(a) {len(hand_confidence)} scored fact(s) still carry a hand-assigned "
            f"`confidence:` literal: {hand_confidence[:5]}{'...' if len(hand_confidence)>5 else ''}. "
            f"Tag measurable properties instead; confidence is derived."
        )

    # (b) no scored fact resolves a feature via type_defaults fallback
    fallback = []
    for f in facts:
        if not _is_scored(f):
            continue
        for feat in ("source_class", "re_verifiability"):
            if _feature_resolves_via_default(f, feat, spec):
                fallback.append((f.get("id"), feat))
    if fallback:
        failures.append(
            f"(b) {len(fallback)} scored fact(s) resolve a feature via type_defaults "
            f"fallback (must carry explicit tags): {fallback[:5]}"
        )

    # (c) the four aggregate-bounding facts are present and scored
    missing = REQUIRED_AGGREGATE_IDS - set(by_id)
    if missing:
        failures.append(
            f"(c) aggregate-bounding fact(s) missing from observable_facts.yaml: "
            f"{sorted(missing)}. Category-based exclusion is a build failure."
        )
    excluded = [rid for rid in REQUIRED_AGGREGATE_IDS
                if rid in by_id and not _is_scored(by_id[rid])]
    if excluded:
        failures.append(
            f"(c) aggregate-bounding fact(s) present but marked non_scoring: "
            f"{excluded}. They must be scored by the same rule as presence facts."
        )

    if failures:
        print("derived-confidence symmetry: FAIL")
        for f in failures:
            print("  " + f)
        return 1
    scored_n = sum(1 for f in facts if _is_scored(f))
    print(f"derived-confidence symmetry: OK")
    print(f"  scored facts: {scored_n} / {len(facts)}")
    print(f"  aggregate-bounding facts present & scored: {len(REQUIRED_AGGREGATE_IDS)} / {len(REQUIRED_AGGREGATE_IDS)}")
    print(f"  no hand-assigned confidence on scored facts; no type_default fallback; no categorical exclusion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
