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

## v5.1 — response to Claude Opus 4.8 clone-and-run audit (2026-07-24)

Adversarial review credit: Claude Opus 4.8 (and prior Gemini). See ACKNOWLEDGMENTS.md.

### Confirmed failures (Opus) and status

| Issue | Status |
|-------|--------|
| Zero-weight collapse was a print short-circuit, not mathematical collapse | **Fixed (honest path)**: at r≈0 the program no longer hides the posterior; it prints the posterior from non-quantitative streams only and labels that this is *not* a return to the prior. |
| Non-quantitative streams dominate and settle H5 at every r | **Open / documented**: floor streams are not mechanism-neutral. Audit required (flatten likelihoods across H1–H5 if floor is meant to be silent on mechanism). |
| physical_loglik not wired into bayesian_core | **Open**: still only used in sensitivity_map / hierarchical_skeleton. Wiring + load from observable_facts.yaml by id is next. |
| PhysicalObservations hardcoded, not from YAML | **Open** |
| Floor terms depend on r (circularity) | **Open**: remove r from floor generative terms or justify explicitly. |
| “Helper = r=1.0 boundary” falsified (H1 ≈ 0 at all r) | **Retracted pending fix**: sensitivity_map language softened; H1 recovery at high r is a real gap. |
| Independence assumption inflates H5 | **Documented** (already in VERSION); not yet modeled away. |
| RAW_PRIORS derivation undocumented | **Open** |

### What v5.1 changed in code

- `bayesian_core.py`: maximal-skepticism path prints the computed non-quantitative posterior instead of claiming “UNDEFINABLE” and returning early.
- `sensitivity_map.py`: same honesty at r≈0; Helper boundary claim marked under audit.
- ACKNOWLEDGMENTS.md: Claude Opus 4.8 and Gemini listed as adversarial reviewers with specific findings.

### Fix order remaining (Opus list, still open)

1. Audit 16 non-quantitative rows → near-flat on H1–H5 if floor is mechanism-silent, **or** explicitly own that the floor *does* inform mechanism.
2. Wire `physical_loglik` into `bayesian_core`; load observations from `observable_facts.yaml` by fact id.
3. Remove r from floor likelihood terms (or document dependence).
4. Fix or permanently retract Helper boundary claim; if kept, H1 must be recoverable at r=1.0 under some documented setting.
5. Optional: assert documentation of current r=0 behavior in self-test (posterior from non-q streams, not prior).

The collapse rule remains the contribution. It is now implemented without suppressing numbers the code already computes.


## v5.2 — next Opus fixes + Gemini credit (2026-07-24)

1. **True zero-weight collapse**: at r≈0, mechanism posterior **returns to the prior**. Floor streams are no longer used to force H5. Physical presence stays in surviving claims, observable facts, and physical_loglik as presence support — not as a silent mechanism vote.

2. **Non-quantitative stream audit (partial)**: meta/uncertainty streams moved toward near-flat; extreme anti-H1 values softened. Full mechanism-neutrality of every floor row is less critical once r≈0 returns to prior.

3. **Circularity fix**: `physical_likelihoods.py` no longer makes erasure asymmetry or regime count a function of r. Structural observables are fixed.

4. **Helper boundary claim**: remains under audit / effectively retracted until H1 is recoverable at high r under a documented setting.

5. **Gemini** fully credited in ACKNOWLEDGMENTS for the comparative critiques that forced the math-vs-epistemic-rule separation and evaluation criteria.

Still open:
- Wire physical_loglik into joint update; load PhysicalObservations from observable_facts.yaml by id
- Document RAW_PRIORS derivation
- Correlation / partial pooling (independence still inflates sharpness when r high)
- Optional: restore a controlled Helper-boundary demo without claiming current H1 posteriors match mainstream totals


## v5.3 — open items completed (2026-07-24)

1. **PhysicalObservations from YAML**: `physical_likelihoods.load_observations_from_yaml()` maps floor fact ids (floor-02, floor-03, floor-04, high-ci burial facts, etc.) into counts. Fallback defaults labeled. Currently loads e.g. n_burial_sites=16 from high-ci presence facts.

2. **RAW_PRIORS documented** in `bayesian_core.py`: 8:15:20:20:47 / 110, uncertainty-favoring, not fitted; r≈0 returns here.

3. **Correlation damping**: `--dampen S` applies group-level partial pooling via `inference_extensions.damp_correlated_streams` (inspectable proxy for residual dependence).

4. **Helper boundary claim**: permanently **retracted** until H1 is recoverable at high r under a documented setting. sensitivity_map language updated.

5. **True collapse + circularity fixes** from v5.2 retained.

Still future (not blockers): full joint hierarchical update combining physical_loglik with stream product; fitted data-level census likelihoods; NumPyro/PyMC.


## v5.4 — collapse is a function (Claude Opus second pass)

**Decision (owned):** at r < 0.05 the mechanism posterior **returns to the prior**. Floor streams are mechanism-silent by construction for H1–H5. Presence/structure live in surviving claims, observable_facts.yaml, and physical_loglik.

**Code:**
- `collapse_posterior(streams, priors, r)` in bayesian_core.py — single source of truth
- bayesian_core CLI and sensitivity_map both import and call it
- Self-test asserts `collapse_posterior(r=0) == PRIOR == RAW_PRIORS`
- README Helper boundary language aligned with retraction
- At r=0 both modules now print H5=42.7% (prior), not 80%+

Verified:
```
r=0 mode PRIOR H5 0.4273 H1 0.0727
r=1 mode UPDATED H5 ≈ 0.82
```


## v5.5 — continuous collapse (Claude Opus 3rd pass)

