# DNA / Genomic Reference Discipline

**Every DNA-derived claim in this repo must carry:**

1. **Sample size (n)** — the number of individuals whose genomes / ancient DNA /
   isotopes were actually measured in the cited study.
2. **Reference population** — the group the sample is being generalized to.
3. **Percentage of reference** — `n / reference_population_size`, computed
   explicitly.
4. **Study citation** with DOI or archival URL.
5. **What the sample can support** and **what it cannot support**.

Percentages small enough to be relevant (e.g. 0.000017% aDNA world coverage,
0.013% Bryc AA cohort, 0.126% Micheletti cohort) MUST be shown, not rounded to
"substantial" or "large."

Rationale: aDNA and consumer genotyping cohorts are the class of evidence that
survives `victors_reliability = 0` and therefore does load-bearing work in the
physical floor. Because they carry that weight, the sample base must be exposed
so that readers can see exactly how much of the reference population is (or
isn't) represented.

Adopted 2026-07-24. Credit: Claude Opus 4.8 review.

---

## The four questions a DNA-derived claim must answer

For any statement in this repo that cites DNA, aDNA, autosomal ancestry,
haplogroup frequency, isotope, or biological measurement:

**Q1. How many individuals were measured?** Give the integer `n`, not a range,
whenever the primary source is available. If a range is unavoidable, give the
minimum.

**Q2. What population is this sample being generalized to?** The reference
population must be named explicitly — "U.S. African-American population,"
"NYABG interred population," "worldwide aDNA record," etc. — and its size must
be stated in the same units as `n`.

**Q3. What fraction of the reference does the sample cover?** Compute
`n / reference_population_size` and show at least two significant figures.
If the fraction is smaller than 1%, show it in per-mille, per-hundred-thousand,
or scientific notation — do not round to zero.

**Q4. What is the sample selection mechanism?** Consumer-genotyping cohorts
have self-selection bias. aDNA cohorts are selected by burial ground,
preservation, and community consent. Isotope samples are selected by which
teeth survived and which permitted destructive analysis. The selection
mechanism must be stated, because it drives what the sample can and cannot
support.

---

## Standard reference-population sizes used in this repo

Update these when the U.S. Census or global population estimates change.

| Reference population | Size (approx.) | Source |
|----------------------|---------------|--------|
| U.S. self-identified African-American population (2020) | ~40,000,000 | U.S. Census Bureau 2020 (Black or African American alone or in combination: ~46.9M; alone: ~41.1M; TAST uses 40M as a round working number and flags departures) |
| U.S. total population (2020) | ~331,000,000 | U.S. Census Bureau 2020 |
| Global aDNA record (all sites, all periods, 2025) | ~15,000–20,000 individuals | Published aDNA literature 2025 (see sources_registry row 7) |
| Global human population (2025) | ~8,100,000,000 | UN DESA 2025 |
| Global historical human population (all humans ever) | ~117,000,000,000 (very rough) | Kaneda & Haub 2022 PRB; used in sources_registry row 9 |
| NYABG estimated interments (17th–18th c.) | 15,000–20,000 | NPS/GSA African Burial Ground reports |
| NYABG excavated / recovered individuals | 419 | GSA/NPS final report |
| Catoctin Furnace burial site | 27 (all excavated) | Harney et al. 2023 |
| Anson Street burial site | 36 (all excavated) | Fleskes et al. 2023 |
| Chesapeake Bay 17th-c. reported (Volgyi 2023) | 11 (3 African-ancestry) | Current Biology 2023 |
| 23andMe consumer cohort (as of 2024) | >12,000,000 | 23andMe public disclosures |
| AncestryDNA consumer cohort (as of 2024) | >23,000,000 | Ancestry public disclosures |
| Consumer DNA kits tested global (2019 figure, dated) | >26,000,000 | MIT Technology Review 2019 |
| 1000 Genomes Phase 3 African-American reference | 157 (ASW 61 + ACB 96) | 1000 Genomes Consortium, Nature 2015 |
| HGDP African reference panel | ~500 individuals across ~15 African populations | Human Genome Diversity Project |
| African Genome Variation Project | 1,481 individuals, 18 ethno-linguistic groups | Gurdasani et al. 2015 Nature |

---

## Standard entry template

Copy this template when adding a new DNA-derived fact to `observable_facts.yaml`
or a new stream to `evidence_streams.csv`. **Do not use aDNA/genetic evidence
without completing this block.**

```yaml
sample_size_discipline:
  primary_study:
    citation: <Author et al. YEAR Journal Volume:pages>
    doi_or_url: <DOI or archival URL>
    n_individuals: <integer>
    reference_population: <named population, e.g. "U.S. self-identified African-American population">
    reference_population_size: <integer or range>
    pct_of_reference: <n / reference * 100, shown to 2 sig figs; use scientific notation when < 0.001%>
    selection_mechanism: <consumer opt-in | community-engaged aDNA | census-linked | reference panel | isotope survivor | ...>
    what_it_supports:
      - <specific claim>
    what_it_cannot_support:
      - <specific claim that would require a larger or differently-selected sample>
  cross_checks:
    - citation: <second study>
      n_individuals: <integer>
      pct_of_reference: <>
      convergent_finding: <>
```

---

## Worked examples

### Bryc et al. 2015 (autosomal ancestry, Stream 31 / floor-09)

```
n_individuals: 5,269
reference_population: U.S. self-identified African-Americans
reference_population_size: ~40,000,000
pct_of_reference: 0.013% (5269 / 40,000,000 = 1.317e-4)
selection_mechanism: 23andMe consumer opt-in; U.S.-only
mean_native_american_ancestry: 0.8% (falsifies material-scale H2 reclassification)
```

### Harney et al. 2023 (Catoctin Furnace aDNA)

```
n_individuals: 27 (all excavated at site)
reference_population: NYABG-comparable enslaved-descendant U.S. sites
reference_population_size: unbounded (site-level, not national)
pct_of_reference: N/A — SITE-LEVEL evidence, not a population sample
selection_mechanism: burial-ground community engagement + preservation
what_it_supports:
  - physical presence of people of African descent at that site
  - genetic continuity (41,799 living genetic relatives identified via 23andMe)
what_it_cannot_support:
  - national head-count
  - national birthplace proportion
```

### Fleskes et al. 2023 (Anson Street aDNA)

```
n_individuals: 36 (all excavated); 18 with low-coverage genomes
reference_population: Charleston-area enslaved-descendant U.S. sites (17th–19th c.)
reference_population_size: unbounded (site-level)
pct_of_reference: N/A — SITE-LEVEL
selection_mechanism: Gullah Society community-engaged aDNA
what_it_supports:
  - presence
  - West/West-Central African genomic ancestry composition
  - community-engaged aDNA method
what_it_cannot_support:
  - birthplace proportion
  - H2 support via ancestry alone (formally rejected in verified_isotope_adna.yaml)
  - The fabricated '29 of 36 Lowcountry-born' claim was RETRACTED 2026-07-24
```

### Goodman NYABG isotope proxy (Stream 30)

```
n_individuals_in_chemical_sample: 32 (13 modified adults + 19 non-modified subadults)
n_individuals_at_site: 419 recovered from estimated 15,000–20,000 interments
reference_population: NYABG chemical sample only
pct_of_site_recovered: 32/419 = 7.6%
pct_of_estimated_interments: 32/15000 = 0.21% to 32/20000 = 0.16%
selection_mechanism: modified adults + young non-modified subadults (NOT random)
what_it_supports:
  - presence of both African-born and NY-born proxies in the chemical sample
  - method demonstration for isotope-based birthplace inference
what_it_cannot_support:
  - site-wide African-born percentage
  - national African-born percentage
encoded_conservative_k_over_n: k=13, n=32, p_hat=0.406 (chemical sample only)
```

### Ancient DNA world coverage (sources_registry row 9)

```
n_individuals: ~15,000–20,000 (published aDNA record global, all periods, 2025)
reference_population: All humans who have ever lived
reference_population_size: ~117,000,000,000 (very rough, Kaneda & Haub 2022)
pct_of_reference: ~1.7e-5% (0.000017%)
selection_mechanism: preservation + excavation + community consent + funding + technical extraction success
what_it_supports:
  - aDNA is possible on a rapidly growing sample base
what_it_cannot_support:
  - representative claims about most populations, most time periods, or most burial contexts
```

---

## Enforcement

- `evidence_streams.csv` rows that reference DNA / aDNA / autosomal ancestry / isotope / haplogroup MUST have a companion `.md` file in `model/` (e.g. `stream30_goodman_nyabg.md`, `stream31_autosomal_ancestry.md`) that fills out the four questions above.
- `observable_facts.yaml` facts of `type: physical_presence` whose evidence base is genomic MUST include a `sample_size_discipline:` block matching the template.
- Any narrative claim in `README.md`, `METHODS.md`, `surviving/*.md`, or `conventional/*.md` that cites a genomic study MUST show `n` and either `% of reference` or `SITE-LEVEL evidence, not a population sample`.
- The self-test in `bayesian_core.py --self-test` may be extended to grep for genomic claims without a sample-size block and warn. That check is future work; the discipline is enforced by review until then.

---

## What this discipline does NOT do

- It does not lower the epistemic status of small-n aDNA studies. The 27
  individuals at Catoctin Furnace are load-bearing physical evidence of
  presence and multi-generational continuity. Sample size discipline requires
  us to state what those 27 support and what they don't — not to downgrade
  them.
- It does not require all genomic claims to be national. Site-level claims
  are valid and clearly labeled as such.
- It does not enforce a minimum n. It enforces transparency about n.
- It does not treat consumer-genotyping cohorts as equivalent to random
  samples. Self-selection bias is stated up-front.

The rule is: **if a genomic number is doing work in this repo, its sample base
must be visible next to it.**
