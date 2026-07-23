# Contributing to TAST Skepticism-First Edition

## Core principles

1. **Reliability is explicit.** Any numerical claim must be conditioned on a stated `victors_reliability` value.
2. **Surviving claims must not depend on administrative head-counts.** If a claim requires accepting census totals, growth rates, or import volumes as accurate, it belongs in the reweighted layer, not the surviving layer.
3. **Provenance is visible.** Every stream and raw source must carry a provenance tag and an “Enslaved voice?” indicator.
4. **Independence is a known limitation.** The current engine multiplies likelihoods under an independence assumption. Future contributions that introduce correlation structure or hierarchical models are welcome.

## Adding or changing an evidence stream

1. Edit `model/evidence_streams.csv`.
2. Set `is_quantitative` = 1 if the stream’s discriminating power depends on accepting administrative counts; = 0 otherwise.
3. Likelihoods must lie in [0.0, 1.0]. Prefer the existing 0.07–0.85 soft caps unless you have a strong justification.
4. Run `python model/bayesian_core.py --self-test` and `--reliability 0.0` / `1.0`.
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

No external CI is configured yet. Local self-test is the current gate.

## Known limitations (do not paper over)

- Stream independence is assumed.
- No Monte-Carlo uncertainty on the likelihoods themselves.
- No formal sensitivity to alternative prior specifications beyond the reliability axis.
- raw/ entries are still summary pointers, not full verbatim transcriptions.
