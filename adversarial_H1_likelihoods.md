# Adversarial H1 Likelihood Table (Opus 4.8 recommendation, 2026-07-24)

**Purpose**: Convert the honest negative ("we could not raise H1 above residual H5") into a stronger claim by running the *strongest good-faith H1-aligned table* through the identical machine and showing where it still fails (or succeeds).

This is required by the symmetry already committed to in Stream 26 (symmetric overreach filter) and the uniform genetics evidentiary bar.

## Current (analyst) vs Adversarial (Hacker/Eltis-aligned reader) for key streams

Only the H1 column is changed for the adversarial table; other hypotheses left as-is for first pass (conservative). Focus streams: 1, 4, 15, 20, 22 as recommended. Other quant streams kept identical.

| stream_id | name | Current H1 | Adversarial H1 | Rationale for adversarial (good-faith mainstream) |
|-----------|------|------------|----------------|---------------------------------------------------|
| 1 | Demographic Growth Rates | 0.07 | **0.85** | H1 *predicts* exceptional NI under U.S. conditions. Observed high growth rates are *exactly* what the hypothesis was built to explain. Inverting this cell is the clearest encoding-of-conclusion. Mainstream (Hacker, McClelland, etc.) treat the growth data as strong support for high NI. |
| 4 | Plantation Ledger Renaming | 0.10 | **0.55** | Renaming/classification fluidity exists, but mainstream views it as second-order relative to the volume of documented arrivals + fertility. Not decisive against H1. |
| 15 | Sex Ratio Skew & Fertility Strain | 0.15 | **0.60** | Sex-ratio problems and strain are real, but H1 already incorporates "exceptional" recovery under U.S. conditions (better nutrition, lower disease load relative to Caribbean, etc.). Not decisive against. |
| 20 | Anthropometric Selection Bias (Steckel) | 0.15 | **0.50** | Selection bias in heights is acknowledged in the literature; it does not overturn the growth accounting that underpins H1. Neutral-to-mild support. |
| 22 | Census Schedule Reclassification Patterns | 0.15 | **0.55** | Reclassification (mulatto/black fluidity, free vs slave) is documented, but mainstream demography treats the net headcount series as still informative for overall growth after standard corrections. |

All other quantitative streams retain their current H1 values for this first adversarial run.

## How to run

```bash
# After placing adversarial values into a copy of evidence_streams.csv
python -m model.bayesian_core --reliability 1.0 --lik-uncertainty 2000 --kappa 8 --seed 42
# Compare the two H5 / H1 intervals side-by-side
```

## Expected diagnostic value

If even the adversarial table still leaves H1 << H5, the negative result is robust to the most charitable mainstream re-reading of the likelihoods.

If the adversarial table *does* raise H1 substantially, then the original table was doing too much work via the inverted cells, and the project must either defend those inversions with primary-linked argument or adopt the more charitable values.

This is the symmetry test the model already claims to apply elsewhere.

Credit: Concrete next-step recommendation from Opus 4.8 review of the Beta-layer pass.
