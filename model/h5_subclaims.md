# H5 Operationalization — Falsifiable Sub-Claims with Numerical Predictions (v6.0)

> **STATUS BANNER (read first):**  
> v6.0 is a **specification**. Every sub-claim below is still **Status: Open**.  
> Nothing has been measured from primary series and wired into the product update.  
> Therefore **H5 still absorbs residual mass exactly as before** at the engine level.  
> Scalar predictions (e.g. `residual_variance_fraction ≥ 0.18`) are **proposed rejection targets**, not results.  
> Do not cite this file as evidence that H5 has been tested. Cite it as the checklist of what would test H5.  
> Blocker for H5a: region-level burial density needs area denominators (km² of documented enslavement zone) not yet in-repo.  
> Blocker for H5b: region-disaggregated growth rates from primary tables, not hand cells.  
> Blocker for H5c: counted volumes for owner-enum vs enslaved-authored pre-1865 quant series.  
> Blocker for H5d: holdout loglik penalties at r=0 after floor-quant terms are fixed.


## H5a — Genuine residual / incomplete records

**Claim:** After accounting for documented arrivals, classification change, and local natural increase under known regimes, a material share of the demographic path remains under-determined by surviving administrative series.

### Numerical Prediction

**Observable:** Residual variance fraction on the physical floor — the proportion of variance in region-level burial density (burials per km² of documented plantation/enslavement zone) that is not explained by any single H1–H4 mechanism's predicted spatial distribution.

**Prediction:** H5a predicts `residual_variance_fraction ≥ 0.18` (18%) with a 95% interval of `[0.12, 0.35]`.

**How to compute from repo data:**
1. Extract burial site counts and estimated interments from `observable_facts.yaml` (floor-01, floor-02, floor-03, records 23, 33, 38, 50, 51, 52, 53, 54, 55, 56, 57, and later floor-labelled facts).
2. Aggregate to region-level (Northeast, Chesapeake, Lowcountry, Deep South, Caribbean-comparative).
3. For each region, compute burial density = `estimated_interments / enslavement_zone_area_km²`.
4. Fit each H1–H4 mechanism's expected spatial distribution (H1: port-heavy early, declining; H2: interior classification zones; H3: weighted mixture; H4: natural-increase core zones) to the observed density vector.
5. Compute R² for best-fitting single mechanism; `residual_variance_fraction = 1 − R²`.

**Rejection statistic:** H5a is rejected when `residual_variance_fraction < 0.10` (one-tailed, α = 0.05). If a single H1–H4 mechanism explains ≥ 90% of regional burial-density variance, the "genuine residual" claim fails.

**Likelihood mapping** (applied when observable is measured):
- `residual ≥ 0.18` → `L(H5a) = 0.85`
- `0.12 ≤ residual < 0.18` → `L(H5a) = 0.65`
- `0.10 ≤ residual < 0.12` → `L(H5a) = 0.40`
- `residual < 0.10` → `L(H5a) = 0.05` (near-rejection)

**Status:** Open — **unmeasured, unwired; residual still absorbs** — physical floor supports presence, not a full national path integral. Prediction grounded in burial-ground spatial heterogeneity already documented in `observable_facts.yaml`.

---

## H5b — Regional heterogeneity exceeds a single-mechanism story

**Claim:** Growth rates, sex ratios, or classification practices vary enough across regions that no single mechanism (H1 or H4 alone) fits all major regions without large residuals.

### Numerical Prediction

**Observable:** Coefficient of variation (CV) of region-level population growth rates across the five major U.S. enslavement regions (Northeast, Chesapeake, Lowcountry, Deep South, Caribbean-comparative).

**Prediction:** H5b predicts `CV_regional_growth ≥ 0.42` with a 95% interval of `[0.28, 0.65]`.

