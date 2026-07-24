# Adversarial H1 Likelihood Table (Opus 4.8 recommendation + measured results)

**Purpose**: Convert the honest negative ("we could not raise H1 above residual H5") into a stronger claim by running the *strongest good-faith H1-aligned table* through the identical machine and showing where it still fails.

This is required by the symmetry already committed to in Stream 26 (symmetric overreach filter) and the uniform genetics evidentiary bar.

## Measured results (r = 1.0, point estimates)

| Table                        | H1 posterior   | H5 posterior | vs Prior (H1 = 7.27 %) |
|-----------------------------|----------------|--------------|------------------------|
| Current (analyst)           | 2.5 × 10⁻⁸     | 0.577        | far below              |
| 5-cell adversarial          | 8.1 × 10⁻⁵     | 0.577        | far below              |
| Full charitable (all 11)    | ≈ 1–3.5 %      | ≈ 0.56       | **still below prior**  |

Even under a maximally charitable mainstream reading of every quantitative cell, H1 lands below its own prior. The negative result is robust.

## Current vs 5-cell adversarial (key streams)

| stream_id | name | Current H1 | Adversarial H1 | Rationale |
|-----------|------|------------|----------------|-----------|
| 1 | Demographic Growth Rates | 0.07 | **0.85** | H1 *predicts* exceptional NI. Observed growth is exactly what the hypothesis was built to explain. |
| 4 | Plantation Ledger Renaming | 0.10 | **0.55** | Second-order relative to documented arrivals + fertility. |
| 15 | Sex Ratio Skew & Fertility Strain | 0.15 | **0.60** | Real, but H1 already incorporates exceptional recovery under U.S. conditions. |
| 20 | Anthropometric Selection Bias (Steckel) | 0.15 | **0.50** | Acknowledged; does not overturn growth accounting. |
| 22 | Census Schedule Reclassification Patterns | 0.15 | **0.55** | Documented; mainstream treats net series as still informative after correction. |

## How to run (reproducible)

```bash
# Current table
python -m model.bayesian_core --reliability 1.0 --lik-uncertainty 2000 --kappa 8 --seed 42

# 5-cell adversarial
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_adversarial.csv --lik-uncertainty 2000 --kappa 8 --seed 42

# Full charitable (all 11 cells)
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_full_charitable.csv --lik-uncertainty 2000 --kappa 8 --seed 42
```

## Why H1 still loses even under charity

Mean likelihood across the 11 quantitative streams (current table):

```
H1:  0.220    0/11 cells ≥ 0.75
H5:  0.764    8/11 cells ≥ 0.75
```

H5 is never surprised. Discrete products have no Occam penalty for a catch-all residual. See DECISIONS.md (H5 column audit) and the next structural step: decompose the H5 column into H5a–H5d.

Credit: diagnosis, design, and measured results from Claude Opus 4.8.
