# Quantitative Floor (Reliability ≈ 0)

> The mathematics used to score these quantities (Poisson counting, Beta rates, hierarchical hyperpriors) is standard.  
> What is deliberate is the epistemic rule: these are the only quantitative statements retained when administrative reliability → 0.


These quantities and lower bounds rest on primary physical and structural evidence.  
They do **not** depend on accepting administrative head-counts, growth rates, or import totals as accurate.  
They remain fully available when `victors_reliability → 0`.

All figures below are still **conditional estimates**, not facts. They are conditioned on the physical remains, the surviving non-owner records, and the measurable structure of the source base itself.

---

## 1. Physical presence (burial & aDNA)

Primary anchors:
- African Burial Ground (NYC) — NPS / GSA archaeological reports (estimated 15,000–20,000 interments of people of African descent, 17th–18th centuries).
- Catoctin Furnace (Harney et al., *Science* 2023) — 27 individuals; genetic links to tens of thousands of living people.
- Anson Street, Charleston (Fleskes et al., *PNAS* 2023) — 36 individuals.
- Chesapeake Bay 17th-century sites (*Current Biology* 2023) and additional documented grounds (Philadelphia, Colonial Williamsburg, Harlem fieldwork, Charleston GIS, etc.).

**Floor statement**: Multiple independent burial populations of African and mixed ancestry were interred on American soil across the 17th–19th centuries. The bodies themselves constitute lower-bound evidence of multi-generational presence that no administrative total can erase.

## 2. Genealogical termination pattern

Primary anchors:
- Freedmen’s Bureau records, church and county registers, plantation ledgers (as location-of-record evidence only), community projects (Whitney Plantation database, Monticello Getting Word, Georgetown Memory Project, 10 Million Names).

**Floor statement**: The large majority of *documented* lineages for the focal population terminate in U.S. records. This is a structural fact about the surviving paper trails, not a claim about the size of any national population.

## 3. Erasure index (structural silence)

Primary anchors:
- LOC WPA Slave Narratives (~2,300 interviews) + supplementary series and HBCU collections.
- Near-total absence of systematic *pre-1865, self-authored-in-the-moment* quantitative testimony by the enslaved population.
- Anti-literacy statutes, bans on assembly, legal non-personhood.
- **Partial counter-example (precision, not rebuttal)**: USCT pension files and Freedmen’s Bureau marriage registers — tens of thousands of sworn or self-reported statements about pre-1865 birth, age, kin, marriage, and sale, produced after emancipation. These make the silence *dated and scoped* (pre-1865 and contemporaneous self-authorship) rather than absolute. Stream 28 encodes this.

**Floor statement**: The volume of owner/trader/enumerator quantitative material vastly exceeds the volume of enslaved-authored quantitative material *produced under slavery*. The scarcity is not ordinary archival loss; it is the measurable result of legal regimes that prevented the creation of counter-records at the time. Post-emancipation sworn testimony (USCT pensions, Bureau marriages) is real and large; it does not erase the structural silence of the slavery period itself. The asymmetry remains evidence.

## 4. Regime intensity (legal & spatial)

Primary anchors:
- Colonial and state anti-literacy and anti-assembly laws.
- Virginia Racial Integrity Act (1924) and related classification statutes.
- Spatial distribution of documented burial grounds, slave-dwelling sites, and early free Black settlements.

**Floor statement**: A coercive legal and spatial regime operated across multiple colonies/states and generations. Its existence and geographic reach are documented independently of any single national head-count.

## 5. What this floor deliberately does *not* claim

- No replacement national population total for 1790 or 1860.
- No precise annual growth rate.
- No exact import volume after 1808.
- No conversion of any of the above into an “unbiased” census substitute.

The floor quantifies presence, continuity, erasure, and regime intensity on substrates that survive maximal skepticism about the administrative counts.

---

**Epistemic status**: These are the quantities that remain when the victor paperwork is set aside. They are the new quantitative starting point.

## 6. Formal link to the model (v4.7)

- Stream 27 (“Structural Silence / Erasure Index”) is coded `is_quantitative = 0`.
- It therefore remains fully weighted when `victors_reliability → 0`.
- The asymmetry (volume of owner/trader/enumerator quantitative material vs. near-absence of enslaved-authored quantitative material) is treated as positive structural evidence, not as a neutral gap.
- This is the first explicit encoding of absence as an informative contribution inside the inference layer.

## 7. Mechanism-relevant physical measurements (bodies & isotopes)

The current physical floor establishes **presence and continuity** but is largely silent on **mechanism** (H1 vs H2). The following measurement classes can change that without borrowing administrative head-counts. No published proportions or rates are asserted here until verified against the primary papers.

### 7.1 Bioarchaeological corpus (genuinely floor)

Larger than the aDNA-cited subset. Most of the skeletal series predate the genetics work:

