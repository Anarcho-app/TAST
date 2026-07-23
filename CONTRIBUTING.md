# Contributing to TAST Skepticism-First Edition

## Core principles

1. **Reliability is explicit.** Any numerical claim must be conditioned on a stated `victors_reliability` value.

2. **Estimates from biased administrative records are never facts.**  
   Language that converts them into facts is forbidden under `--strict` (default on):
   - “least-bad sources”, “best available”, “robust after correction / adjustment”
   - “the historical consensus”, “accepted / established / known fact”, etc.

3. **Population framing discipline.**  
   The focal population is **multi-generational American lineages of African and mixed ancestry** (Freedmen’s Bureau-era and earlier U.S. lineages whose genealogical chains predominantly terminate in pre-1865 U.S. records).  
   - Continental-African framing is **not** the unmarked identity label for this group.  
   - Reserve “African-descent / continental African origin” language for explicit discussions of documented transatlantic arrivals or genetic reference panels, always conditioned.  
   - Reject phrasing that collapses the multi-generational U.S. group into a perpetual proxy for the African continent.

4. **Surviving claims must not depend on administrative head-counts.** If a claim requires accepting census totals, growth rates, or import volumes as accurate, it belongs in the reweighted layer, not the surviving layer.

5. **Provenance and scope are visible.** Every stream and raw source should carry a provenance tag, an “Enslaved voice?” indicator, and (where relevant) a scope tag: multi-generational U.S. lineages / documented arrivals / administrative category only / genetic reference.

6. **Independence is a known limitation.** The current engine multiplies likelihoods under an independence assumption. Future contributions that introduce correlation structure or hierarchical models are welcome.

## Required disclaimer on quantitative output

Every quantitative claim must carry (or be immediately preceded by):

> CONDITIONAL ESTIMATE derived from biased administrative records (victors’ paperwork). This is NOT A FACT.

## Hypothesis labels (v4.4)

Hypotheses are scoped to processes on American soil or to documented arrival cohorts. None treat “African origin” as the unmarked residual category for the multi-generational population:

- H1: Documented transatlantic arrivals + exceptional natural increase under U.S. conditions
- H2: Classification / absorption processes operating on American soil
- H3: Hybrid mechanisms (partial absorption + moderate structural advantage on American soil)
- H4: U.S.-specific structural conditions (natural increase via local regime features)
- H5: Mixed / undocumented mechanisms (honest uncertainty; residual includes possibility that administrative categories obscure distinct American trajectories)

## Adding or changing an evidence stream

1. Edit `model/evidence_streams.csv`.
2. Set `is_quantitative` = 1 if the stream’s discriminating power depends on accepting administrative counts; = 0 otherwise.
3. Likelihoods must lie in [0.0, 1.0].
4. Run:
   ```bash
   python model/bayesian_core.py --self-test
   python model/bayesian_core.py --reliability 0.0
   python model/bayesian_core.py --reliability 1.0
   ```
5. Document the change in `VERSION.md`.

## Quantitative floor (reliability ≈ 0)

Primary-linked lower bounds and structural metrics live in `surviving/quantitative_floor.md`. Additions must rest on physical or structural primaries and must not re-introduce administrative head-counts as if they were facts.

## Changing surviving claims

Edit `surviving/qualitative_claims.md`. Keep the numbered list format. Re-run `--self-test`.

## Rejection criteria

Any contribution that:

- presents a number derived from the administrative records as a fact, or
- relies on “least-bad sources” (or equivalent) language to imply factual status, or
- uses continental-African framing as the primary / unmarked descriptor of the multi-generational U.S. group,

will be rejected.
