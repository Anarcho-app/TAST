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
