# Reweighted Layer — Bayesian Streams & Posteriors

This layer contains the evidence streams and the posterior calculations **conditioned on a chosen reliability value**.

- See `../model/evidence_streams.csv` for the full likelihood table.
- See `../model/bayesian_core.py` for the update engine and the `victors_reliability` parameter.

Every numerical posterior printed here must be read with the conditioning statement:

> “If we treat the recorded population totals as approximately accurate (victors_reliability = X), then …; if we do not, the quantitative claim is undefined.”
