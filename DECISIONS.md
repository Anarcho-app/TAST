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
