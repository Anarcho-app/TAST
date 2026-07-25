# Decision & Correction Log

Honest record of directional changes. Bidirectional when evidence supports it.

| Date | Decision | Direction | Notes |
|------|----------|-----------|-------|
| 2026-07-23 | Layered repo; zero-weight rule stated | — | Founding epistemic rule |
| 2026-07-23 | Physical floor + observable facts | strengthens presence claims | Not a national total |
| 2026-07-23/24 | Exclude non-quant streams from H1–H5 at all r | **lowers unearned H5** from floor product | Continuous collapse (Opus) |
| 2026-07-24 | Soften extreme anti-H1 floor likelihoods | **raises H1 path relative to old floor-only** | Before quant-only rule made this moot for ranking |
| 2026-07-24 | r→0 returns to prior by arithmetic (L→0.5) | **H5 82%+ → 42.7% at r=0** | Bidirectional vs earlier print-forced H5 |
| 2026-07-24 | Retract Helper = r=1.0 boundary | — | H1 not recovered at high r |
| 2026-07-24 | Likelihood uncertainty (Beta means) | H5 interval 22.2–84.0% at r=1, κ=8 (n=2000, seed=42) | False precision removed; prior ~19–81% was approximate |
| 2026-07-24 | H5 operationalized into H5a–H5d | H5 must be falsifiable | See model/h5_subclaims.md |
| 2026-07-24 | Structural limit of Beta layer acknowledged | — | Beta tests precision around analyst means; does not test direction of the means themselves. Credit: Opus 4.8 review |

## Explicit statement (critique #2)

We have **lowered** H5’s unearned certainty when floor streams were excluded and when
collapse became continuous. We have **not** yet identified primary-linked quantitative
evidence that raises H1 (or H4) above residual H5 under the current 11-stream table at r=1.
That is diagnostic and is stated here rather than omitted.

Publishing your own negative result is the thing most projects never do.

Stream-level defense/revision (especially Demographic Growth Rates H1=0.07) remains open.

## The one finding this pass (Opus 4.8)

The Beta layer removes false precision but cannot test direction. At κ=3 — Beta(0.21, 2.79) for stream 1's H1, about as diffuse as is meaningful — the best of 2000 draws puts H1 at ~1e-4 order:

```
κ=3    H1 median≈1e-10   99th≈4e-07   max/2000≈1e-04
κ=10   H1 median≈2e-09   99th≈4e-07   max/2000≈4e-06
```

The reason is structural: Beta(mean·κ, (1−mean)·κ) is centered on the analyst's own point estimate. Loosening κ asks how precisely do I know this cell. It never asks is this cell pointed the right way. Eleven cells centered anti-H1 stay anti-H1 under any concentration, because the draws are unbiased around anti-H1 means.

Quantified, what it would actually take at r=1.0:

```
H1 posterior = 1%   →  +0.405 on every H1 cell   (stream 1: 0.07 → 0.48)
H1 posterior = 5%   →  +0.503 on every H1 cell   (stream 1: 0.07 → 0.57)
```

That's not a precision question. That's a reinterpretation question, and nothing in the model currently poses it.

## Stream 1, since DECISIONS.md leaves it open

H1 is "documented arrivals + exceptional natural increase under U.S. conditions." Stream 1 is "Demographic Growth Rates." So the cell is asking: how surprising is the observed growth data, given the hypothesis whose entire content is that growth was exceptional?

The answer encoded is 0.07 — meaning the data would be very surprising under the hypothesis specifically constructed to predict it. On its face that looks inverted, and a mainstream reader would put it high, likely above H5's 0.80. It's the single clearest place where the table reads as encoding its conclusion rather than testing it, and it's doing 10.6× more work than any other cell.

## Concrete next step (adopted from Opus 4.8)

Build the adversarial H1 table: the strongest good-faith version a Hacker- or Eltis-aligned reader would write, particularly for streams 1, 4, 15, 20, 22. Run it. Publish both posteriors side by side.

That converts the honest negative — "we couldn't find evidence that raises H1" — into something much stronger: "here is the best case for H1, run through the same machine, and here is exactly where it fails." It's also what stream 26 (symmetric overreach filter) and the uniform genetics bar already commit us to; right now that symmetry is applied to genetic evidence and to the administrative totals, but not to the likelihood table itself.

## Reproducibility note (2026-07-24)

The κ=8 interval is now logged with exact parameters so the correction log itself is checkable:

- `python -m model.bayesian_core --reliability 1.0 --lik-uncertainty 2000 --kappa 8 --seed 42`
- Observed: H5 5%=22.2%  50%=56.4%  95%=84.0%  (matches independent reproduction)

## GPT 5.6 Sol / Kat / Minimax audit fixes (v5.9.11)