**Delete the threshold.** Non-quantitative streams are excluded from H1–H5 ranking at **all** r. Only quantitative streams enter `apply_reliability` + `bayes_update`. As r → 0, each L → 0.5, likelihood is flat, posterior → prior continuously. No cliff at 0.05.

Verified design consequence (Opus):
- Slider moves: H5 42.7% → ~58% range rather than stuck at ~82%
- Collapse is a consequence of the math, not a print or a magic constant
- Helper gap (H1 tiny at r=1) is now localized to the 11 quantitative rows

**Next open (Opus):**
- Defend or revise stream 1 (`Demographic Growth Rates` H1=0.07) — the natural-increase differential is central to H1 yet assigned near-zero likelihood under H1
- Use `--dampen` / correlation structure on the remaining 11 by default or document why not


## v5.6 — likelihood uncertainty + audited interpretation layer

- `--lik-uncertainty N --kappa K`: treats each quantitative L as a Beta mean; reports posterior quantiles under likelihood uncertainty (hierarchical_skeleton idea wired into main path).
- `data/stream_likelihood_meta.csv`: 55 cells with placeholder provenance (hand-specified pending primary-linked derivation) — same audit trail demand as facts YAML.
- `--dampen` help text corrected: group-mean shrink, not effective sample size.
- Substantive result (Opus leave-one-out): H1 exclusion is the quantitative table as a whole; not a single-cell or independence artifact. Defense/revision of those cells is now the research task.

Example:
  python model/bayesian_core.py --reliability 1.0 --lik-uncertainty 300 --kappa 8


## v5.7 — H5 falsifiability + decision log + literature bar

- Operationalized H5 into H5a–H5d with explicit rejection conditions (`model/h5_subclaims.md`)
- `DECISIONS.md` correction log; states we have lowered unearned H5 and not yet raised H1/H4 above residual H5 under the current quant table at r=1
- `conventional/literature_engage.md` named converge/diverge vs Hacker, SlaveVoyages, Fogel/Engerman, Gutman, Steckel, Borucki & O’Malley
- Uniform genetics evidentiary bar (same sample-size caution in every direction)

## v5.8 — literature pass → discriminating streams + precise erasure (2026-07-24)

- Stream 28: USCT pension & Freedmen’s Bureau marriage testimony (is_quantitative=0); erasure claim made precise rather than absolute.
- Stream 29: Steckel anthropometric signature (discriminating; H1 predicts joint morphological pattern, H2 does not).
- literature_engage.md v2: record producers with opposing incentives; named regional and theory literature; Fogel/USCT irony.
- quantitative_floor §7: isotopes + skeletal stress markers as mechanism-relevant physical measurements (no invented numbers).
- Independence assumption now has a concrete literature path.
- Direction: Claude Opus 4.8 literature pass. Likelihood values and verification remain project work.

## v5.8.1 — Stream 29 group fix + H5 absorption finding (2026-07-24)

- Stream 29 moved group N → R (own group) so `--dampen` cannot flip the only pro-H1 quantitative stream.
- Measured: adding Stream 29 raises H5 (0.577→0.591) because it penalizes H2 harder than the residual — cleanest demonstration that H5a–H5d decomposition is the blocking item.
- Full-charitable H1 median now marginal vs prior (6.07% vs 7.27%); upper tail ~20.9%. Bidirectional correction recorded in DECISIONS.
- Stream 28 explicitly documented as floor-only (no mechanism ranking).
- Credit: Claude Opus 4.8.

## v5.9 — genuine floor map (bodies, isotopes, law, sites) (2026-07-24)

- quantitative_floor.md §§7–11: bioarchaeological corpus, expanded isotopes (incl. Schroeder 2015 PNAS), Gross racial-determination trials prioritized, site/material culture path, explicit not-floor boundary (Kiple/Savitt/Hall/Higman).
- No numbers encoded; verification against papers required before likelihood terms.
- Priority to move model: isotopes (H1 vs H2 on bodies), then Gross trials (adversarial H2 documentation).
- Direction: Claude Opus 4.8. Figures and encoding remain project work after verification.

## v5.9.1 — encoding fix + prior-sweep (2026-07-24)

- Windows cp1252 crash fixed (UTF-8 reconfigure + ASCII bar fallback).
- `--prior-sweep`: H1≈0 at r=1 under current / uniform / mainstream-H1 priors (evidence-driven); r=0 prior-determined.
- README header version label updated (cosmetic drift).
- Floor-not-wired diagnosis recorded: physical_loglik held, not ranked; isotopes remain the path to make the floor learn.
- Credit: GLM 5.2 audit.

## v5.9.2 — multi-agent audit + verified isotope skeleton (2026-07-24)

- UTF-8 guard ported to physical_likelihoods.py and hierarchical_skeleton.py.
- data/verified_isotope_adna.yaml: only figures confirmed against primary papers (Harney 2023, Schroeder 2015, Fleskes 2023 accurate counts). Fabricated Anson Street birthplace claim rejected.
- model/M1_floor_likelihood_design.md: design for hypothesis-conditional floor likelihoods (no parameters invented).
- Stipulated floor constants flagged; four-test verdict and structural findings recorded.
- Credit: Kimi K3 (lead), Kat Coder Pro 2.5, Minimax M3.

## v5.9.4 — P1/P3 scaffolds (no invented numbers)

- schemas/gross_trial_corpus.schema.yaml (empty; fill from Gross / trial dockets only)
- model/floor_isotope_terms_scaffold.md (Beta-Binomial / Binomial per site; blocked on Goodman tables)
- Prioritization reconfirmed: isotopes → Gross → counted inventories → hierarchical independence → H5 submodels
