# Joint α model (Path A)

## Estimand

**α** = fraction of the 1860 enslaved population attributable to absorption/reclassification.

Not \(P(H_1,\ldots,H_5)\). The five-way product is retired for this claim.

## Latents (shared)

| Parameter | Prior |
|-----------|--------|
| \(r_{US}\) | N(2.2%, 0.4%) |
| \(r_{Carib}\) | N(−0.8%, 1.0%) |
| **α** | Beta(1, 20) (skeptical of large absorption) |
| log σ | N(0.15, 0.05) |
| n_pool | LogNormal around 800k |

## Observables (one joint likelihood)

1. US 1790→1860 terminal count under NI + imports + α  
2. Post-trade growth gap US vs British Caribbean  
3. NA ancestry soft ceiling (Bryc-class)

## Run

```bash
python -m model.joint_alpha_model
```

## Illustrative posterior (seed=42, 2000 draws)

| | α |
|--|---|
| median | ~0.8% |
| 90% CI | ~[0.0%, 4.2%] |
| p99 | ~6% |

Bound is driven by growth + genomic observables under stated priors.  
Refine by replacing priors with Steckel CBR/CDR, Indigenous pool series, sex ratio, reclassification rates — as **parameter priors / additional observables**, not new product rows.

## Relationship to bayesian_core

`bayesian_core.py` remains for reliability-collapse demos and triage.  
**Publishable absorption claim lives here.**
