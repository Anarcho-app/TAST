# Contributing to TAST Skepticism-First Edition

## Core principles

1. **Reliability is explicit.** Any numerical claim must be conditioned on a stated `victors_reliability` value.
2. **Estimates from biased administrative records are never facts.**  
   Language that converts them into facts is forbidden:
   - “least-bad sources”
   - “best available”
   - “robust after correction / adjustment”
   - “the historical consensus”
   - any equivalent that restores factual status to a conditional estimate.
3. **Surviving claims must not depend on administrative head-counts.** If a claim requires accepting census totals, growth rates, or import volumes as accurate, it belongs in the reweighted layer, not the surviving layer.
4. **Provenance is visible.** Every stream and raw source must carry a provenance tag and an “Enslaved voice?” indicator.
5. **Independence is a known limitation.** The current engine multiplies likelihoods under an independence assumption. Future contributions that introduce correlation structure or hierarchical models are welcome.

## Required disclaimer on quantitative output

Every quantitative claim emitted by the model or appearing in documentation must carry (or be immediately preceded by) language equivalent to:

> CONDITIONAL ESTIMATE derived from biased administrative records (victors’ paperwork). This is NOT A FACT.

The code enforces this under `--strict` (default on).

## Adding or changing an evidence stream

1. Edit `model/evidence_streams.csv`.
2. Set `is_quantitative` = 1 if the stream’s discriminating power depends on accepting administrative counts; = 0 otherwise.
3. Likelihoods must lie in [0.0, 1.0]. Prefer the existing soft caps unless you have a strong justification.
4. Run:
   ```bash
   python model/bayesian_core.py --self-test
   python model/bayesian_core.py --reliability 0.0
   python model/bayesian_core.py --reliability 1.0
   ```
5. Document the change in `VERSION.md`.

## Changing surviving claims

Edit `surviving/qualitative_claims.md`. Keep the numbered list format so the loader can parse it. Re-run `--self-test`.

## Testing

```bash
cd model
python bayesian_core.py --self-test
python bayesian_core.py --reliability 0.0
python bayesian_core.py --reliability 1.0 --verbose
```

`--self-test` now also verifies that banned fact-conversion phrases are rejected and that the required “NOT A FACT” disclaimer is present.

## Rejection criteria

Any contribution that:

- presents a number derived from the administrative records as a fact, or
- relies on “least-bad sources” (or equivalent) language to imply factual status,

will be rejected.
