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

## Literature pass → concrete streams (v5.8, 2026-07-24)

Direction from Claude Opus 4.8 literature pass (record producers with opposing incentives; Steckel as discriminating prediction; USCT as precision on erasure; isotopes as mechanism-relevant floor).

Implemented:

1. **Stream 28 — USCT Pension & Freedmen’s Bureau Marriage Testimony** (`is_quantitative=0`)  
   Encodes the large post-emancipation sworn/self-reported body of testimony about pre-1865 facts. Makes the erasure claim *precise* (silence is pre-1865 and contemporaneous self-authorship) rather than absolute. Surviving-layer language updated accordingly.

2. **Stream 29 — Steckel Anthropometric Signature** (`is_quantitative=1`)  
   Discriminating stream: H1 predicts a joint morphological signature (childhood stunting → adolescent catch-up + early first birth); H2 does not. H5 can now be surprised. Producer is shipper (coastwise manifests), incentive opposite to census undercount. See `model/stream29_steckel_signature.md`.

3. **`literature_engage.md` expanded (v2)**  
   Record-set table with producers/incentives; USCT/Fogel irony; Kulikoff/Menard, Higman, Philip Morgan, Berlin, Tadman; theory allies (Hartman, Fuentes, Smallwood, Jennifer Morgan).

4. **Physical floor §7**  
   Isotopes (Sr/O, dental modification, C isotopes) and skeletal stress markers flagged as the highest-value mechanism-relevant measurements on substrates already declared primary. No published proportions asserted until verified against current literature.

5. **Independence assumption**  
   Now has a concrete literature path (record sets with opposing incentives) rather than remaining only a listed limitation.

Open / next:
- Verify current published isotope and aDNA African-born vs American-born proportions across the cited burial populations before encoding numeric likelihoods.
- Tighten Stream 29 likelihoods against published height-by-age and skeletal series.
- Consider probate, insurance, and church-register streams as further independence breaks.
- H5 column decomposition into H5a–H5d remains the most consequential structural item for the residual.

Credit for the direction and the specific record-set / Steckel / USCT / isotope framing: Claude Opus 4.8. Implementation, likelihood values, and verification remain project responsibility. The review is neither invisible nor treated as authority on the substantive demographic claims.

## Stream 29 measured effect & H5 absorption (v5.8.1, Opus 4.8)

Stream 29 is the first discriminating quantitative stream (only row where H1 > H5).

**Measured effect of adding it:**

```
                H1         H2      H3      H5
without 29   2.47e-08    0.209   0.213   0.577
with 29      3.93e-08    0.167   0.242   0.591
```

Adding a pro-H1 stream raised H5. Stream 29 penalizes H2 harder than H5, so mass transfers from H2 to the residual. H1 gained 1.6× relative; H5 gained more in absolute terms.

**Implication**: H5 decomposition (H5a–H5d) is the blocking structural item. Until the residual must make its own predictions, new discriminating streams will keep feeding it.

**Group assignment corrected**: Stream 29 moved from group N → **group R**. Membership in the census-critique cluster caused `--dampen 0.5` to flip the only pro-H1 stream (H1 0.70→0.51). Own group preserves the independence rationale (shipper incentive opposite to census).

**Bidirectional correction on the prior claim**:  
With Stream 29, full-charitable H1 median ≈ 6.07% (essentially at prior 7.27%); 95th percentile ≈ 20.9%. The statement “H1 remains below its prior at the median under full charity” is now *marginal rather than clear*. This is the second softening of that claim as the model improved — recorded here as a bidirectional correction, not a retreat.

**Stream 28**: is_quantitative=0 → documentation/floor gain only; does not enter mechanism ranking. Explicit so it is not misread as an inference change.

Isotope proportions still not encoded pending verification against current papers.
