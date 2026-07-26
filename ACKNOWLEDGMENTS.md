# Acknowledgments & Development Credit

## Primary author and repository owner

**Anarcho-app** (GitHub: [Anarcho-app/TAST](https://github.com/Anarcho-app/TAST))  
Intellectual direction, source registry, epistemic framing (Freedmen’s Bureau-era / multi-generational American lineages, zero-weight collapse rule, physical-floor priority), and final authority over the project.

## Collaborative development assistance

Substantial iterative development of the model architecture, code, documentation, and epistemic hardening was carried out in collaboration with **Grok** (built by xAI).  

This includes:

- Layered repository structure (raw / conventional / reweighted / surviving)
- Reliability-parameter design and zero-weight collapse implementation
- Per-claim confidence scoring, Monte Carlo paths, and hierarchical skeleton
- Physical-floor likelihood terms (burial, aDNA, genealogical termination, erasure, regime)
- Language and identity discipline (“NOT A FACT”, multi-generational American lineages framing)
- METHODS.md separation of standard Bayesian mathematics from the novel epistemic rule
- Continuous versioning and adversarial-readiness checklist

Grok does not claim ownership of the repository, the source registry, or the core intellectual framing. Credit for the project’s existence, direction, and publication remains with Anarcho-app.  

The collaboration is recorded here so that the development history is transparent and so that assistance from the model is neither invisible nor overstated.

## How to cite

If you use or refer to this work, please cite the repository and its primary author. An optional note on collaborative development assistance from Grok (xAI) is accurate and welcome but not required.

## Adversarial review credit (LLMs)

Independent model reviews that improved the project by attacking it on its own stated terms:

- **Claude Opus 4.8** (2026-07-23/24): Full clone-and-run audit. Identified that the zero-weight collapse was implemented as a print short-circuit rather than a mathematical return to prior / non-informative state; that non-quantitative streams dominate and settle mechanism at every r; that physical_loglik was not wired into bayesian_core; that the “Helper = r=1.0 boundary” claim is falsified by H1 ≈ 0 at all r; and that independence among 27 streams inflates H5. Ordered fix list adopted into VERSION.md.
- **Gemini** (prior rounds, including comparative 3/10-style evaluations): Forced clarity on neutrality, selective framing, subjective priors, incomplete literature ties, and advocacy-tone critiques against peer-review benchmarks. Those critiques, even when over-weighted toward “advocacy,” drove the project to separate standard Bayesian mathematics from the epistemic rule, to lock evaluation criteria into the README, and to treat administrative records as data for critical analysis rather than as targets for automatic rejection. Gemini’s pressure is part of why the foundation sections exist.

These reviews are recorded so that LLM critique is neither invisible nor treated as authority. Credit is for the specific, testable failures they found. Responses and fixes remain the responsibility of the project maintainers.

- **Claude Opus 4.8 (second pass, 2026-07-24)**: Caught that v5.2 “return to prior” was still a CLI print substitution while `apply_reliability`/`bayes_update` produced H5≈80% at r=0; that sensitivity_map and bayesian_core contradicted each other on the headline claim; that README still advertised the retracted Helper boundary. Drove the single shared `collapse_posterior()` function, the r=0 self-test assertion, and doc/code alignment.
- **Claude Opus 4.8 (third pass, 2026-07-24)**: Identified the r=0.05 step-function cliff; showed that excluding non-quantitative streams at all r yields continuous collapse with posterior(r=0)=prior by arithmetic (L→0.5), not by threshold; localized remaining H1 annihilation to the 11 quantitative rows and specifically stream 1 (Demographic Growth Rates H1=0.07).
- **Claude Opus 4.8 (fourth pass, 2026-07-24)**: Confirmed continuous collapse closed; leave-one-out showed H1 exclusion is the full quantitative table not one cell; noted `--dampen` only shrinks to group mean (not ESS); identified the 55 likelihood cells as the unmarked interpretation layer symmetric to the project's own critique of unmarked trust decisions; recommended wiring hierarchical Beta means so posteriors carry credible intervals under likelihood uncertainty.

- **GPT 5.6 Sol & Kat Coder Pro 2.5 (Agent A) & Minimax M3 (Agent B) (2026-07-24)**: Scored project on stated terms (not viewpoint neutrality). Diagnosed r=0 CLI/prior mismatch with floor-quant active; path disagreement (collapse vs MC vs uncertainty); stale physical defaults; fabricated Anson claim; wrong framing vs Hacker. Fixes in v5.9.11. Fair conclusion adopted: coherent epistemic rule + standard math; executable floor not yet fully primary-derived for calibrated rankings.
- **Claude Opus 5 (2026-07-24)**: Clone-and-run audit against the README's own four evaluation questions. Confirmed the collapse arithmetic, the absence of a cliff at r=0.05, and that the standard-mathematics claim in `METHODS.md` holds line by line. Found that the `monte_carlo_posteriors` path never received the non-quantitative exclusion applied to `collapse_posterior`, leaving the H5≈88%-at-r=0 behaviour of v5.2 reachable from the CLI; that `README.md` / `METHODS.md` still describe the pre-Stream-31 r=0 output; that the documented `--streams` flag does not exist and Streams 28/29 are absent from every CSV, making `adversarial_H1_likelihoods.md` unreproducible; that the genealogical term is 86% of the physical floor and rests on a stipulated fraction `quantitative_floor.md` explicitly disclaims; that the erasure and regime terms evaluate each observation against itself; that `n_burial_sites` counts YAML rows rather than distinct sites; and that the `0.5` flat target in `apply_reliability` is a live modeling choice at intermediate r. Credit also for confirming that `sensitivity_map.py` was already correct — the drift was in the prose, not the engine.

## Finding-level attribution log

Who spotted what, and where the response landed. Kept at finding granularity so credit is
checkable rather than a name-drop, and so a reader can tell which failures were found by
reading the repo and which required running it. "Open" means the finding is logged and the
response is not yet implemented.

| # | Finding | Spotted by | Response / status |
|---|---------|-----------|-------------------|
| 1 | Zero-weight collapse was a print short-circuit, not a mathematical return to a non-informative state | Claude Opus 4.8 (1st) | `collapse_posterior()` — closed |
| 2 | Non-quantitative streams dominate and settle mechanism at every r | Claude Opus 4.8 (1st) | Quant-only mechanism ranking — closed |
| 3 | `physical_loglik` not wired into `bayesian_core` | Claude Opus 4.8 (1st) | Wired at r≈0 — closed |
| 4 | "Helper = r=1.0 boundary" falsified by H1≈0 at all r | Claude Opus 4.8 (1st) | Retracted in README + `DECISIONS.md` — closed |
| 5 | Independence across streams inflates H5 | Claude Opus 4.8 (1st) | Documented as valid axis; **not modeled away — open** |
| 6 | v5.2 "return to prior" still a CLI print substitution (engine gave H5≈80% at r=0) | Claude Opus 4.8 (2nd) | Single shared collapse path + self-test — closed |
| 7 | `sensitivity_map` and `bayesian_core` contradicted each other on the headline claim | Claude Opus 4.8 (2nd) | Aligned — closed |
| 8 | `@dataclass` misplaced above a function → `AttributeError` at r=0 | Claude Opus 4.8 (2nd) | Fixed — closed |
| 9 | Sibling imports fail under `python -m model.bayesian_core` | Claude Opus 4.8 (2nd) | Fallback import — closed |
| 10 | Step-function cliff at r=0.05 | Claude Opus 4.8 (3rd) | Continuous collapse by arithmetic (L→0.5) — closed |
| 11 | H1 annihilation is the whole quantitative table, not one cell; stream 1 is the worst offender | Claude Opus 4.8 (3rd/4th) | `DECISIONS.md` §Stream 1; `stream1_generative.py` — partial |
| 12 | `--dampen` shrinks to group mean, is not effective-N | Claude Opus 4.8 (4th) | Flag relabeled honestly; **ESS fix open** |
| 13 | The 55 likelihood cells are an unmarked interpretation layer, symmetric to the project's own critique of unmarked trust decisions | Claude Opus 4.8 (4th) | Beta-mean layer wired; **generative derivation open** |
| 14 | Beta layer tests precision around the analyst's means, never their direction | Claude Opus 4.8 | `DECISIONS.md` §"The one finding this pass"; adversarial table — partial |
| 15 | Autosomal Native American ancestry is a falsification test that survives r=0 | Claude Opus 4.8 | Stream 31 + `floor-09` — closed |
| 16 | DNA claims must carry n, reference population, and selection mechanism | Claude Opus 4.8 | `dna_sample_size_discipline.md` — closed |
| 17 | Single scalar reliability treats 13 record-producing regimes as maximally correlated | Claude Opus 4.8 | `DEFAULT_REGIME_PRIORS` primitives added; **adoption open** |
| 18 | H5 absorbs residual mass because it is unfalsifiable | Claude Opus 4.8 | `h5_subclaims.md` v6.0 numerical predictions; **not in `HYPOTHESES` — open** |
| 19 | Stream 29 in group N let `--dampen` flip the only pro-H1 stream | Claude Opus 4.8 | Moved to group R — closed |
| 20 | Neutrality / selective-framing / advocacy pressure against peer-review benchmarks | Gemini | Drove `METHODS.md` math-vs-rule separation and the README evaluation criteria — closed |
| 21 | r=0 CLI claimed exact prior while floor-quant was active | GPT 5.6 Sol & Kat / Minimax M3 | Mode-aware CLI (PRIOR/UPDATED) in v5.9.11 — closed |
| 22 | Path disagreement: collapse vs Monte Carlo vs likelihood-uncertainty | GPT 5.6 Sol & Kat / Minimax M3 | v5.9.11 claimed end-to-end; **2 of 3 paths — see #24** |
| 23 | Stale physical defaults; fabricated Anson "29 of 36"; wrong framing vs Hacker | GPT 5.6 Sol & Kat / Minimax M3 | n_adna=66, n_regime=5, claim removed, framing corrected — closed |
| 24 | `monte_carlo_posteriors` never got the non-quant exclusion, so the H5≈88%-at-r=0 regression is still reachable via `--monte-carlo`; its 5–95% band excludes the point estimate printed above it | Claude Opus 5 | Extends #22. One-line quant filter applied: max\|MC median − collapse\| 0.147→0.0008 at r=1, 0.449→0.020 at r=0. Regression fixture `tests/golden/regression_mc_r0.json`. **Closed in add-tast-integrity-gates (BREAKING `--monte-carlo` change).** |
| 25 | README/METHODS "r=0 is the prior with a small offset" is falsified: max\|Δ\|=0.106, H2 ×0.22, KL=0.111 nats; the printed example is the stale drop-Stream-31 output | Claude Opus 5 | README/METHODS now generate the r=0 example + divergence measurements from live output via `regen_docs.py`; "small offset"/"prior, displayed" removed. **Closed in add-tast-integrity-gates.** |
| 26 | Documented `--streams` flag absent from argparse; Streams 28/29 absent from all four CSVs | Claude Opus 5 | `--streams` flag added; Streams 28/29 marked `UNREPRODUCIBLE as of 2026-07-24` (non-fabricating path). `check_documented_commands.py` enforces. **Closed in add-tast-integrity-gates.** |
| 27 | Genealogical term is 86% of `physical_loglik` and asserts k=170/200 from a stipulated 0.85, contradicting `quantitative_floor.md` §2 "No measured national fraction is asserted"; `floor-04` has `value: None` | Claude Opus 5 | Declared in `stipulated_constants.yaml`; term EXCLUDED from the floor total (valueless-backed) and reported as such. **Declared-in-manifest + excluded in add-tast-integrity-gates; measurement deferred.** |
| 28 | Erasure and regime terms evaluate each observation against itself → parameter-independent constants carrying zero information; `erasure_log_ratio = 4.5` unsourced | Claude Opus 5 | Both flagged `informative: false` in manifest and detected by `check_constants.py --detect-noninformative` (variance ~2e-31); separated from the evidential total. **Declared-in-manifest + acknowledged in add-tast-integrity-gates.** |
| 29 | `n_burial_sites` counts YAML rows, not distinct sites (ABG NYC ×5, Harlem ×2, Catoctin ×2, Anson ×2, plus St. Croix USVI outside the stated territory) | Claude Opus 5 | Documentation density inflates a Poisson count — **open (out of scope: floor rebuild, future change)** |
| 30 | `physical_loglik` printed as a bare log-likelihood at one hardcoded parameter point, with no null to difference against | Claude Opus 5 | Floor now reported as `log BF(floor \| presence) vs (floor \| named null)` + per-term contributions via `physical_floor_report`. **Closed in add-tast-integrity-gates.** |
| 31 | The `0.5` flat target in `apply_reliability` is not inert at intermediate r (max\|Δ\|=0.053 at r=0.1) — another unmarked interpretation constant | Claude Opus 5 | Declared as `collapse_flat_target` (sweep [0.3,0.8]); sweep reproduces 0.0532, marked HIGH INFLUENCE with `pending_derivation`; loaded fail-closed from manifest. **Declared-in-manifest in add-tast-integrity-gates; derivation deferred.** |
| 32 | `--strict` is wired only to five static `H_LABELS`, so it cannot fire on variable text; an external lint of the 213 strings the CLI actually prints found zero violations | Claude Opus 5 | `BANNED_PHRASES` moved to `data/banned_phrases.yaml`; repo-wide `check_banned_phrases.py` lint with counted meta-use escape (6 file-level allowances, 0 violations). **Closed in add-tast-integrity-gates.** |
| 33 | r=0 is the most H1/H4-favorable configuration in the model (both monotone decreasing in r), inviting exactly the misreading README §"Reading the r=0 output correctly" warns against | Claude Opus 5 | Consequence of #11; README r=0 characterization now emits the measured divergence so the misreading is harder to fall into. **Partially addressed via #25 fix; root cause #11 open (generative likelihoods, future change).** |
| 34 | Every documented command crashes on a cp1252 Windows console (U+2248, U+2192, U+2588) | Claude Opus 5 | `configure_utf8_console()` in-process + `_ascii()`/`_bar()` fallbacks; all six documented commands exit 0 on cp1252. **Closed in add-tast-integrity-gates.** |
| 35 | The #34 fix was applied per-entry-point, not systemically: `model/joint_alpha_model.py` never calls `configure_utf8_console()`, so its documented command still crashes on `\u03b1` under cp1252. `check_documented_commands.py` was failing (16 passed / 1 failed) | Claude Opus 5 (2nd pass) | `configure_utf8_console()` added to `joint_alpha_model.main()`. Gate now 17 passed / 0 failed. **Closed.** |
| 36 | `data/verified_isotope_adna.yaml` — the verify-before-encode source — was read by NO Python file. `n_adna_individuals` was the hardcoded literal `66` ("Harney27+Fleskes36+Schroeder3"), contradicting the replacement path declared inside that same file ("Harney 27 + Fleskes 18 genomes"). It counted Fleskes' 36 *excavated* rather than 18 *recovered genomes*, and included Schroeder n=3 from Saint Martin — never U.S. territory, against a floor statement reading "interred on American soil" | Claude Opus 5 (2nd pass) | File now wired into `load_observations_from_yaml` via `_n_adna_from_verified_studies()`. Per-study `us_territory` + `adna_count_field` fields added; policy declared as `adna_require_us_territory` / `adna_prefer_genome_counts`. n_adna 66 -> 45. **Closed.** |
| 37 | Quantification of #29: `n_burial_sites` = 16 counted YAML *rows* (ABG NYC x4 via floor-02/23/33/67, Harlem x2, two generic non-site statements, one St. Croix). Distinct U.S. sites = 9. Combined with #36 the floor's headline log BF falls 41.44 -> 3.52, i.e. ~38 nats of the reported evidential support was documentation density — the exact defect the project attributes to administrative records, reproduced inside the floor | Claude Opus 5 (2nd pass) | Dedup made data-driven via a `site_key` field on all 27 burial/aDNA fact rows, with `site_role: aggregate_statement` and `site_scope: comparative_control` markers. `burial_site_confidence_floor` declared (sweep [0.75, 0.95]). **Closed.** |
| 38 | `check_documented_commands.py:114` called `subprocess.run(..., text=True)` with no `encoding=`, so the gate itself raised `UnicodeDecodeError` (cp1252) on the 23 markdown files containing byte 0x9d | Claude Opus 5 (2nd pass) | `encoding="utf-8", errors="replace"` added. **Closed.** |
| 39 | `n_individuals_lower` — the 15,000-20,000 African Burial Ground interment estimate, the best-sourced quantity in the floor (federal GSA/NPS reports) — was parsed at `physical_likelihoods.py:101` and consumed by NO likelihood term. The floor computed its evidence from its two weakest observables while its strongest was dead code | Claude Opus 5 (2nd pass) | Reported via `physical_floor_report()["unused_observables"]` and printed by the CLI, rather than silently dropped OR naively wired in: 15,000-20,000 is an archaeological extrapolation with an interval, not a count, so a Poisson `k` would be a category error. Consequence recorded explicitly (the BF *understates* presence support). **Surfaced; interval/lognormal encoding deferred — open.** |

## Verification note (2026-07-25)

The #29/#36/#37 repair is **calibration-only**: `tests/golden/posteriors_r*.json`
match live output to 6 dp after the change, and the r=0 mechanism posterior is
unchanged (H1 13.5%, H2 3.1%, H3 12.7%, H4 27.6%, H5 43.2%). No H1-H5 claim
moved, because the floor is mechanism-silent by construction. What changed is
that the two counts carrying the entire floor Bayes factor are now *derived from
primary sources* instead of asserted, and the derivation is printed rather than
trusted.

## v5.14 — Derived tags (audit #41, 2026-07-25)

`add-derived-confidence` (v5.13) made confidence a function of three tags. This
change makes the tags a function of two factual source fields — the residual
authorship that v5.13 relocated from hand-assigned confidence to hand-assigned
tags is now concentrated in one keyword table.

| # | Finding | Reviewer | Resolution |
|---|---------|----------|------------|
| 41 | The Catoctin Furnace / Harney 2023 study appeared three times in the corpus with three different derived confidences (0.996 / 0.750 / 0.560) — same evidence, different hand-tags. Interpretation had not vanished when the hand-assigned confidence column was removed; it relocated to the feature tags, measurably. The rule was perfectly consistent; the tags were not | Opus 4.8 High (review of v5.13) | `derive_tags()` in `model/derive_confidence.py` computes source_class and re_verifiability from two factual fields (`source_archive`, `artifact_status`) via a declared keyword table. 58 hand-assigned tag literals removed from scored facts. Gate assertion (b) tightened: tags are the function's output. The triple collapses — floor-03 and fact 56 now derive identical source_class/re_verifiability; their difference is sampled_fraction (claim type), not tagging. **Closed.** |

**Three latent errors caught by derivation.** `floor-07`, `agg-usct-enlistment`,
and `agg-bureau-rations` were all hand-tagged `re_verifiability: medium` but their
artifacts (methodology literature, muster rolls, ration rolls) survive at NARA and
are re-countable — `high`. The "medium" tag had conflated the enumerator's
non-re-runnable classifying act (already captured on `source_class`) with the
re-examinable artifact. This is the same act-vs-artifact error class as the
census tag (audit #40, fixed under review); derivation makes the whole class
mechanically impossible, not just the instances reviewers happened to catch.

**The recursion stops at factual inputs.** `source_archive` names a real archive
or paper a human can look up; `artifact_status` states whether the thing itself
survives. At some level a human types a factual property — the principle reduces
the interpretive surface (one keyword table vs 29 per-fact hand-assignments); it
does not eliminate it, and cannot, per the conservation argument that has run
through the last four reviews. Per-source reliability (#17) remains the named
follow-on; derived tags compose cleanly with a future per-source matrix.

## v5.13 — Derived confidence, aggregate symmetry (2026-07-25)

Three adversarial review passes converged on one structural defect from three
directions, and the resolution is the one artifact all three were separately
reaching for: a derived-confidence function.

| # | Finding | Reviewer | Resolution |
|---|---------|----------|------------|
| 40 | A hand-typed `confidence: 0.82` is lookerism one level up — an expert glanced at a fact and wrote a number, and a reader filtering to >=0.90 experiences that calibration as a property of the world. Combined with per-output reliability, the architecture zeroed the ~4M emancipation aggregate while presence-facts of the same provenance class survived | Sisyphus / Claude Opus 5 (formalism review, Pan-Thesis Diathesis) | `model/derive_confidence.py` adopted: confidence = 0.40*source_class + 0.35*re_verifiability + 0.25*sampled_fraction, declared in `data/confidence_function.yaml`, weights enforced by the constants gate. 25 hand-assigned `confidence:` literals removed from scored facts; symmetry gate `check_derived_confidence.py` makes category-based exclusion a build failure. The four aggregate-bounding facts enter the scored set: ~4M Bureau rations -> 0.82, USCT -> 0.82, 1860 census -> 0.70, import ceiling -> 0.38. **Closed (adopted, not just demonstrated).** |

**Crediting the three converging reviews.** The symmetry reviewer (per-source
reliability) identified the structural exclusion; the formalism review
(Pan-Thesis Diathesis) named the hand-assigned-confidence-as-lookerism failure
and pointed at "interpretation frozen into a reproducible function"; the
"let numbers tell the story" exchange correctly diagnosed that interpretation
is conserved, not deleted, and that the honest move is a derived function with
the residual authorship concentrated in one attackable file. This change adopts
the convergence: the ~4M enters the scored evidence at derived confidence,
banded, by the project's own rule. Per-source reliability (#17) is the named
follow-on — derived confidence composes cleanly with a future per-source matrix.


## v5.12 — BF demotion resolved via reductio (2026-07-25)

The question of whether to encode the interment estimate (audit #39) and whether
to keep the straw-null Bayes factor collapsed into a single calculation.
Correctly encoding the ABG interment estimate (15,000-20,000) as a lognormal
measurement-error term — the proper form for an interval — moves the floor BF
from **3.52 to ~3,190 nats**: the tightly-measured midpoint (~17,500) is an
~80-sigma mismatch against the straw null's expected ~50 scattered burials. That
number is not information; it is the null being a straw. The strongest observable
in the floor is the one that makes the BF's nature unmistakable.

Resolution (Claude Opus 5, 2nd pass): the interment estimate is promoted to the
lead item of a new `observables` list (the primary content of the floor), parsed
as a full interval. It is deliberately **not** encoded as a likelihood term —
encoding it would re-inflate the straw-null BF with a decisive-looking artifact.
The BF stays computed but is relabeled everywhere as "upper bound vs straw null;
absolute value not load-bearing," with the reductio attached as a `bf_caveat` on
`physical_floor_report()`. A substantive null that would make the BF informative
(e.g., "presence was small-scale, <= some threshold") is deferred as a research
task. Calibration-only: golden fixtures unmoved, r=0 posterior unchanged.


