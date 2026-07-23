# Versioned Skepticism Log

## v4.0 — 2026-07-23

**Change type**: Structural + epistemic.

- Introduced explicit `victors_reliability` parameter (0.0–1.0).
- At reliability ≈ 0.0 every quantitative head-count, growth rate, and import total is declared UNDEFINED; only qualitative / physical / meta claims survive.
- Strict four-layer separation: `raw/`, `conventional/`, `reweighted/`, `surviving/`.
- Converted from monolithic .txt to Markdown + CSV + runnable Python package.
- All numerical claims now require the conditioning prefix.
- Python core moved to center; CLI + notebook expose the reliability slider.
- Non-quantitative evidence (burial, genealogy termination, structural silence) elevated to primary status in the surviving layer.
- Original v3.0 monolithic files retained under `reweighted/` for reference.

**Diff impact**:  
- Posteriors at reliability=1.0 remain H5-dominant (as in v3.0).  
- At reliability=0.0 the entire quantitative apparatus collapses by design.  
- No new primary sources added; reorganization only.

## Prior (monolithic)

- v3.0 / v2.6.x — living document with 26 streams, 155 claims, H5 ≈ 70–88 % under full reliability.

## v4.1 — 2026-07-23 (same day expansion)

- Extracted full Appendix A Sources Master Registry (155 claims) into `data/sources_registry.csv`.
- Expanded `raw/` with 5 additional primary-source files:
  - 04_us_census_slave_schedules.md
  - 05_slavevoyages.md
  - 06_wpa_slave_narratives.md
  - 07_african_burial_ground_nps.md
  - 08_classification_and_paper_ethnocide.md
- Updated layer READMEs.
- Original full document remains the authoritative backup under `reweighted/`.

## v4.2 — 2026-07-23

Addressed structural critiques:

- Surviving claims are now **loaded from** `surviving/qualitative_claims.md` (no longer hard-coded).
- Surviving list cleaned: removed residual dependence on the U.S.–Caribbean numerical growth differential.
- `load_streams()` now validates required columns, types, and likelihood ranges [0,1]; raises `StreamLoadError` on malformed input.
- Added `--self-test` mode covering load, reliability extremes, posterior normalization, surviving load, and prior sum.
- Explicit note in output that stream independence is assumed (known limitation).
- Added `CONTRIBUTING.md`.

Still open (not yet addressed):
- Stream independence / correlated likelihoods
- Monte-Carlo or hierarchical uncertainty
- Full verbatim primary-source tables in raw/
- Continuous integration / external validation
- Multi-axis adversarial sensitivity beyond the single reliability parameter

## v4.3 — 2026-07-23

Language and epistemic hardening (response to external review):

- **Ban on fact-conversion language**: “least-bad”, “best available”, “robust after correction”, “historical consensus”, and equivalents are forbidden under `--strict` (default on).
- Every quantitative output path now prints the required disclaimer:
  `CONDITIONAL ESTIMATE derived from biased administrative records (victors' paperwork). This is NOT A FACT.`
- Surviving layer gains explicit meta-claim 11: no national-scale total derived from the administrative records constitutes a fact; “least-bad” designation does not convert estimates into facts.
- `--self-test` extended to verify banned-phrase detection and presence of the disclaimer constant.
- CONTRIBUTING.md updated with rejection criteria for any contribution that restores factual status to biased-source estimates.
- Core rule stated in module docstring and CLI banner.

Still open:
- Stream independence / correlated likelihoods
- Monte-Carlo sampling over bias magnitudes
- Formal functional dependence N = f(C_t, I, r) published as a first-class object
- Full verbatim primary-source tables
- Continuous integration / external validation
- Multi-axis adversarial sensitivity
