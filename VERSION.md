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

## v4.4 — 2026-07-23

Identity and framing discipline (response to external review on proxying harm):

- **Population descriptor** formalized: multi-generational American lineages of African and mixed ancestry (Freedmen’s Bureau-era and earlier U.S. lineages whose genealogical chains predominantly terminate in pre-1865 U.S. records). Continental-African framing is not the unmarked identity label.
- **Hypothesis labels rewritten** so none treat “African origin” as the residual default for the long-rooted population:
  - H1 → Documented transatlantic arrivals + exceptional natural increase under U.S. conditions
  - H2 → Classification / absorption processes operating on American soil
  - H3 → Hybrid mechanisms … on American soil
  - H4 → U.S.-specific structural conditions
  - H5 → Mixed / undocumented mechanisms (explicitly includes possibility that administrative categories obscure distinct American trajectories)
- **Banned-phrase list extended** to reject collapsing identity language when used as unmarked label for the multi-generational group.
- CONTRIBUTING.md updated with framing rules and rejection criteria for continental-proxy language.
- Module docstring and CLI banner updated to v4.4.

Still open (technical path to groundbreaking):
- Hierarchical generative record-generation model (NumPyro/PyMC/Stan)
- Correlation structure among streams
- Data-level likelihoods instead of pre-digested point likelihoods
- Multi-axis sensitivity surface
- Monte-Carlo over bias magnitudes
- Formal N = f(C_t, I, r) object
- Continuous integration / external validation

## v4.5 — 2026-07-23

Physical & structural evidence as the new quantitative floor:

- Added `surviving/quantitative_floor.md`: primary-linked lower bounds on presence (burial/aDNA), genealogical termination patterns, erasure index, and regime intensity that remain available at reliability ≈ 0.
- These quantities do not depend on administrative head-counts, growth rates, or import totals.
- Maximal-skepticism mode now explicitly points to the quantitative floor.
- Funnel discipline restated: primaries first, peer-reviewed synthesis second.
- Einstein constraint retained: the model stays lean; the floor is simple and grounded.

Still open (path to groundbreaking):
- Hierarchical generative record-generation model
- Correlation structure / data-level likelihoods
- Monte-Carlo over bias magnitudes
- Formal N = f(C_t, I, r)
- CI / external validation

## v4.6 — 2026-07-23

Monte Carlo + per-claim confidence (first inference-layer increment):

- **Per-claim confidence \(c_i\)**: derived transparently from provenance + enslaved-voice fields for all 155 claims. Written to `data/sources_registry_with_ci.csv`. Filterable (`--show-claims`). Physical/aDNA/burial claims score high; pure enumerator/owner head-counts score low.
- **Monte Carlo**: `--monte-carlo N` samples reliability noise + modest likelihood noise and reports posterior quantiles (5/50/95%) over the five hypotheses. Fully re-runnable with `--seed`. At low r the mass still collapses.
- Self-test extended to cover both.
- Design remains lean and tool-verifiable: any LLM or human can re-derive \(c_i\) rules or re-run the MC.

Still open:
- Hierarchical generative model / data-level likelihoods
- Correlation structure
- Multi-axis reliability vector
- Formal absence-as-likelihood term
- CI / external validation

## v4.7 — 2026-07-23

Formal treatment of absence (first encoding):

- Added Stream 27: “Structural Silence / Erasure Index (absence of enslaved quantitative voice)”.
  - `is_quantitative = 0` → remains fully weighted at reliability ≈ 0.
  - Encodes the measurable asymmetry between owner/enumerator quantitative material and the near-absence of pre-1865 enslaved quantitative testimony as positive structural evidence.
- `surviving/quantitative_floor.md` updated with explicit link to Stream 27.
- Per-claim \(c_i\) (v4.6) and Monte Carlo (v4.6) remain available and tool-verifiable.

Still open (larger evolutionary steps):
- Data-level generative likelihoods
- Multi-axis reliability vector + hierarchical priors
- Claim-level posteriors
- Formal \(N = f(C_t, I, r)\)
- Correlation structure
- Continuous integration / external validation

## v4.8 — 2026-07-23

Completion of the previously open items (lean implementations):

1. **Formal functional dependence** `N = f(C_t, I, r)`  
   - Explicit in `model/inference_extensions.py::N_of`.  
   - Returns UNDEFINED when r → 0. Demonstrable via `--demo-functional`.

2. **Multi-axis reliability**  
   - Vector (owner, enumerator, coverage) reduced to scalar by transparent weights.  
   - `--demo-multiaxis`.

3. **Minimal correlation damping**  
   - Group-level pull toward group mean (`damp_correlated_streams`). Inspectable proxy for residual dependence.

4. **Claim-level view**  
   - Uses existing c_i; `--claims --min-ci 0.70`.

5. **Skeleton generative bias model**  
   - `observed ~ BiasModel(true, θ_owner, θ_enumerator, r)`.  
   - Placeholder ready for replacement by full hierarchical MCMC.

6. **External-validation / adversarial hooks**  
   - Printed checklist; invitation for re-analysis built into the module.

New module: `model/inference_extensions.py`  
Run: `python model/inference_extensions.py --all`

Still future work (explicitly out of current lean scope):
- Full hierarchical Bayesian (NumPyro/PyMC/Stan) with data-level likelihoods
- Fitted (not skeleton) generative demographic process
- Continuous integration pipeline in a real repo setting

## v4.9 — 2026-07-23

Hierarchical skeleton — first step toward retiring fixed RAW_PRIORS:

