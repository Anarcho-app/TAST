# Adversarial H1 Likelihood Table — Measured Results

**Purpose**: Convert the honest negative into a stronger claim by running the strongest good-faith H1-aligned table through the identical machine.

Required by Stream 26 (symmetric overreach filter) and the uniform genetics bar.

## Measured results (r = 1.0)

| Table | H1 point | H1 CI (κ=8, n=2000, seed=42) | H5 |
|-------|----------|------------------------------|-----|
| Current | 0.0000 | [0.0000, 0.0000] | 0.577 |
| 5-cell adversarial | 0.0001 | [0.0000, 0.0004] | 0.577 |
| Full charitable (all 11) | 0.0343 | [0.0050, 0.1179] | 0.558 |
| Prior | 0.0727 | — | 0.427 |

Under the most charitable mainstream reading of all eleven quantitative cells, H1 remains below its prior at the point estimate and at the median. Likelihood uncertainty admits values above the prior in the upper tail (95th ≈ 11.8 %). 

Honest statement: *H1 remains below its prior at the median under full charity; the upper tail of the Beta layer can exceed the prior.*

## How to run (reproducible)

```bash
python -m model.bayesian_core --reliability 1.0
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_adversarial.csv
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_full_charitable.csv --lik-uncertainty 2000 --kappa 8 --seed 42
```

The `--streams` flag now passes the path explicitly to `load_streams()` (no default-argument trap).

## Key streams changed in 5-cell version

| id | name | Current H1 | Adversarial H1 |
|----|------|------------|----------------|
| 1 | Demographic Growth Rates | 0.07 | 0.85 |
| 4 | Plantation Ledger Renaming | 0.10 | 0.55 |
| 15 | Sex Ratio Skew & Fertility Strain | 0.15 | 0.60 |
| 20 | Anthropometric Selection Bias | 0.15 | 0.50 |
| 22 | Census Schedule Reclassification | 0.15 | 0.55 |

Full charitable raises all eleven quantitative H1 cells (see `model/evidence_streams_full_charitable.csv`).

## Why residual H5 still dominates

Mean L (current table): H5 = 0.764 (8/11 ≥ 0.75). A residual that is never surprised wins the product by construction. See DECISIONS.md H5 column audit. Next structural step: replace the single H5 column with H5a–H5d.

Credit: design, measurement, CI nuance, and the default-argument bug report — Claude Opus 4.8.
