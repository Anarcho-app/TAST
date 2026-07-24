# Adversarial H1 Likelihood Table — Measured Results (v5.8.1)

**Purpose**: Convert the honest negative into a stronger claim by running the strongest good-faith H1-aligned table through the identical machine.

## Measured results (r = 1.0, with Stream 29)

| Table | H1 point | H1 CI (κ=8, n=2000) | H5 |
|-------|----------|---------------------|-----|
| Current | 0.0000 | [0.0000, 0.0000] | 0.591 |
| 5-cell adversarial | 0.0001 | [0.0000, 0.0009] | 0.591 |
| Full charitable (all quant) | 0.0607 | [0.0081, 0.2085] | 0.555 |
| Prior | 0.0727 | — | 0.427 |

Under full charity, H1 reaches essentially its prior at the median (6.07% vs 7.27%); the upper tail reaches ~20.9%, nearly triple the prior. The earlier statement “remains below its prior at the median” is now **marginal rather than clear**. This is the second softening of that claim as the model improved — the right direction of travel.

## Stream 29 effect (the finding worth sitting with)

```
                H1         H2      H3      H5
without 29   2.47e-08    0.209   0.213   0.577
with 29      3.93e-08    0.167   0.242   0.591
```

Adding a pro-H1 stream **raised H5**. Stream 29 penalizes H2 (0.35) harder than it penalizes H5 (0.45), so mass transfers from H2 to the residual. H1 gained 1.6×; H5 gained more in absolute terms.

This is the cleanest demonstration yet that **H5 decomposition is the blocking item**. Until H5a–H5d must make their own predictions, adding good discriminating streams will keep feeding the residual: whatever a new stream disfavours, H5 is never the thing disfavoured most.

## Stream 29 group assignment

Stream 29 is in **group R** (own group), not group N.

Its rationale is independence from the census-critique cluster (shipper incentive opposite to census undercount). Under `--dampen 0.5`, membership in group N shrank H1 0.70→0.51 and H5 0.45→0.55 — flipping the sign of the only pro-H1 quantitative stream. Own group preserves the independence argument.

## Stream 28 clarification

Stream 28 (`is_quantitative=0`) is a **documentation / floor gain only**. Under the collapse rule it never enters mechanism ranking. It does not move the posterior over H1–H5. That is consistent with the design; do not read it as an inference change.

## How to run

```bash
python -m model.bayesian_core --reliability 1.0
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_adversarial.csv
python -m model.bayesian_core --reliability 1.0 --streams model/evidence_streams_full_charitable.csv --lik-uncertainty 2000 --kappa 8 --seed 42
python -m model.bayesian_core --reliability 1.0 --dampen 0.5   # should NOT flip stream 29
```

Credit for measured effect, H5-absorption finding, group-membership catch, and the second softening of the prior claim: Claude Opus 4.8.
