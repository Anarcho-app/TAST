# Observable Facts (Physical & Structural Floor)

These are the statements closest to clear observables that survive maximal skepticism of administrative head-counts.

Administrative national totals are **not** treated as facts here.

**Confidence values in this file are the output of `model/derive_confidence.py`** (0.40·source_class + 0.35·re_verifiability + 0.25·sampled_fraction; weights declared in `data/confidence_function.yaml` and enforced by the constants gate), computed against `data/observable_facts.yaml` as of 2026-08-04. No hand-assigned confidence appears in this file; parity is enforced by `scripts/check_observable_facts_parity.py`.

Total scored facts: 29 · High confidence (derived c ≥ 0.85): 19

---

**Strict filter applied (v4.2)**: Claims that depend on accepting the numerical U.S. vs. Caribbean/Brazilian growth differential have been removed or rephrased. Only claims that can stand without treating the administrative head-counts as accurate are retained.

Framing note (v4.4): The focal population is multi-generational American lineages of African and mixed ancestry (Freedmen's Bureau-era and earlier U.S. lineages). Continental-African identity is not the unmarked label for this group.

See also: `quantitative_floor.md` — primary-linked lower bounds and structural metrics that remain available at reliability ≈ 0.

---

## High-confidence observables (derived c ≥ 0.85)

- **[0.996]** Multiple burial grounds containing remains of people of African and mixed ancestry exist on the territory that became the United States (17th–19th centuries). (`floor-01`)
  - Source: NPS African Burial Ground; Harney et al. Science 2023; Fleskes et al. PNAS 2023; Chesapeake aDNA studies
  - Type: `physical_presence` · Provenance: Physical archaeological + aDNA

- **[0.996]** African Burial Ground (New York) contains an estimated 15,000–20,000 interments of people of African descent (late 17th–18th centuries). — `15,000–20,000 (estimate)` (`floor-02`)
  - Source: NPS / GSA African Burial Ground reports
  - Type: `physical_presence` · Provenance: Physical archaeological

- **[0.996]** Published aDNA has been recovered from historical individuals of African and mixed ancestry interred at U.S. sites including Catoctin Furnace, Anson Street (Charleston), and Chesapeake Bay 17th-century contexts. (`floor-03`)
  - Source: Harney et al. Science 2023; Fleskes et al. PNAS 2023; Current Biology 2023
  - Type: `physical_presence` · Provenance: Lab-derived aDNA + physical remains; community-engaged

- **[0.996]** People of African and mixed ancestry were present on the territory that became the United States for multiple generations prior to 1865. (`floor-08`)
  - Source: Convergent physical, genealogical, and documentary evidence
  - Type: `physical_presence` · Provenance: Physical + genealogical + documentary

- **[0.996]** Autosomal Native American ancestry in self-identified African-Americans is trace-level (mean ~0.5–2%), independent of owner/enumerator/shipping records. (`floor-09`)
  - Source: Bryc et al. 2015 (AJHG); Baharian et al. 2016 (Nature Comms); Micheletti et al. 2020 (AJHG); All of Us (AJHG Jun 2025); gnomAD v4 LAI (Kore et al. 2025)
  - Type: `physical_presence` · Provenance: Lab-derived autosomal genotyping; participant-opt-in cohorts; NOT owner-mediated

- **[0.996]** African Burial Ground (Manhattan) — `15,000+ estimated burials` (`23`)
  - Source: National Park Service
  - Type: `observable_candidate` · Provenance: Archaeological + federal records

- **[0.996]** 15,000-20,000 estimated burials; skeletal analysis + artifacts (1690s-1794) — `15,000-20,000 burials` (`33`)
  - Source: New York African Burial Ground Archaeological Reports (full GSA/NPS reports)
  - Type: `observable_candidate` · Provenance: Federal archaeological excavation

- **[0.996]** Harlem African Burial Ground fieldwork — `Phase completion (2024-2025); archaeological recovery of remains` (`50`)
  - Source: NYCEDC/AKRF (2025 report)
  - Type: `observable_candidate` · Provenance: Archaeological excavation

- **[0.996]** First African Baptist Church Cemetery, Philadelphia: ~140+ burials excavated (2023-2024); 18th-19th century free & enslaved Black community — `~140+ burials` (`58`)
  - Source: Various press reports + forthcoming publication
  - Type: `observable_candidate` · Provenance: Archaeological excavation; urban redevelopment context

- **[0.996]** Colonial Williamsburg enslaved cemetery GPR surveys: ground-penetrating radar mapping of unmarked enslaved burials across multiple plantation sites (`59`)
  - Source: Colonial Williamsburg Foundation ongoing projects
  - Type: `observable_candidate` · Provenance: Archaeological remote sensing

- **[0.996]** Pine Street African & African American Burial Ground, Kingston NY: 18th-century; colonial "Colored" category included Indigenous + multi-ethnic individuals — `Est. hundreds of burials` (`60`)
  - Source: Diamond (2006), Northeast Historical Archaeology 35(1):47-62
  - Type: `observable_candidate` · Provenance: Archaeological + historical records

- **[0.996]** Cedar Key Cemetery, Florida: African American section GPR survey; community-engaged archaeology in majority-White rural setting (`61`)
  - Source: González-Tennant & González-Tennant (2024)
  - Type: `observable_candidate` · Provenance: Archaeological GPR survey

- **[0.996]** Belmont Cemetery, Nashville TN: enslaved burial ground; ongoing preservation — `Estimated 500+ burials` (`62`)
  - Source: Nashville historical/preservation records
  - Type: `observable_candidate` · Provenance: Archaeological + community records

- **[0.996]** Montpelier (James Madison): enslaved community burial ground; descendant-directed research since 2014 — `~150+ estimated burials` (`63`)
  - Source: Montpelier Foundation
  - Type: `observable_candidate` · Provenance: Archaeological excavation + descendant engagement

- **[0.996]** African Burial Ground National Monument NYC expanded: 419 recovered; 10,000-20,000+ estimated total; community-directed research (Howard Univ.) — `419 recovered; 10,000-20,000 est.` (`67`)
  - Source: GSA/NPS/Howard University reports
  - Type: `observable_candidate` · Provenance: Federal excavation; community-directed

- **[0.996]** Harlem African Burial Ground expanded: June 2024-Sept 2025 fieldwork completed; full site mapped; analysis beginning 2026 — `Complete site recovery` (`68`)
  - Source: NYCEDC + HABGI (2025)
  - Type: `observable_candidate` · Provenance: Archaeological excavation; descendant-directed

- **[0.996]** Montgomery NY African Burial Ground: est. 500 individuals; earliest burial 1756; colonial "Colored" = mixed classification (`69`)
  - Source: Sandy (2024), archaeological surveys
  - Type: `observable_candidate` · Provenance: Archaeological; magnetometry + GPR

- **[0.958]** ~179k men physically mustered into the U.S. Colored Troops (1863–1866); self-presentation at muster. (`agg-usct-enlistment`)
  - Source: NARA RG 94 (USCT muster rolls); RG 105
  - Type: `administrative_process` · Provenance: Federal muster rolls (men physically present, not owner-classified)

- **[0.956]** Freedmen's Bureau processed ~4M ration issuances / labor contracts / refugee registrations (1865–1869); bodies physically present. (`agg-bureau-rations`)
  - Source: NARA RG 105 (Freedmen's Bureau field office records)
  - Type: `administrative_process` · Provenance: Federal post-emancipation logistics (rations issued to people physically present)

---

## Scored below the high-confidence threshold

Derived values below 0.85 are not quality judgments on the underlying evidence. The function scores claim-type and coverage: specific samples (n of a reference population) score lower on `sampled_fraction` than aggregate existence claims, and administrative-process claims score lower on `source_class` by the anti-lookerism rule. The ordering is the function's output, swept in `model/PRIOR_SENSITIVITY.md`.

- **[0.838]** 1860 U.S. census slave schedules + free colored counts aggregate to ~4M persons of African descent (enumerator-classified). (`agg-1860-census`)
  - Source: 1860 U.S. census (NARA)
  - Type: `administrative_process` · Provenance: Federal enumerator classification (appearance-assigned, not self-reported). Common ground across H1–H4 (LR ≈ 1); composition discriminates, not the total.

- **[0.836]** Racial classification on U.S. censuses and vital records for the relevant period was primarily enumerator-driven rather than self-reported. (`floor-07`)
  - Source: U.S. Census instructions and historical methodology literature
  - Type: `administrative_process` · Provenance: Administrative / methodological

- **[0.807]** The large majority of documented genealogical chains for the focal multi-generational U.S. population terminate in U.S. records (church, county, plantation, Freedmen's Bureau, community projects). No measured national fraction is asserted. (`floor-04`)
  - Source: Freedmen's Bureau records; community genealogical projects (Getting Word, Whitney, etc.)
  - Type: `genealogical_structure` · Provenance: Genealogical / documentary location-of-record

- **[0.798]** Colonial and state anti-literacy laws and related statutes restricted enslaved people's ability to create and preserve their own quantitative records. (`floor-05`)
  - Source: Colonial and state session laws; legal-historical literature
  - Type: `structural_silence` · Provenance: Legal / statutory

- **[0.798]** Systematic pre-1865 quantitative testimony authored by the enslaved population is extremely scarce relative to the volume of owner, trader, and enumerator quantitative material. (`floor-06`)
  - Source: Comparative volume of surviving record classes; WPA collection as post-bellum and limited
  - Type: `structural_silence` · Provenance: Structural / archival asymmetry

- **[0.750]** Community-engaged aDNA reveals diverse origins of 18th-century Charleston African descendants — `Low-coverage aDNA from 18 of 36 individuals at Anson Street African Burial Ground` (`52`)
  - Source: Fleskes et al. (2023), *PNAS* 120(3):e2201620120
  - Type: `observable_candidate` · Provenance: Lab-derived aDNA; community-engaged (Gullah Society of Charleston)

- **[0.750]** Chesapeake Bay 17th-c. expanded: ancestry-segregated burial groupings confirm racial classification applied even in death — `11 individuals (8 European-ancestry, 3 African-ancestry)` (`55`)
  - Source: Current Biology 33(13), 2023
  - Type: `observable_candidate` · Provenance: Lab-derived aDNA; archaeological context

- **[0.750]** Catoctin Furnace expanded: study linking historical aDNA to a modern commercial ancestry platform; reports 41,000+ database matches to living participants — `27 individuals` (`56`)
  - Source: Harney et al. (2023), Science 381(6657)
  - Type: `observable_candidate` · Provenance: Lab-derived aDNA; community-engaged; linked to modern platform

- **[0.750]** Estate Little Princess Archaeology Project (St. Croix, USVI): Danish colonial enslaved remains; bioarchaeological + aDNA; comparative Caribbean enslaved population (`57`)
  - Source: Norton & Fleskes, various publications (2019-2024)
  - Type: `observable_candidate` · Provenance: Lab-derived aDNA; community-engaged model. Comparative control (not U.S. territory).

- **[0.376]** ~388k documented transatlantic import arrivals to the territory that became the U.S. (customs / manifests; over-records if anything). (`agg-import-ceiling`)
  - Source: SlaveVoyages (slavevoyages.org); customs records
  - Type: `administrative_process` · Provenance: Trader / customs manifests. Lowest scored entry by design: trader-mediated provenance.

---

## Unscored context entries (no derived confidence)

The following entries are retained in `data/observable_facts.yaml` as `non_scoring` context (provenance retained, no scoring path). They carry **no confidence value** because the derived-confidence rule does not score them; listing one would be a hand-assigned number.

- Excavations + surveys of enslaved cemeteries (e.g., Hermitage, Mount Vernon) (`38`) — Source: Andrew Jackson's Hermitage Enslaved Cemetery + Mount Vernon Slave Memorial Reports · Provenance: Archaeological digs
- Genetic legacy of African Americans from Catoctin Furnace (`51`) — Source: Harney et al. (2023), *Science* 381(6657):eade4995 · Provenance: Lab-derived aDNA; community-engaged; linked to modern ancestry database
- Historical genomes elucidate European settlement and the African diaspora at 17th-century Chesapeake Bay (`53`) — Source: *Current Biology* 33(13), 2023 · Provenance: Lab-derived aDNA; archaeological context
- Anson Street (Charleston) ASABG: Fleskes et al. 2023 report 36 individuals and low-coverage genomic data for 18; published work addresses West/West-Central African ancestral connections. Birthplace proportions are NOT asserted here — the "29 of 36 Lowcountry-born" figure was previously flagged as fabricated and removed (v5.9.11). (`54`)
- Great Dismal Swamp maroon communities: sustained ~1700s–1860s; escaped enslaved + Indigenous + others (`152`) — Source: Sayers (2014) "A Desolate Place for a Defiant People" · Provenance: Archaeological

---

**Epistemic status**: These claims are qualitative and structural. They survive the zero-weight mode because they do not require accepting any particular numerical total from the administrative record as accurate. They form the floor of what can be said with relatively high confidence once the quantitative reconstructions are set aside. Confidence ordering above is the derived-confidence function's output — challenge the function (one swept file), not individual numbers.
