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
| `01_continuous_harm_declaration_cba.md` | Continuous Harm, Declaration Legitimacy, and Collective Cost-Benefit Framework | Offered for evaluation (2026-08-04) |