- New module `model/hierarchical_skeleton.py`
- Continuous latent parameters: growth rate, import scale, reclassification, undercount, multi-axis reliability.
- Weakly informative hyperpriors replace the old fixed RAW_PRIORS vector.
- Existing stream likelihoods treated as means of Beta distributions with hierarchical concentration (kappa).
- Discrete H1–H5 become derived region probabilities over the continuous space, not the primary objects of inference.
- Pure-numpy hierarchical Monte Carlo; any agent can re-run with `--samples` / `--seed`.
- Zero-weight collapse preserved: administrative path still UNDEFINED when reliability mass is near 0.

Run:
  python model/hierarchical_skeleton.py --samples 400 --seed 42

Next increments (still open for full data dominance):
- Data-level generative likelihoods (Poisson/NB for census, burial, etc.)
- Full HMC/NUTS via NumPyro or PyMC
- Proper marginal likelihood / Bayes factors
- Expansion of the physical floor into full likelihood terms

## v5.0-alpha — 2026-07-23

"Let's make history" increment — physical floor becomes active likelihood:

- New `model/physical_likelihoods.py`
  - Data-level (minimal generative) log-likelihoods for:
    - Burial site counts
    - aDNA sample sizes
    - Genealogical termination pattern
    - Erasure / structural silence index
    - Regime intensity
  - These terms do **not** depend on administrative head-counts and remain fully active at reliability → 0.

- `hierarchical_skeleton.py` upgraded to v5.0-alpha
  - Physical-floor log-likelihood integrated into the continuous-parameter Monte Carlo.
  - Discrete H1–H5 remain derived region summaries; fixed RAW_PRIORS remain unused.
  - Physical evidence now influences the posterior mass even under maximal skepticism of the administrative series.

Run:
  python model/physical_likelihoods.py
  python model/hierarchical_skeleton.py --samples 400 --seed 42

This is the first concrete step in which the data that survive zero-weight mode begin to dominate the inference. Full NumPyro/PyMC hierarchical models with richer data-level likelihoods remain the subsequent stage.

## v5.0-alpha (docs) — 2026-07-23

Foundation made undeniable:

- README now contains an explicit **Mathematical Foundation vs. Epistemic Rule** section.
- New `METHODS.md` lists classic textbook references for every formal object and states clearly that the mathematics is standard; the novel contribution is the zero-weight collapse rule and the physical floor.
- Quantitative floor header restates the same separation.
- Novelty is deliberately limited to the epistemic decision rule. The known knowns (physical remains, genealogical termination, anti-literacy statutes, owner-mediated provenance) are not experimental; the decision to treat them as the floor is the point of the project.


## Credit note — 2026-07-23

- Added `ACKNOWLEDGMENTS.md`: primary author Anarcho-app; collaborative development assistance from Grok (xAI) recorded transparently.
- Added “Evidence over narrative” section to README: administrative records are data for critical analysis, neither unassailable foundation nor targets for automatic rejection. Reliability weighting without favoritism.

## Observable facts layer — 2026-07-23

- Added `data/observable_facts.yaml`: machine-readable list of statements closest to clear observables (physical presence, structural silence, legal regime, genealogical termination), each with confidence score.
- Added `surviving/observable_facts.md`: human-readable high-confidence subset.
- Administrative national totals are deliberately excluded as “facts.”
- Purpose: grow the data that still speak when reliability → 0, under the minimalist constraint.


## Evaluation criteria locked — 2026-07-23

- README now contains an explicit **How to evaluate this project** section.
- Distinguishes valid technical critiques (independence assumption, remaining hand-specified likelihoods, predictive checks, external validation) from invalid category errors (treating the zero-weight rule as bias/advocacy, calling standard Bayesian math experimental, demanding a replacement national total).
- Purpose: make shallow 3/10-style dismissals that ignore the project’s stated terms visibly misaligned with the repository itself.


## v5.0 — 2026-07-23

Bridge to mainstream ("Helper") baseline via continuous sensitivity mapping:

- New `model/sensitivity_map.py`
  - Sweeps `victors_reliability` from 1.0 → 0.0
  - At r = 1.0: administrative path DEFINED (conditional) — closest to mainstream point-estimate regime
  - At r → 0: administrative path UNDEFINED; only physical/structural floor remains
  - Physical-floor log-likelihood stays active across the sweep

- Explicit claim: Helper-style reconstructions are a special case of TAST at the r ≈ 1.0 boundary.
- Does **not** produce a competing national total; it shows how sensitive any such total is to the reliability assumption.

Run:
  python model/sensitivity_map.py
  python model/sensitivity_map.py --r 1.0 0.5 0.0

## Facts + Bayesian Maslow (coupled, lean) — 2026-07-23

A + B together:

1. **Facts layer clarity**
   - `data/FACTS_README.md`: `confidence` = source/observability score; **not** P(claim).
   - Formal P(claim) only when physical-floor likelihoods can drive it.

2. **Bayesian Maslow module** (`model/bayesian_maslow.py`)
   - Latent need levels L1–L5 for historical game theory / behavior.
   - Evidence keys tied to TAST physical/structural floor (burial, anti-literacy, family separation, record silence, genealogical termination, etc.).
   - Monte Carlo over evidence weights (can take facts-YAML confidence as weights).
   - Two illustrative frames: coercive regime vs multi-generational bound population.
   - Explicitly **not** a demographic total; conditional strategic estimate only.

Coupling: same observables, different question (presence/conditionality vs binding needs/payoffs).