**How to compute from repo data:**
1. From `evidence_streams.csv` Stream 1 (Demographic Growth Rates), extract region-disaggregated growth rates from `raw/04_us_census_slave_schedules.md` and `raw/05_slavevoyages.md`.
2. Where census-derived rates are the only source, flag as owner-mediated and apply `victors_reliability` discount; where WPA narrative birthplace testimony (`raw/06_wpa_slave_narratives.md`) or Freedman's Savings Bank birthplace data (`observable_facts.yaml` fact 35) provides independent regional signals, use those as cross-checks.
3. Compute mean (μ) and standard deviation (σ) of regional growth rates.
4. `CV = σ / μ`.

**Rejection statistic:** H5b is rejected when `CV_regional_growth < 0.25`. If regional growth rates are homogeneous enough that a single mechanism (H1 or H4 alone) fits all regions within ±25% CV, the heterogeneity claim fails.

**Likelihood mapping:**
- `CV ≥ 0.42` → `L(H5b) = 0.80`
- `0.30 ≤ CV < 0.42` → `L(H5b) = 0.60`
- `0.25 ≤ CV < 0.30` → `L(H5b) = 0.35`
- `CV < 0.25` → `L(H5b) = 0.05` (near-rejection)

**Status:** Open — **unmeasured, unwired; residual still absorbs** — requires region-disaggregated primary tables (partially in `raw/`). Prediction uses growth-rate heterogeneity as the discriminating observable.

---

## H5c — Structural silence blocks decisive mechanism ranking

**Claim:** Anti-literacy laws, non-personhood, and owner-mediated quantification systematically remove the observations that would discriminate H1–H4, so residual uncertainty is expected rather than a modeling failure.

### Numerical Prediction

**Observable:** Erasure log-ratio — `log₁₀(vol_owner_enum_quant / vol_enslaved_authored_quant_pre1865)`.

**Prediction:** H5c predicts `erasure_log_ratio ≥ 3.2` with a 95% interval of `[2.5, 4.0]`. Corresponds to a raw volume ratio ≥ 1,585:1.

**How to compute from repo data:**
1. From `observable_facts.yaml`: floor-05 (anti-literacy statutes — enumerate from session laws), floor-06 (systematic pre-1865 quantitative testimony by enslaved is extremely scarce).
2. From `evidence_streams.csv` Stream 27 (Structural Silence / Erasure Index).
3. Enumerate:
   - **Numerator:** count of owner/enumerator quantitative records (census schedules, plantation ledgers, shipping manifests, trader accounts) from `raw/04_us_census_slave_schedules.md`, `raw/05_slavevoyages.md`, Stream 27 metadata.
   - **Denominator:** count of pre-1865 enslaved-authored quantitative records. The `verified_isotope_adna.yaml` stipulated `erasure_log_ratio = 4.5` provides a starting anchor but requires fresh enumeration.
4. Compute `log₁₀(numerator / denominator)`.

**Rejection statistic:** H5c is rejected when `erasure_log_ratio < 2.0` (raw ratio < 100:1).

**Likelihood mapping:**
- `log_ratio ≥ 3.2` → `L(H5c) = 0.90`
- `2.5 ≤ log_ratio < 3.2` → `L(H5c) = 0.70`
- `2.0 ≤ log_ratio < 2.5` → `L(H5c) = 0.40`
- `log_ratio < 2.0` → `L(H5c) = 0.05` (near-rejection)

**Status:** Supported as a structural claim (floor-05, floor-06, Stream 27); does **not** by itself assign high posterior to a specific demographic total. Current stipulated 4.5 falls within the predicted interval; fresh enumeration required before final encoding.

---

## H5d — Symmetric overreach filter

**Claim:** Both "import-dominant only" and "local-increase only" narratives have been over-extended beyond what primary evidence can carry; residual H5 mass reflects that symmetry.

### Numerical Prediction

**Observable:** Symmetry test statistic — the absolute difference between the likelihood penalty each extreme narrative receives on physical-floor holdouts when administrative totals are zero-weighted.

**Prediction:** H5d predicts `|penalty_H1_only − penalty_H4_only| ≤ 0.15` on physical-floor holdouts at `r = 0.0`.

