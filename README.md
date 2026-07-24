# TAST Demographic Model — Skepticism-First Edition (v4.0)

**All large-scale numerical estimates of the enslaved population in the territory that became the United States are reconstructions from records produced by the trading and slaveholding societies. Those records are biased sources (victors' paperwork). Estimates calculated from them are conditional estimates — never facts. No amount of correction, cross-checking, or “least-bad” framing changes this.**

This repository does not claim to escape that constraint. The focal population is multi-generational American lineages of African and mixed ancestry (Freedmen’s Bureau-era and earlier U.S. lineages). Continental-African framing is not the unmarked identity label for this group. It only shows what happens when those same records are re-weighted, and what remains when they are set aside.

This is a living, layered empirical engine for analyzing the demographic history of people of African and mixed descent in the United States, with explicit focus on Freedmen’s Bureau-era lineages (FBA) and multi-generational American rootedness.


## Mathematical Foundation vs. Epistemic Rule

**The inference machinery is standard Bayesian statistics.** None of the following is experimental or non-standard:

- Bayes’ theorem and the product rule
- Log-space numerical stability
- Monte Carlo sampling from a reliability (or bias) hyperparameter
- Hierarchical / weakly informative treatment of source reliability
- Poisson-style counting arguments for physical evidence (burial sites, aDNA individuals, jurisdictions)
- Beta-style concentration for rates and proportions

These are textbook tools (see classic references in `METHODS.md`).

**The novel contribution of this project is the epistemic rule, not the mathematics:**

- A continuous `victors_reliability` parameter applied to administrative records produced by trading and slaveholding societies
- The explicit zero-weight collapse: when that reliability approaches zero, every quantitative head-count, growth rate, and import total derived from those records becomes **UNDEFINED**
- The physical and structural evidence floor (burial grounds, aDNA remains, genealogical termination patterns, structural silence, regime intensity) is the only quantitative layer that remains
- Language discipline that forbids converting “least-bad / best-available / historical consensus” into “fact”

The project does **not** claim to replace any national administrative total.  
It makes the conditionality of every such total unavoidable.

The known knowns (physical remains on American soil, genealogical chains terminating in U.S. records, anti-literacy laws, owner-mediated provenance) are not experimental.  
The decision to treat those known knowns as the floor and the administrative series as optionally discardable is the point of the project.



## Evidence over narrative

Slaveowners’ documents, shipping manifests, and other victors’ accounts are valuable primary sources. They are also incomplete and self-interested.  

This project treats them as **data for critical analysis**, not as an unassailable foundation and not as targets for automatic rejection.  

Bayesian updating (via the continuous `victors_reliability` parameter) weighs their reliability without favoritism. When reliability is high, the administrative series inform the posterior; when reliability approaches zero, those series become non-informative and only the physical and structural floor remains.  

Cross-checks against economics, demography, archaeology, genealogy, and logic are required. That is how understanding grows. Narrative preference — on any side — is not a substitute for evidence.


## How to evaluate this project

Evaluate TAST on its stated terms. The following distinction is load-bearing.

### Valid axes of critique

- Independence assumption among evidence streams (explicitly flagged as a limitation).
- Remaining hand-specified point likelihoods in `evidence_streams.csv` (conversion to data-level terms is active work).
- Need for fuller prior/posterior predictive checks.
- Need for external validation, adversarial re-analysis, and comparison against independent physical or genealogical series.
- Scope and density of the physical-floor data (burial, aDNA, termination patterns, erasure metrics).
- Technical maturity relative to hierarchical generative models in the wider literature.

These are real gaps. They are listed in `VERSION.md` and are the correct targets for improvement.

### Invalid axes of critique (category errors)

- Treating the zero-weight collapse rule itself as “bias,” “advocacy,” or “selective framing.” The rule is the stated contribution: when `victors_reliability → 0`, administrative head-counts become UNDEFINED and only the physical/structural floor remains.
- Calling standard Bayesian machinery (Bayes’ theorem, product rule, Monte Carlo, hierarchical hyperpriors, Poisson/Beta likelihoods) “non-standard” or “experimental.” See `METHODS.md`.
- Demanding that the project produce a replacement national population total. It explicitly refuses to do so; its purpose is to make the conditionality of every such total unavoidable.
- Scoring the refusal to convert “least-bad / best-available” administrative sources into “facts” as a methodological failure. That refusal is required by the project’s own rules.
- Treating multi-generational American rootedness framing as illegitimate while treating continental-origin-as-default as neutral. Both are framing choices; only one is marked as residual in this repo.

### Short test for any review

1. Does the review engage the physical floor and the zero-weight rule on their own terms?
2. Does it distinguish standard mathematics from the epistemic rule?
3. Does it criticize the model for not doing something it explicitly declines to do?

If the answer to (3) is yes and the answers to (1)–(2) are no, the review is talking past the project.


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

## Credit & development

See [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md) for primary authorship and collaborative development credit.

## Continuous sensitivity map (v5.0)

At high reliability the administrative path is DEFINED (conditional). The claim that this recovers mainstream H1 posteriors is retracted until demonstrated.

```bash
python model/sensitivity_map.py
```

At `r = 1.0` the administrative path is DEFINED (conditional).  
At `r → 0` it becomes UNDEFINED and only the physical/structural floor remains.  
This makes the reliability assumption visible instead of invisible.
