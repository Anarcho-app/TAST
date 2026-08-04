# Artifact 01 — Staffer Brief

> Parallel 3–5 page companion to `01_continuous_harm_declaration_cba.md`, prepared per the legislative-readiness spec of Grok 4.5 Expert (xAI). Opens with the hardest-to-dismiss evidence, states the Declaration binary neutrally, presents only the baseline and inaction scenarios, and ends with questions for legislative counsel and scorekeepers.

| | |
|---|---|
| **Content** | Grok 4.5 Expert (xAI) — framework and spec |
| **Placement** | Anarcho-app (repository owner) |
| **Integration** | Sisyphus (qwen3.8-max-preview) |
| **Added** | 2026-08-04 |
| **Full document** | `01_continuous_harm_declaration_cba.md` in this directory |

---

## 1. The hardest-to-dismiss evidence (physical floor)

These observables do not depend on trusting any administrative record. They survive maximal skepticism of government head-counts, which is why they lead this brief. Confidence values are derived by the TAST confidence function (`model/derive_confidence.py`: source class × re-verifiability × sampled fraction) — function output as of 2026-08-04, not hand-assigned, parity-enforced by `scripts/check_observable_facts_parity.py`.

| Anchor | Derived confidence |
|---|---|
| Multi-generational presence on the territory prior to 1865 (`floor-08`) | 0.996 |
| Multiple burial grounds of African and mixed-ancestry individuals (17th–19th c.) (`floor-01`) | 0.996 |
| Published aDNA at U.S. sites (Catoctin Furnace MD, Anson Street SC, Chesapeake Bay) documenting West/West-Central African ancestry, variable European admixture, and parent–child kinship (`floor-03`) | 0.996 |
| New York African Burial Ground: estimated 15,000–20,000 interments; 419 excavated, analyzed, reinterred; National Monument (`floor-02`) | 0.996 |
| Genealogical chains for the focal population terminate in U.S. records (`floor-04`) | 0.807 |
| Colonial and state anti-literacy laws restricting self-authored records (`floor-05`) | 0.798 |

Osteological and isotopic evidence from these sites records hard labor, nutritional stress, and elevated mortality. The bodies are the testimony that no administrative file can condition away.

## 2. The administrative mechanism, briefly

The classification machinery is documented, continuous, and still operating:

- U.S. Census racial categories since 1790; enumerators commonly assigned race pre-1960; fractional "blood" categories in 1890; one-drop instructions in 1930.
- Virginia Racial Integrity Act (1924) and 1930 amendment: mandatory racial registration, felony for false registration, parallel hypodescent rules across multiple states into the mid-20th century.
- OMB Statistical Policy Directive No. 15 (2024 revision): seven minimum socio-political categories, explicitly **not** biological or genetic definitions; collection remains mandatory for many federal purposes, with non-response frequently imputed.
- Documented policy applications: slave schedules and property law, Jim Crow statutes, federal housing underwriting that priced racial composition as risk (1930s–1960s), differential access to New Deal, GI Bill, and early Social Security coverage.

The mechanism did not end; it changed form. That continuity is Premise 1 of the framework.

## 3. The Declaration binary, stated neutrally

Text (Declaration of Independence, 1776):

> Governments derive just powers from the consent of the governed. Whenever any form of government becomes destructive of the ends of life, liberty, and the pursuit of happiness, it is the right of the people to alter or to abolish it.

The framework's binary, stated without advocacy:

- **Premise 1** — forced racial taxonomy plus its documented applications constitutes continuing government-caused harm. This premise is observationally grounded in Sections 1–2 above.
- **Premise 2** — the alter-or-abolish clause is triggered by sustained failure to redress that harm. This premise is contestable: courts treat the Declaration as founding principle, not positive law that automatically voids authority upon non-redress.
- **Path A** — structured restorative investment, differentiated by intensity of exposure, with reciprocal fiscal returns.
- **Path B** — refusal while classification continues; legitimacy with respect to the most intensively affected population is placed in question; resource return, if it comes, arrives via rupture rather than ordinary politics, and its net outcome is uncertain.