| Source | Population / site | Relevance |
|--------|-------------------|-----------|
| Blakey & Rankin-Hill, *New York African Burial Ground Skeletal Biology Final Report* | NYABG technical corpus | Major skeletal biology behind the site already anchored; methodology also in Blakey, *Annual Review of Anthropology* |
| Rathbun (AJPA, 1980s–90s) | South Carolina plantation skeletal series | Regional plantation mortality and stress |
| Owsley | Catoctin Furnace skeletal analysis | Preceded Harney genetics; same population |
| Davidson | Freedman’s Cemetery, Dallas | Large post-emancipation series (*Historical Archaeology*) |
| Rose (ed.) | Cedar Grove, Arkansas | Documented series |
| Handler & Lange | Newton Plantation, Barbados | Comparative Caribbean baseline from bodies |

**Measurement classes from these series that bear on mechanism:**

- **Age-at-death distributions** (dental cementum annulation + standard osteology) → mortality / survivorship profile from bodies. Natural increase requires a specific survivorship shape; that is an H1 prediction testable without a census.
- **Entheseal changes & musculoskeletal stress markers** → labor intensity from skeletons. Regime-intensity currently rests on statutes (what was *permitted*); these record what was *done*.
- **Enamel hypoplasia, Harris lines, cribra orbitalia** → physical check on the childhood-stunting → adolescent-catch-up profile predicted under H1 / Stream 29.

### 7.2 Isotopes (genuinely floor; highest leverage for H1 vs H2)

| Work | Signal | Why it matters |
|------|--------|----------------|
| Goodman et al. | Sr and Pb at New York African Burial Ground | Childhood geology + colonial lead exposure |
| Schroeder et al. | Newton Plantation (Barbados) | Caribbean comparative |
| Laffoon | Caribbean baselines | Regional reference |
| Bastos et al. | Pretos Novos, Rio | South Atlantic comparative |
| Schroeder et al. 2015 (*PNAS*) | Genome-wide data from three 17th-c. African-born individuals at Saint Martin | Proof of concept: African-born status recoverable from remains — the exact H1-vs-H2 question |

Lead isotopes are worth treating separately: colonial-era exposure signatures can distinguish provenance where strontium is ambiguous.

**Status (unchanged discipline)**: Literature exists. Current published African-born vs American-born proportions, and any mortality or stress rates, must be verified against the latest papers before encoding as likelihood terms. No numbers are asserted here. Encoding from recall would reintroduce the hand-specified-cell problem the project has spent multiple versions removing.

### 7.3 Why this lets the floor speak to mechanism

Isotopes are the only measurement class that answers H1 vs H2 *on bodies*. The floor currently establishes presence and continuity and was excluded from mechanism ranking for that silence. Verified isotope (and related skeletal) terms are what would let it re-enter ranking legitimately, without borrowing a single census number.

---

## 8. Statutes and adjudication (genuinely floor)

Statutes are self-documenting; they survive r→0 by construction. Two additions with discriminating power:

| Work | Content | Why floor / why discriminating |
|------|---------|--------------------------------|
| Thomas Morris, *Southern Slavery and the Law, 1619–1860* | Systematic legal survey | Regime structure independent of head-counts |
| **Ariela Gross**, *Double Character* and *What Blood Won’t Tell* | Racial-determination trials | **Prioritize**. Adversarial court proceedings where racial classification was contested *in the record itself* — direct documentary evidence for H2’s mechanism, produced by a process with no interest in the census enumerator’s outcome. Rare. |

Gross is the closest thing to contemporaneous adversarial documentation of the classification process H2 posits. Candidate for a dedicated non-quantitative stream or floor term once the trial corpus is mapped.

---

## 9. Sites and material culture (genuinely floor)

Singleton (*The Archaeology of Slavery and Plantation Life*; *I, Too, Am America*); Heath (Poplar Forest); Fennell; Franklin.

Quarter counts, spatial distribution of slave-dwelling sites, and dendrochronological dating of standing structures are physical observables. The current `n_regime_jurisdictions` (or equivalent stipulated constant) can in principle be replaced by counted site inventories rather than remaining a fixed parameter.

---

## 10. Explicitly *not* floor (boundary discipline)

The following are valuable and often better-provenance *paper*, but they still route through documentary producers and are r-dependent. They belong in quantitative streams with their own provenance groups — not in the floor. Blurring this boundary is how a floor stops being a floor.

| Work | Why not floor |
|------|----------------|
| Kiple & King, *Another Dimension to the Black Diaspora*; Savitt, *Medicine and Slavery* | Disease / nutrition environment — relevant to whether exceptional NI was possible, but documentary |
| Hall, Louisiana Slave Database | Draws on notarial, church, and court records — different producers/incentives, still paper; own group candidate |
| Higman, *Slave Populations of the British Caribbean* | Canonical comparative baseline the U.S. differential rests on; stream 2 is coarse next to it — quantitative stream improvement, not floor |

---

## 11. What would move the model (priority order)

1. **Isotopes** — only measurement that answers H1 vs H2 on bodies; lets the floor re-enter mechanism ranking legitimately once figures are verified from the papers.
2. **Gross on racial-determination trials** — closest contemporaneous adversarial documentation of the classification process H2 posits.

Same discipline as §7: pull the actual papers before encoding anything. Direction for this map of candidates: Claude Opus 4.8. Published figures and likelihood values remain project responsibility after verification.
