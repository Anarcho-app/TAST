# Stream 31 — Autosomal Native American ancestry ceiling (Bryc et al. 2015)

## Purpose

Add a physical/genomic stream that discriminates H2 (classification / absorption of
Indigenous populations into the enslaved-descendant record) from H1/H3/H4/H5 on
evidence that survives `victors_reliability = 0` (owner, enumerator, trader, and
shipping records are irrelevant to autosomal-ancestry measurement).

Flagged `is_quantitative = 1` and `is_floor_quantitative = 1`. It bypasses the
`apply_reliability` r-blend and remains active in mechanism ranking at r → 0.

Credit: identified as a load-bearing floor gap by Claude Opus 4.8 (2026-07-24).

## Source

Bryc, K., Durand, E. Y., Macpherson, J. M., Reich, D., & Mountain, J. L. (2015).
"The Genetic Ancestry of African Americans, Latinos, and European Americans across
the United States." *American Journal of Human Genetics*, 96(1), 37–53.
DOI: 10.1016/j.ajhg.2014.11.010

## Sample-size discipline (mandatory)

| Quantity | Value | % of reference population |
|----------|-------|---------------------------|
| n African-American self-identified individuals | 5,269 | 0.013% of ~40,000,000 total AA population (2020 U.S. Census) |
| Mean African autosomal ancestry | 73.2% | — |
| Mean European autosomal ancestry | 24.0% | — |
| Mean Native American autosomal ancestry | **0.8%** | — |
| Reference panel size (AFR + EUR + NAT) | ~940 individuals | — |

The 0.8% Native American figure is the mean; the distribution has a right tail
(some individuals carry higher Indigenous ancestry) but the tail does not shift
the population mean above the trace band.

Cross-checks (independent samples):

| Study | n | % of ~40M AA reference | Native ancestry finding |
|-------|---|------------------------|-------------------------|
| Baharian et al. 2016 (Nature Comms) | 3,726 | 0.0093% | ~0.9% mean |
| Micheletti et al. 2020 (AJHG) | 50,281 | 0.126% | ~0.5–1.2% by region |
| All of Us / AJHG Jun 2025 | ~1,000,000 total, AA subset in Table S2 | ~2.5% of AA | 82.72% African (SD 10.87%); low Native (1–2%) consistent |
| gnomAD v4 LAI 2025 (Kore et al., Nature Comms) | 20,805 AA | 0.052% | ≥2-fold ancestry-specific frequency difference confirms two-way AFR-EUR admixture; low Native |

All three independent cohorts converge on autosomal Native American ancestry
in African-Americans within the ~0.5–2% band.

## Discrimination between hypotheses

Under H2 ("classification / absorption processes operating on American soil"),
material reclassification of Indigenous populations into the enslaved-descendant
record would predict autosomal Native American ancestry in modern African-
Americans materially higher than trace — plausibly in the 5–30% range depending
on the reclassification model. Observed: ~0.8% mean. This is the sharpest
available test that H2 does not do the load-bearing demographic work at
population scale.

Predicted-vs-observed reasoning by hypothesis:

| H | Prediction on Native % | L(H | data) |
|---|-------------------------|-------------|
| H1 documented arrivals + natural increase | ~0–2% Native (post-contact admixture only) | 0.75 |
| H2 classification / absorption of Indigenous | ≥ 5% mean Native, likely 10–30% under material reclassification | **0.10** |
| H3 hybrid (partial absorption + structural advantage) | 2–8% Native | 0.30 |
| H4 U.S. structural natural increase on American soil | ~0–3% Native (admixture only) | 0.65 |
| H5 mixed / residual | wide, symmetric residual | 0.45 |

These are the numbers encoded in `evidence_streams.csv` row 31.

## What this stream deliberately does NOT claim

- It does not assert a birthplace proportion. Genomic ancestry ≠ birthplace
  (see also `verified_isotope_adna.yaml` inference_rule caveats for Anson Street
  and NYABG).
- It does not license a national head-count.
- It does not preclude regional pockets of Indigenous absorption; it constrains
  the *population-scale* claim.
- It does not assume the reference panels are perfect. Reference-panel choice
  (e.g. 1000 Genomes Phase 3 ASW n=61 + ACB n=96 = 157 total AA reference
  samples) is itself a limitation logged in `sources_registry.csv` rows 110–118.

## Why is_floor_quantitative = 1

The physical-floor semantics of TAST are: evidence that survives when all
owner-, trader-, and enumerator-mediated records are set aside. Autosomal
ancestry from consumer genotyping cohorts is:

- Not owner-mediated (participants opt in).
- Not enumerator-mediated (no census-taker classifies the data).
- Not shipping-manifest-mediated (no trader produced it).
- Not administrative in the sense that `victors_reliability` was designed to
  discount.

It is a biological measurement on self-identified members of the focal
population. The `victors_reliability` scalar does not apply to it. Therefore
Stream 31 is coded `is_floor_quantitative = 1` and survives the r-blend intact.

## Falsifiability

This stream can be revised or retired if:

- New reference panels demonstrate that current autosomal Native % estimates
  are systematically biased low by an order of magnitude, **or**
- Local-ancestry inference reveals a much larger Indigenous component that was
  previously misclassified as African or European in the reference panels, **or**
- A specific reclassification model is presented that predicts the observed
  ~0.8% mean *and* the observed African / European ratios simultaneously.

Until then, the ~0.8% ceiling holds and H2 pays a likelihood penalty.
