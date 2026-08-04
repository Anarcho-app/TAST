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
- **Path B** — refusal while classification continues; legitimacy with respect to the most intensively affected population is placed in question; resource return, if it comes, arrives via rupture rather than ordinary politics, and its net outcome is uncertain. *Path B is presented only as the logical residual if sustained non-redress continues; it is not a recommendation.*

This brief does not ask you to accept Premise 2. It asks you to know where the logic leads if a critical mass does, and what the cheaper alternative (Path A) would cost and return.

## 4. Two scenarios — ten-year window first

Only the two scenarios relevant to a legislative choice are shown. **Illustrative, not a score.** Model-dependent inputs carry their sweep bands inline; the NPV arithmetic converting them is exact and repo-gated.

### Primary: 10-year budget window (the one Congress scores)

Constant annual net flows; annuity factors 8.530 (3% real) and 7.722 (5% real).

| Scenario | Net annual (model-dependent) | 10-yr cumulative | 10-yr NPV @ 3% | 10-yr NPV @ 5% |
|---|---|---|---|---|
| Baseline reciprocal (Path A) | +$120 B (multiplier 1.3×; sweep 0.6–2.0) | +$1.2 T | +$1.0 T | +$0.9 T |
| Inaction (status quo) | –$600 B (drag estimate; sweep $200 B–$1 T) | –$6.0 T | –$5.1 T | –$4.6 T |

**Plain English — baseline scenario.** This assumes each invested dollar returns $1.30, sustained across the window (mid-range of the 1.2–2.0 band cited in the literature); if returns are only 1.0× instead, the 10-year net is roughly $0, and if 0.6×, roughly –$1.0 T — still better than inaction.

**Plain English — inaction scenario.** This assumes the disparity drag persists near $600 B/yr; if the drag is only $200 B/yr (the low end of the cited band), the 10-year cost is roughly –$1.7 T instead of –$5.1 T — still negative, still compounding.

### Secondary: 50-year reference horizon

| Scenario | 50-yr NPV @ 3% | 50-yr NPV @ 5% |
|---|---|---|
| Baseline reciprocal (Path A) | +$3.1 T | +$2.2 T |
| Inaction (status quo) | –$15.4 T | –$11.0 T |

**Horizon note.** The 10-year window captures under half the 50-year signal; returns that mature after year 10 (early-childhood and health cohorts) will systematically underscore inside it. Request scoring on both windows.

## 5. Modular levers (pick pieces, not the whole)

Each lever stands alone, with its operational shape in brief. Carrying one does not require owning the entire framework.

1. **Classification opt-out / "human" default** on federal forms, no service penalty. *OMB + collecting agencies; pilot two or three forms, then government-wide rulemaking; three-year review with a zero-service-penalty trigger; administrative/discretionary cost only.*
2. **Time-limited pilot investments** tied to measurable disparity reduction, with sunset clauses. *Existing grantmaking agency by domain (HHS/DOE/HUD/DOL); 5–10 jurisdiction pilot cohort; five-year sunset with independent metric review pre-registered at authorization; discretionary, time-limited, scores inside the 10-year window.*
3. **State/local experiments** suspending or replacing federal categories while measuring outcomes, on transparent open-source dashboards. *States/municipalities with federal waiver authority; federal categories run in parallel so national series stay continuous; each experiment carries its own sunset; state/local funds plus small federal technical assistance.*
4. **Human-capital investments scored against reciprocal fiscal returns**, with scoring published alongside outlays. *Existing program agencies; CBO/JCT score outlays and revenue effects separately; Treasury/SSA track the payroll channel (0.124 × covered-earnings growth); cohort-phased; discretionary outlays with mandatory feedback booked as revenue/savings effects, never netted.*

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
