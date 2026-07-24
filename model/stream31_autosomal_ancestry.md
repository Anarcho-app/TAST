# Stream 31 — Autosomal Native American ancestry (canonical encoding)

**Canonical likelihoods (conservative, 2026-07-24):**

| H1 | H2 | H3 | H4 | H5 |
|----|----|----|----|-----|
| 0.60 | 0.35 | 0.50 | 0.55 | 0.50 |

`is_floor_quantitative = 1`

## Published anchor

Bryc et al., *Am J Hum Genet* 2015, n = 5,269 self-identified African Americans: mean ancestry ≈ 73.2% African, 24% European, **0.8% Native American**. Cross-checks (Baharian 2016, Micheletti 2020, All of Us, gnomAD LAI) converge on roughly 0.5–2% mean NA ancestry in large modern AA cohorts. See `dna_sample_size_discipline.md` for n and % of reference population.

## What this supports vs does not

**Supports:** Population-scale material Indigenous absorption/reclassification as the dominant demographic mechanism is hard to reconcile with only trace autosomal NA ancestry in large modern self-identified AA samples.

**Does not:** Falsify H2 at 10:1. The cohort is defined by a social category whose boundaries are partly under test; regional structure (e.g. Bryc Oklahoma elevation) and directional sorting are real confounds. A generative model (absorbed fraction f + admixture timing → predicted modern NA %) is required before a sharper H2 likelihood is defensible.

## Supersession

An earlier aggressive encoding (H1=0.75, H2=0.10) lived briefly in this file and in the CSV. It overstated what the observation can carry. **Conservative values are now canonical.** File `stream31_bryc_na_ancestry.md` is historical/rationale only if retained; likelihoods in CSV + this file control the engine.

## Citation

Bryc K et al. The Genetic Ancestry of African Americans, Latinos, and European Americans across the United States. Am J Hum Genet. 2015;96(1):37–53. doi:10.1016/j.ajhg.2014.11.010
