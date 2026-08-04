# Artifacts Layer — Downstream Syntheses

An *artifact* is a self-contained synthesis document built **on top of** the TAST
layers, for audiences beyond the model itself (executive, legislative, and
general readership). Artifacts are **outputs, not inputs**:

- Nothing in this layer feeds `model/evidence_streams.csv`,
  `data/observable_facts.yaml`, `data/stipulated_constants.yaml`, or the
  H1–H5 mechanism ranking. An artifact cannot move a posterior.
- An artifact's observables must either trace to registered TAST evidence
  (`data/sources_registry_with_ci.csv`, `data/observable_facts.yaml`,
  `surviving/`) or be explicitly flagged as **unregistered** (candidate for
  future registry expansion).
- Every quantitative claim in an artifact remains conditional and
  sensitivity-declared, in TAST style: administrative magnitudes are
  conditional on `victors_reliability`; the physical/structural floor carries
  priority; model-dependent magnitudes are swept under hierarchical priors
  rather than asserted.
- The repo-wide language discipline (`scripts/check_banned_phrases.py`)
  applies to this layer without exemption.

## Orientation

This layer exists to support **reparative resolution** of the damage done by
state-imposed racial classification. The classification machinery itself is
treated as the injury; biological race is not affirmed anywhere in the layer.

