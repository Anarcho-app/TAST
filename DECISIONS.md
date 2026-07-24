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
| 2026-07-24 | Likelihood uncertainty (Beta means) | H5 interval 22.2–84.0% at r=1, κ=8 (n=2000, seed=42) | False precision removed |
| 2026-07-24 | H5 operationalized into H5a–H5d | H5 must be falsifiable | See model/h5_subclaims.md |
| 2026-07-24 | Structural limit of Beta layer acknowledged | — | Beta tests precision around analyst means; does not test direction. Credit: Opus 4.8 |
| 2026-07-24 | Adversarial H1 tables measured | H1 stays below prior at median even under full charity | See below |
| 2026-07-24 | H5 column audit | residual wins by never being surprised (8/11 ≥0.75) | Next: decompose into H5a–d |

## Explicit statement (critique #2)

We have **lowered** H5’s unearned certainty when floor streams were excluded and when
collapse became continuous. We have **not** yet identified primary-linked quantitative
evidence that raises H1 (or H4) above residual H5 under the current 11-stream table at r=1.
That is diagnostic and is stated here rather than omitted.

Publishing your own negative result is the thing most projects never do.

Stream-level defense/revision (especially Demographic Growth Rates H1=0.07) remains open.

## Adversarial H1 results (measured)

```
r = 1.0              H1 point    H1 CI (κ=8, n=2000)     H5
current              0.0000      [0.0000, 0.0000]        0.577
adversarial (5)      0.0001      [0.0000, 0.0004]        0.577
full_charitable      0.0343      [0.0050, 0.1179]        0.558
prior                0.0727
```

Under the most charitable mainstream reading of all eleven quantitative cells, H1 remains below its prior at the point estimate and at the median. Likelihood uncertainty (κ=8) admits values above the prior in the upper tail (95th ≈ 11.8 %). The honest statement is therefore:

> Under the most charitable mainstream reading, H1 remains below its prior at the median, though likelihood uncertainty admits values above it in the upper tail.

This is weaker than an unqualified “negative result is robust” and more defensible — the distinction the Beta layer was added to surface.

## H5 column audit

Mean likelihood across the 11 quantitative streams (current table):

```
H1:  0.220    0/11 cells ≥ 0.75
H2:  0.768    7/11
H3:  0.750    7/11
H4:  0.441    3/11
H5:  0.764    8/11
```

H5 (“mixed / undocumented mechanisms / residual”) is assigned ≥ 0.75 on eight of eleven streams. A hypothesis that is never surprised by any observation wins a likelihood product by construction. Discrete hypothesis products apply no Occam factor. H5 at 57.7 % is not evidence about mechanisms; it is what happens when you multiply eleven numbers near 0.8.

This is the exact mirror of the H1-column inversion. Stream 26 commits the project to catching it. The open structural item is to replace the single H5 column with H5a–H5d so each sub-claim must make predictions and can lose.

## Operational status (honest)

- [x] Measured adversarial numbers published (not only conditional framing)
- [x] `--streams PATH` flag implemented correctly (path passed explicitly to `load_streams`; no global rebind)
- [ ] Non-canonical duplicate files still present in some trees — `literature_engage.md` (root canonical) and `data/stream_likelihood_meta.csv` (canonical); delete the other copies when applying this package
- [ ] H5 column decomposition into H5a–H5d (most consequential remaining item)

## How to run the comparison

```bash
python -m model.bayesian_core --reliability 1.0
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_adversarial.csv
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_full_charitable.csv
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_full_charitable.csv --lik-uncertainty 2000 --kappa 8 --seed 42
```

Credit for diagnosis of the broken global-rebind, the false-negative risk, the CI nuance, and the H5 audit: Claude Opus 4.8.
