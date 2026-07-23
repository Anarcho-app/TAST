# TAST Demographic Model — Skepticism-First Edition (v4.0)

**All large-scale numerical estimates of the enslaved population in the territory that became the United States are reconstructions from records produced by the trading and slaveholding societies. Those records are biased sources (victors' paperwork). Estimates calculated from them are conditional estimates — never facts. No amount of correction, cross-checking, or “least-bad” framing changes this.**

This repository does not claim to escape that constraint. The focal population is multi-generational American lineages of African and mixed ancestry (Freedmen’s Bureau-era and earlier U.S. lineages). Continental-African framing is not the unmarked identity label for this group. It only shows what happens when those same records are re-weighted, and what remains when they are set aside.

This is a living, layered empirical engine for analyzing the demographic history of people of African and mixed descent in the United States, with explicit focus on Freedmen’s Bureau-era lineages (FBA) and multi-generational American rootedness.

## Core Design Principles (v4.0)

1. **Zero-Weight / Maximal-Skepticism Mode**  
   A single parameter (`victors_reliability ∈ [0.0, 1.0]`) scales the trust placed in every census total, shipping manifest, plantation ledger, and administrative count.  
   - At `1.0`: conventional + reweighted Bayesian posteriors are computed as before.  
   - At `0.0`: all quantitative head-counts, growth rates, and import totals become *undefined / unknowable*. Only qualitative patterns survive (existence of forced labor regimes, multi-generational presence of people of African and mixed descent on American soil, family separation practices, burial evidence, etc.).

2. **Strict Layer Separation**
   - `raw/` — Verbatim excerpts or links to primary documents, each tagged with provenance (owner-mediated, multi-national shipping, archaeological, oral/community, etc.).
   - `conventional/` — Standard reconstructions (SlaveVoyages, Hacker, census aggregates) with their explicit assumptions listed.
   - `reweighted/` — Bayesian evidence streams, priors, and posteriors under varying reliability.
   - `surviving/` — Statements that remain after quantitative records are discarded or set to near-zero reliability.

3. **Conditioned Language**  
   Every numerical claim is prefixed:  
   > “If we treat the recorded population totals as approximately accurate (victors_reliability ≈ 1.0), then …; if we do not, the quantitative claim is undefined.”

4. **Python Core as Center**  
   The Bayesian skeleton lives in `model/`. A CLI and notebook expose a single reliability slider so users can dial skepticism from 0.0 → 1.0 and watch both conventional and alternative claims appear or vanish.

5. **Non-Quantitative Evidence Treated as Primary**  
   Burial grounds, genealogical termination patterns, oral/community testimony, and physical remains are elevated. They support qualitative claims of multi-generational American presence; they do **not** underwrite precise head-counts or growth rates.

6. **Versioned Skepticism**  
   Changes to reliability assumptions are tagged releases with clear diffs of every affected claim.

## Quick Start

```bash
cd model
python -m bayesian_core --reliability 0.0   # maximal skepticism: only qualitative survives
python -m bayesian_core --reliability 1.0   # full quantitative mode
python -m bayesian_core --reliability 0.3   # intermediate
```

Or open `notebooks/reliability_slider.ipynb`.

## Current Expansion Status (2026-07-23)

- Full 155-claim Sources Master Registry extracted → `data/sources_registry.csv`
- `raw/` expanded with 8 key primary-source files (census, SlaveVoyages, WPA, burial grounds, classification laws, etc.)
- Original monolithic files retained under `reweighted/` for reference
- Python reliability slider remains the center of the model

## Directory Map

```
tast-skepticism-v4.0/
├── README.md                 # this file
├── model/
│   ├── bayesian_core.py      # core engine + CLI
│   └── evidence_streams.csv  # likelihood table
├── data/
│   └── (supporting CSVs)
├── raw/                      # primary-document excerpts + provenance tags
├── conventional/             # standard numerical reconstructions + assumptions
├── reweighted/               # Bayesian streams & posteriors
├── surviving/                # qualitative claims that survive zero-weight
└── notebooks/
    └── reliability_slider.ipynb
```

## Provenance Audit (inherited & expanded)

Even in high-reliability mode, the majority of quantifiable demographic claims rest on owner-, trader-, or enumerator-mediated records. The living structure makes this absence visible rather than papering over it.

## Version

- **v4.0** (2026-07-23): First skepticism-first restructuring. Zero-weight mode, strict layer separation, conditioned language, Python core centered, non-quantitative primary.
- Prior versions (v2.x–v3.0) remain in the original monolithic .txt files for reference.

---

*This repository is a tool for epistemic hygiene, not a competing origin narrative.*
