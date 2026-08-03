# DNA / ancestry sample-size and model discipline

## Hard rules

1. **Report n, cohort, selection.** Never state a % as if measured on the full ~40M+ African American population unless that is literally the frame.
2. **SE-of-mean ≠ representativeness.** Large n shrinks sampling error *inside the cohort*; it does not fix who is in the cohort (self-ID, consumer genomics, category stayers).
3. **K-cluster admixture is a model.** 5–7 continental reference components are a low-rank fit to genotype data relative to chosen reference panels — not proof that historical populations “are” those boxes across space-time.
4. **Cluster % ≠ lookerism.** Enumerator race, statute, and reputation are not autosomal components. Do not identify administrative absorption (α_admin) with a “Native American” component (α_I channel).
5. **Extrapolating cohort mean → national essence is inference.** Label it as such or do not do it.


## Consumer ancestry method anchors

These first-party documents are useful as disclosures of how commercial ancestry estimates are constructed:

- [AncestryDNA, Ethnicity Estimate White Paper](https://www.ancestry.com/cs/dna-help/ethnicity/whitepaper) — marked “Last updated October 30, 2013”; its V2 description says that reference panels are necessary, that living samples are used as proxies when historical populations cannot be sampled, and that admixture and panel quality affect the estimate.
- [23andMe, Ancestry Composition Guide](https://www.23andme.org/ancestry/ancestry-composition-guide/) — marked “Updated September, 2025”; it reports more than 21,000 reference individuals and 78 populations, and describes phasing, segment-level classification, thresholds, and internal holdout testing.

Use these links to support the method-level claim that an ancestry percentage is conditional on a reference panel, population labels, algorithm, and uncertainty procedure. Do **not** use them as independent validation of Bryc et al., as evidence of birthplace or historical identity, or as support for national representativeness, population counts, or any TAST H1–H5 likelihood. The 23andMe holdout results are agreement with the vendor’s reference labels; the AncestryDNA page describes an older V2 system and should not be treated as a current product specification.


## Bryc-class figures (example)

| Item | Status |
|------|--------|
| Mean NA-component ~0.8% in cohort | In-sample summary under method M |
| n ~ 5,269 (Bryc 2015 order) | Tiny fraction of ~40M+ |
| Apply 0.8% to all African Americans | **Not a measurement** |
| Use as α_admin | **Invalid** (lookerism ≠ genome) |
| Use as α_I (retained in *this* self-ID cohort) | Narrow channel only |

## Required fields on any DNA claim in this repo

- n
- reference / cohort definition
- pct_of_reference_population (scientific notation if << 0.1%)
- selection mechanism (who is in / out)
- method (admixture K, panel, or haplogroup)
- what the number **supports**
- what it **cannot** support

## α split (see joint_alpha_model)

- **α_I**: constrained by modern cohort NA-component under stated model — publishable narrow claim.
- **α_admin**: administrative category motion under lookerism — **not** identified by NA%.

## Category exit (2026-07-24)

Observed cohort NA mean is a **lower bound** on historical retained Indigenous-associated
ancestry among lineages that remained in the self-ID sample. Symmetric SE-of-mean does
not model directional exit of high-NA tails. Joint model uses floor + exit_bias latent.

## Panel relativity of f_I

f_I is “fraction projecting onto NA component under reference panel P,” not “fraction
Indigenous in an 1800 ethnohistorical census.” Priors on f_I must respect that.