This brief does not ask you to accept Premise 2. It asks you to know where the logic leads if a critical mass does, and what the cheaper alternative (Path A) would cost and return.

## 4. Two scenarios — ten-year and fifty-year

Only the two scenarios relevant to a legislative choice are shown. Constant annual net flows; annuity factors 8.530 (3% real, 10 yr), 7.722 (5% real, 10 yr), 25.73 (3% real, 50 yr), 18.26 (5% real, 50 yr). **Illustrative, not a score.**

| Scenario | Net annual | 10-yr cumulative | 10-yr NPV @ 3% | 10-yr NPV @ 5% | 50-yr NPV @ 3% |
|---|---|---|---|---|---|
| Baseline reciprocal (Path A) | +$120 B | +$1.2 T | +$1.0 T | +$0.9 T | +$3.1 T |
| Inaction (status quo) | –$600 B | –$6.0 T | –$5.1 T | –$4.6 T | –$15.4 T |

**What would have to be true — baseline scenario.** Annual reciprocal returns at 1.3× annual investment, sustained. External racial-equity literature cites multipliers of 1.2–2.0 when human-capital and health channels are included, so 1.3 is mid-range, not optimistic — but it requires functional delivery, measurable targets, and payroll-base feedback actually materializing (OASDI contributions ≈ 0.124 × covered-earnings growth).

**What would have to be true — inaction scenario.** The disparity drag persists at roughly $600 B/yr, within the $200 B–$1 T annualized range of cited estimates, and the administrative machinery keeps generating its own costs. If the drag is at the low end of that range, inaction is less costly than shown — the sweep band is the honest statement.

**Horizon note.** The 10-year window (the one Congress scores) captures under half the 50-year signal; returns that mature after year 10 (early-childhood and health cohorts) will systematically underscore inside it. Request scoring on both windows.

## 5. Modular levers (pick pieces, not the whole)

1. **Classification opt-out / "human" default** on federal forms, no service penalty.
2. **Time-limited pilot investments** tied to measurable disparity reduction, with sunset clauses.
3. **State/local experiments** suspending or replacing federal categories while measuring outcomes, on transparent open-source dashboards.
4. **Human-capital investments scored against reciprocal fiscal returns**, with scoring published alongside outlays.

Each lever stands alone. Carrying one does not require owning the entire framework.

## 6. Questions for legislative counsel / scorekeepers

1. **Baseline definition.** Can CBO/JCT score a Path A proposal against the continuing-drag baseline rather than a zero-cost status quo, and if not, what is the procedural route to an alternative baseline?
2. **Window discipline.** Which levers score positive inside a 10-year window, and what is the formal treatment of returns maturing beyond year 10 (early-childhood, health cohorts)?
3. **Feedback channels.** How would scorekeepers treat payroll-tax feedback (0.124 × ΔW) and reduced disability/SSI outlays — on the score, in a supplemental estimate, or not at all?
4. **Sunset structure.** What sunset/pilot drafting satisfies Budget Act points of order while preserving re-authorization against measured outcomes?
5. **Opt-out exposure.** Does a classification opt-out / "human" default create statutory or civil-rights-compliance exposure in any current mandate (SPD 15 and successor directives, grant conditions)?
6. **Evidence threshold.** What measured outcomes would justify re-scoring the inaction baseline upward or downward within a pilot horizon?
7. **Premise 2 status.** Counsel's view: the Declaration's alter-or-abolish clause as founding principle vs. positive law — and whether any justiciable legitimacy exposure exists under sustained non-redress, even if small.
8. **Sweep reporting.** Can scored estimates carry sensitivity bands (multipliers 0.6–2.0; drag $200 B–$1 T; discount 3%/5% real) rather than point values, consistent with the framework's TAST-compatible uncertainty discipline?

---

*Every administrative magnitude in this brief is a conditional estimate under the TAST rule; the physical floor of Section 1 is not. The full artifact carries the grounding appendix, the fiscal scorekeeping appendix, and the complete scenario sweep.*
