# Prior sensitivity (table-as-verdict)

```bash
python -m model.bayesian_core --prior-sensitivity
```

If posterior H1 stays ~0 until prior H1 exceeds ~0.9999, the engine is not balancing evidence against a prior — the likelihood product has already decided. Rebuild cells (Stream 1 first); do not add streams or tune priors.