1. **CLI honesty at r=0**: mode-aware — prints PRIOR or UPDATED; no longer claims exact prior when floor-quant is active.
2. **is_floor_quantitative consumed end-to-end**: load_streams + apply_reliability + MC/uncertainty paths + self-test.
3. **Fabricated Anson "29 of 36 Lowcountry-born"** removed from observable_facts.yaml.
4. **n_adna default 66** (verified study sum); n_regime prefers jurisdiction_inventory count (5).
5. **Framing**: TAST is complementary audit/sensitivity framework, not a replacement for Hacker et al. national totals.

Credit: GPT 5.6 Sol & Kat Coder Pro 2.5 (Agent A) & Minimax M3 (Agent B).

## Claude Opus 4.8 second-pass fixes (v5.9.12) — 2026-07-24

Every finding below was reproduced from a fresh clone before the fix. Opus 4.8 ran the code rather than only reading the README, and every item landed inside the README's own valid-axes list (independence assumption, remaining hand-specified likelihoods, physical-floor scope). Corrections applied:

1. **Physical-floor runtime error fixed.** `model/physical_likelihoods.py` had `@dataclass` misplaced above `_n_regime_from_inventory()` (a function), producing `AttributeError: 'function' object has no attribute '__mro__'` at r=0. The decorator now sits above `class PhysicalObservations:`. The r=0 path emits its physical-floor log-likelihood cleanly.

2. **Sibling import fixed for `python -m` invocation.** `bayesian_core.py`, `hierarchical_skeleton.py`, and `sensitivity_map.py` each had `from physical_likelihoods import physical_loglik` which failed under `python -m model.bayesian_core`. Fallback to `from model.physical_likelihoods import ...` added. This restores the r=0 physical-floor loglik report.

3. **r=0 = prior stated plainly in README.** New README subsection "Reading the r=0 output correctly" says outright that the r=0 posterior is `RAW_PRIORS` returned, with modest offset from any `is_floor_quantitative=1` streams — not a data-fitted verdict. Core Design Principle #1 also expanded with the same statement. `METHODS.md` grew a "What this project's r=0 output IS" section.

4. **New floor-quant stream 31: Autosomal Native American ancestry ceiling.** Added to `evidence_streams.csv` with `is_floor_quantitative=1`, likelihoods H1=0.75 H2=0.10 H3=0.30 H4=0.65 H5=0.45. Grounded in Bryc et al. 2015 (n=5,269 African-Americans, 0.013% of ~40M AA population) + four cross-checks (Baharian 2016 n=3,726; Micheletti 2020 n=50,281; All of Us 2025 ~25k AA subset; gnomAD v4 LAI Kore et al. 2025 n=20,805). All four cohorts converge on ~0.5-2% mean autosomal Native American ancestry. Under any material Indigenous-reclassification model, autosomal Native ancestry would be far higher than trace. It isn't. This is a falsification test that requires no census, no manifest, and no enumerator — it survives `victors_reliability = 0` completely. Companion rationale: `model/stream31_autosomal_ancestry.md`. New floor fact `floor-09` in `observable_facts.yaml` with full sample-size discipline block.

5. **DNA sample-size discipline made mandatory.** New file `dna_sample_size_discipline.md` requires every DNA / aDNA / autosomal / isotope / haplogroup claim in the repo to carry `n`, reference population, `pct_of_reference`, selection mechanism, and what the sample supports vs. cannot support. Standard reference-population sizes documented. Worked examples for Bryc 2015, Harney 2023, Fleskes 2023, Goodman NYABG, and the global aDNA record. `METHODS.md` updated. This applies to Stream 31 out of the gate and is retroactive for any new DNA-referencing edits.

6. **H5 decomposition made numerically falsifiable.** `model/h5_subclaims.md` upgraded from v5.7 (rejection conditions only) to v6.0 (each of H5a–H5d now carries a scalar numerical prediction with 95% interval, a computation recipe from repo data, a rejection statistic, and a likelihood-mapping table). Until these observables are measured and the mappings applied, H5 is no longer allowed to absorb residual mass by being unfalsifiable.

7. **Hierarchical multi-regime reliability layer added (opt-in).** `model/inference_extensions.py` gains `DEFAULT_REGIME_PRIORS` (13 record-producing regimes with Beta(α,β) priors), `regime_scalar_for_stream()`, `hierarchical_reliability_vector()`, and `demonstrate_hierarchical_reliability()`. Scalar `victors_reliability` remains the default; hierarchical layer opt-in via `--demo-hierarchical` (opt-in adoption in `bayesian_core.py` is future work; the primitives are now in place). The `abolitionist_inquiry` regime carries the highest reliability prior (Beta(7,3), mean 0.70) because its bias direction opposes the trade — corroboration from adversarial regimes is especially probative. The single-scalar model treated Portuguese/Spanish/British/French/Dutch/Danish shipping + Brazilian/Cuban ports + admiralty + insurance + abolitionist inquiries as maximally correlated. That is a modeling error with direction; the hierarchical primitives make the correction available.

