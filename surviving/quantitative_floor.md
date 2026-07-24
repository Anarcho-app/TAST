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

## 7. Mechanism-relevant physical measurements (next increment)

The current physical floor establishes **presence and continuity** but is largely silent on **mechanism** (H1 vs H2). Two measurement classes can change that without borrowing administrative head-counts:

### Isotopic and dental signals on existing burial populations
- Strontium and oxygen isotope ratios in tooth enamel record childhood geology and drinking water; they can distinguish African-born from American-born individuals directly from remains.
- Dental modification patterns and carbon isotope ratios (C₄ vs C₃ diets) supply independent origin and diet signals.
- African Burial Ground, Catoctin Furnace, Anson Street, and Chesapeake contexts already have published work in this area.  
- **Status**: Literature exists; current published African-born vs American-born proportions must be verified against the latest papers before encoding as likelihood terms. No numbers are asserted here until that verification.

### Skeletal stress markers
- Enamel hypoplasia, Harris lines, cribra orbitalia, and related markers from the same burial populations provide a physical check on the childhood-stunting → adolescent-catch-up profile predicted by H1 under Steckel-style anthropometrics (Stream 29).
- Two independent substrates (bodies vs shipper manifests) on the same morphological claim.

These measurements keep the floor’s commitment: they do not depend on census totals, growth rates, or import volumes. They are the highest-value addition that lets the floor speak to mechanism.