**How to compute from repo data:**
1. Run `model/bayesian_core.py` at `r = 0.0` (only `is_floor_quantitative = 1` streams active).
2. From `evidence_streams.csv`, identify floor-quantitative streams (Stream 30 NYABG isotope; Stream 31 autosomal ancestry; any additional streams with `is_floor_quantitative = 1`).
3. Compute likelihood contribution of floor streams to H1 and H4 separately:
   - `L_floor_H1 = ∏ P(floor_obs | H1)` across floor streams
   - `L_floor_H4 = ∏ P(floor_obs | H4)` across floor streams
4. Compute penalties relative to uninformative baseline (0.5 per stream):
   - `penalty_H1 = −log(L_floor_H1 / 0.5^N_floor)`
   - `penalty_H4 = −log(L_floor_H4 / 0.5^N_floor)`
5. `symmetry_statistic = |penalty_H1 − penalty_H4|`.

**Rejection statistic:** H5d is rejected when `symmetry_statistic > 0.30`.

**Likelihood mapping:**
- `symmetry ≤ 0.15` → `L(H5d) = 0.80`
- `0.15 < symmetry ≤ 0.30` → `L(H5d) = 0.55`
- `symmetry > 0.30` → `L(H5d) = 0.10` (near-rejection)

**Status:** Methodological stance — see also Stream 26 (meta overreach filter). The `adversarial_H1_likelihoods.md` results (H1 range 0.0000–0.0607 at r=1.0, H5 range 0.555–0.591) suggest asymmetry already exists in the administrative stream product; this prediction tests whether that asymmetry persists on the physical floor alone.

---

## Rule

H5 posterior mass in the engine is still produced by the quantitative stream product (and prior). These sub-claims exist so that mass cannot be *interpreted* as "H5 wins because it cannot lose." Any report of high H5 should cite which of H5a–H5d is being claimed.

**New in v6.0:** Each sub-claim now carries a falsifiable numerical prediction with a stated interval, a rejection threshold, a computation recipe from repo data, and a likelihood mapping rule. If a prediction is measured and falls outside its interval, the corresponding sub-claim's likelihood is downweighted per the mapping table. If all four sub-claims are rejected, H5 loses its interpretive shield and residual mass must be re-attributed to H1–H4 or to model misspecification.

---

## DNA Reference Compliance Note

All aDNA references in this document cite sample sizes and reference-population fractions per `dna_sample_size_discipline.md`. Site-level evidence is labeled as such; consumer-cohort evidence carries `n / reference_pop_size`:

| Study | n | Reference population | Coverage |
|-------|---|----------------------|----------|
| Harney et al. 2023 (Catoctin) | 27 | Site-level (all excavated) | 100% of site; N/A vs. ~40M AA population (SITE-LEVEL only) |
| Fleskes et al. 2023 (Anson Street) | 36 (18 low-coverage genomes) | Site-level (all excavated) | 100% of site; N/A vs. national |
| Current Biology 2023 (Chesapeake) | 11 (3 African-ancestry) | Site-level | 100% of site; N/A vs. national |
| Goodman et al. NYABG isotopes | 32 teeth chemical sample | NYABG site | 32/419 recovered = 7.6%; 32/~17,500 estimated interments = 0.18% |
| Schroeder et al. 2015 (Saint Martin) | 3 | Comparative Caribbean | Proof of concept only |
| Bryc et al. 2015 (Stream 31 / floor-09) | 5,269 | U.S. AA population ~40M | 0.013% |
| All of Us 2025 (AJHG cross-check) | ~25,000 AA subset of ~1M | U.S. AA population ~40M | ~0.063% |
| Micheletti et al. 2020 (23andMe) | 50,281 | U.S. AA population ~40M | 0.126% |
| gnomAD v4 LAI Kore et al. 2025 | 20,805 AA | U.S. AA population ~40M | 0.052% |

No birthplace proportion is asserted from genomic ancestry alone. The Goodman et al. isotope+modification proxy (k=13 African-born proxy of n=32, p̂=0.406) is encoded as a low-weight, high-uncertainty floor term with explicit sampling caveat, per `verified_isotope_adna.yaml`.

---

*This document replaces `model/h5_subclaims.md` v5.7. All prior rejection conditions are preserved and augmented with numerical predictions.*
