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

    # (b) no scored fact resolves a feature via type_defaults fallback AND (audit #41)
    # every scored fact carries the factual source fields (source_archive,
    # artifact_status) from which derive_tags() computes its tags. No scored fact
    # carries a hand-assigned source_class/re_verifiability literal — those are
    # the function's output now, not the file's input. A tag is "derived" (not
    # fallback) when source_archive/artifact_status are present; type_defaults
    # apply only when those factual fields are absent.
    fallback = []
    missing_factual = []
    hand_tags = []
    for f in facts:
        if not _is_scored(f):
            continue
        has_factual = bool(f.get("source_archive")) and bool(f.get("artifact_status"))
        if not has_factual:
            # only here can type_defaults fire; that is the fallback failure
            for feat in ("source_class", "re_verifiability"):
                if _feature_resolves_via_default(f, feat, spec):
                    fallback.append((f.get("id"), feat))
        if not f.get("source_archive") or not f.get("artifact_status"):
            missing_factual.append((f.get("id"), bool(f.get("source_archive")), bool(f.get("artifact_status"))))
        for tag in ("source_class", "re_verifiability"):
            if tag in f:
                hand_tags.append((f.get("id"), tag))
    if fallback:
        failures.append(
            f"(b) {len(fallback)} scored fact(s) resolve a feature via type_defaults "
            f"fallback (must carry source_archive/artifact_status so tags derive): {fallback[:5]}"
        )
    if missing_factual:
        failures.append(
            f"(b)[#41] {len(missing_factual)} scored fact(s) missing source_archive/artifact_status "
            f"(tags cannot be derived): {missing_factual[:5]}"
        )
    if hand_tags:
        failures.append(
            f"(b)[#41] {len(hand_tags)} scored fact(s) carry a hand-assigned source_class/re_verifiability "
            f"literal (tags are derived by derive_tags, not hand-assigned): {hand_tags[:5]}"
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

    # (d) no administrative / aggregate-role fact hides in non_scoring. The four
    # pinned agg-* facts are covered by (c), but a future asymmetry could be
    # smuggled in by marking an administrative_process or aggregate_role fact
    # non_scoring. Flag any such case so the escape hatch is visible (review
    # Opus 4.8 High, who noted 44/73 facts are non_scoring and unconstrained).
    hidden = []
    for f in facts:
        if not _is_scored(f):
            t = f.get("type", "")
            role = f.get("aggregate_role", "")
            if t == "administrative_process" or role:
                hidden.append((f.get("id"), t, role))
    if hidden:
        failures.append(
            f"(d) {len(hidden)} administrative/aggregate fact(s) marked non_scoring "
            f"(the new escape hatch): {hidden[:5]}. Either score them or document "
            f"why they are genuinely non-scoring context."
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