8. **Likelihood-table observation logged, not fixed.** Opus 4.8 measured cumulative LR H5/H1 ≈ 3.6×10⁶ across the 12 quantitative streams; independent reproduction here confirmed 3.617×10⁶ exactly. Mean H1 (all 28 streams) = 0.297, mean H5 = 0.650. H1 leads in 2 of 28 streams; H5 leads in 14. This is not the zero-weight collapse — it is twelve hand-set point values multiplied under an independence assumption the README already flags as a valid axis of critique. The correct fix is (a) stream-by-stream defense/revision (`DECISIONS.md` §"Stream 1, since DECISIONS.md leaves it open" already opens this) and (b) `--dampen` correlation damping (already implemented). No point-cell edits made in this pass; the observation is documented so it cannot be pattern-matched away as "the collapse rule producing H1=0.0."

Reproduction commands (all should succeed):

```bash
python model/physical_likelihoods.py                                # no @dataclass error
python -m model.bayesian_core --reliability 0.0                     # physical-floor loglik prints, r=0 = prior + Stream 30/31 offset
python -m model.bayesian_core --self-test                           # existing + new floor-quant paths pass
python -m model.inference_extensions --demo-hierarchical            # per-regime reliability demo
python -m model.inference_extensions --adversarial                  # hook list intact
```

Credit: Claude Opus 4.8 review (2026-07-24) for the runtime bug, the r=0-is-prior observation, the autosomal-ancestry falsification test, the hierarchical-reliability observation, and the H5 numerical-prediction requirement. Every valid observation landed inside the README's own valid-axes list; scoring the model on the invalid axes would have missed all seven fixes.

## Prior-sensitivity + regroup (2026-07-24) — the over-engineering / table-as-verdict point

**`--prior-sensitivity`** at r=1 (conservative Stream 31 table):

```
prior H1 = 0.0727  → post H1 ≈ 0.000%
prior H1 = 0.50    → post H1 ≈ 0.000%
prior H1 = 0.90    → post H1 ≈ 0.000%
prior H1 = 0.9999  → post H1 ≈ 0.44%
prior H1 = 0.999999→ post H1 ≈ 30.5%
```

No rational prior recovers H1. The likelihood table is the verdict. Further stream additions and prior tweaks are cosmetic until cells are rebuilt (especially Stream 1). This is the project's own "hidden conditioning" critique applied to itself.

**Group regroup:** US admin-linked quant streams (1,4,7,8,10,15,20,22) → group `U` so `--dampen` pools them. Floor (30,31) → `P`. SlaveVoyages → `V`. Dampen can now move cell values toward the group mean; H1 posterior remains ~0 because the *product* of still-anti-H1 means dominates — damping is not a substitute for generative cells.

Credit: Claude Opus 4.8 (prior-sensitivity table, KL redundancy detector, regroup-by-source-system).

## Effective-N damping + Stream 1 is the only remaining move (2026-07-24)

**Bug:** `damp_correlated_streams` shrank L toward the group mean but still multiplied all k terms — the opposite of correlation control.

**Fix:** `--dampen s` now uses group log-weights `w = k_eff/k` with `k_eff = 1+(k-1)(1-s)`. At s=1, group U (8 streams) contributes as **one** observation.

Measured at r=1 (conservative Stream 31):

```
s=0.0  H1≈0.0%  H5≈61.1%
s=0.5  H1≈0.0%  H5≈58.0%
s=1.0  H1≈0.1%  H5≈54.1%
```

Collapsing the entire US-admin cluster to one observation moves H1 from 0.0% to **0.1%**. Multiplicity is not the mechanism; **magnitude** is — eleven streams each encode “H1 fits poorly.”

**Streams 30 and 31** kept in separate groups (P vs R): different measurement systems / populations; must not share a damping factor.

**Shortlist collapses to one item:** Derive Stream 1 generatively — P(observed 1790/1860 counts | documented arrivals + NI model with explicit error structure), calibrated against Caribbean/Brazilian contrast cases. If that yields 0.07, the cell is earned. If it yields ~0.5, the headline dissolves. No further stream additions; no prior tweaks; damping is done.

Credit: Claude Opus 4.8 (effective-N formula, magnitude-not-multiplicity correction, Stream 1 sole priority).

## Triage (2026-07-24)

13 quant → **6 quant** in product.

- Demoted measurement-error streams 4, 20, 21 to is_quantitative=0 (σ/reliability layer).
- Demoted redundant 3, 7, 8, 10 (7≡8 duplicate vectors).
- Kept 1 (derived), 2, 15, 22, 30, 31.
- Stream 1 complete generative row restored in CSV.

Next = priors stage for parameters (Steckel CBR/CDR, Caribbean series, sex ratio, Indigenous pool) — not new asserted cells.

Credit: Opus 4.8 Max triage plan.