Consistent with the main README ("Consumer ancestry methods: narrow
evidentiary use") and `dna_sample_size_discipline.md`, TAST does **not** cater
to PCA-style or consumer-ancestry outputs in this layer: those outputs are
panel-relative, model-dependent comparisons to selected reference samples — not
readings of historical identity — and they are not the reparative channel.

## Current artifacts

| File | Title | Status |
|------|-------|--------|
| `01_continuous_harm_declaration_cba.md` | Continuous Harm, Declaration Legitimacy, and Collective Cost-Benefit Framework | Offered for evaluation (2026-08-04); legislative-ready v1.1 (compliance record below) |
| `01_staffer_brief.md` | Artifact 01 — Staffer Brief (parallel 3–5 page companion) | Offered for evaluation (2026-08-04); part of the v1.1 compliance record |

## Compliance record — Artifact 01 vs. Checklist v1.1 (verified 2026-08-04)

The checklist above is the standing requirement for future artifacts; this record
shows Artifact 01's item-by-item completion against it. Future artifacts get their
own record in this section when marked legislative-ready.

| # | Checklist item (v1.1) | Satisfied in | Status |
|---|---|---|---|
| 1 | One-page executive summary (plain language, no formulas) | Artifact 01 — "Executive Summary (Plain Language, One Page)" | ✓ |
| 2 | One-page decision matrix + break-even in one sentence | Artifact 01 — "Decision Matrix (One Page)" | ✓ |
| 3 | Fiscal scorekeeping appendix (CBO/JCT vocabulary; 10-year window; model-dependent flags with sweep bands) | Artifact 01 — Appendix B | ✓ |
| 4 | Implementation levers as a modular menu | Artifact 01 — Section 5 lever menu | ✓ |
| 5 | Operational notes per lever (administrator, scale/phase-in, sunset trigger, TAST-tied metrics, funding character) | Artifact 01 — Section 5, levers 1–4 | ✓ |
| 6 | Implementation & evaluation subsection (inaction-baseline scoring, no-double-count tracking, underperformance path) | Artifact 01 — Section 5 "Implementation & evaluation" | ✓ |
| 7 | Cost-benefit packaging: 10-year primary / 50-year secondary, inline sensitivity bands, plain-English assumption sentence per scenario | Staffer brief — Section 4; Artifact 01 — Section 4 assumption check | ✓ |
| 8 | Path B residual clarification (logical residual, not a recommendation) | Artifact 01 §3 Path B; Staffer brief §3 | ✓ |
| 9 | Parallel staffer brief (3–5 pages; physical floor first; neutral binary; baseline + inaction only; counsel/scorekeeper questions) | `01_staffer_brief.md` (1,323 words) | ✓ |
| 10 | Explicit bipartisan compatibility language without dilution | Artifact 01 — Section 1 "Bipartisan compatibility" | ✓ |
| 11 | Photocopy-durable visuals (scenario table, decision tree, anchor table with derived confidence) | Artifact 01 — Decision Matrix section (table + ASCII tree + anchor table) | ✓ |
| 12 | Grounding appendix; unregistered items in a clearly labeled candidates list | Artifact 01 — Appendix A (14 registered anchors; "Candidates for future registry") | ✓ |
| 13 | Conditionality statement present; banned-phrase lint clean | Artifact 01 — Appendix A conditionality statement; lint green 2026-08-04 | ✓ |

Gate evidence for items 12–13: `check_artifact_grounding.py` (23 citations, 0 phantoms),
`check_npv_arithmetic.py` (20 values, 0 drift), `check_observable_facts_parity.py`
(29 values, 0 drift), `check_banned_phrases.py` (0 violations) — all re-run 2026-08-04.

## Legislative Readiness Checklist v1.1

v1.0 proposed by Grok 4.5 Expert (xAI), adopted 2026-08-04. v1.1 (same date) adds
Grok 4.5 Expert's round-2 operational repairs. Every future artifact aimed at
executive or legislative audiences must satisfy this checklist before it is
marked legislative-ready. Version the checklist in any future revision.

- [ ] **One-page executive summary** at the top — plain language, no formulas.
- [ ] **One-page decision matrix** — "if you accept Premise 1, the choice is between Path A and Path B" — with the break-even condition in one sentence.
- [ ] **Fiscal scorekeeping appendix** in CBO/JCT/appropriations vocabulary: NPV scenarios mapped onto baseline vs. alternative baselines; illustrative **10-year budget windows** alongside long-horizon figures; every model-dependent number flagged with its sweep band.
- [ ] **Implementation levers as a modular menu** (classification opt-out / "human" default; time-limited pilots with sunset clauses; state/local experiments with transparent dashboards; investments scored against reciprocal fiscal returns) — members can carry one lever without owning the whole framework.
- [ ] **Operational notes per lever (v1.1)**: who administers it; rough scale / phase-in (pilot → evaluation → optional expansion); sunset or evaluation trigger; success metrics tied to physical-floor or disparity data already in TAST; one sentence on funding character (discretionary / mandatory / tax expenditure).
- [ ] **Implementation & evaluation subsection (v1.1)**: how pilots score against the inaction baseline (not a zero-cost status quo); how reciprocal fiscal returns are tracked channel-by-channel without double-counting; the underperformance path (automatic sunset or one redesign re-entry).
- [ ] **Cost-benefit packaging for legislative readers (v1.1)**: 10-year window is the primary table in the staffer brief with the 50-year horizon secondary; every model-dependent number carries its sensitivity band inline; one plain-English assumption sentence per scenario ("This assumes X; if returns are only Y instead, the net becomes Z").
- [ ] **Path B residual clarification (v1.1)**: the binary states explicitly that Path B is the logical residual of sustained non-redress, not a recommendation.
- [ ] **Parallel staffer brief (3–5 pages)**: opens with the physical-floor observables (hardest to dismiss); states the Declaration binary neutrally; presents only baseline + inaction scenarios with "what would have to be true" sensitivity notes; ends with questions for legislative counsel / scorekeepers.
- [ ] **Explicit bipartisan compatibility language** that does not water down the logic.
- [ ] **Photocopy-durable visuals**: one clean scenario-comparison table; a simple decision-tree graphic for the Declaration binary; a short list of the highest-confidence physical anchors with confidence scores derived from the TAST confidence function.
- [ ] **Grounding appendix** mapping observables to registered TAST claims; unregistered items in a clearly labeled "candidates for future registry" list (flagged, not fabricated).
- [ ] **Conditionality statement** present; banned-phrase lint clean.
