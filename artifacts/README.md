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
| `01_continuous_harm_declaration_cba.md` | Continuous Harm, Declaration Legitimacy, and Collective Cost-Benefit Framework | Offered for evaluation (2026-08-04); legislative-ready v1.0 |
| `01_staffer_brief.md` | Artifact 01 — Staffer Brief (parallel 3–5 page companion) | Offered for evaluation (2026-08-04) |

## Legislative Readiness Checklist v1.0

Proposed by Grok 4.5 Expert (xAI), adopted 2026-08-04. Every future artifact aimed
at executive or legislative audiences must satisfy this checklist before it is
marked legislative-ready. Version the checklist in any future revision.

- [ ] **One-page executive summary** at the top — plain language, no formulas.
- [ ] **One-page decision matrix** — "if you accept Premise 1, the choice is between Path A and Path B" — with the break-even condition in one sentence.
- [ ] **Fiscal scorekeeping appendix** in CBO/JCT/appropriations vocabulary: NPV scenarios mapped onto baseline vs. alternative baselines; illustrative **10-year budget windows** alongside long-horizon figures; every model-dependent number flagged with its sweep band.
- [ ] **Implementation levers as a modular menu** (classification opt-out / "human" default; time-limited pilots with sunset clauses; state/local experiments with transparent dashboards; investments scored against reciprocal fiscal returns) — members can carry one lever without owning the whole framework.
- [ ] **Parallel staffer brief (3–5 pages)**: opens with the physical-floor observables (hardest to dismiss); states the Declaration binary neutrally; presents only baseline + inaction scenarios with "what would have to be true" sensitivity notes; ends with questions for legislative counsel / scorekeepers.
- [ ] **Explicit bipartisan compatibility language** that does not water down the logic.
- [ ] **Photocopy-durable visuals**: one clean scenario-comparison table; a simple decision-tree graphic for the Declaration binary; a short list of the highest-confidence physical anchors with confidence scores derived from the TAST confidence function.
- [ ] **Grounding appendix** mapping observables to registered TAST claims; unregistered items flagged as registry candidates.
- [ ] **Conditionality statement** present; banned-phrase lint clean.
