# M1 Design — Floor Likelihood with Hypothesis Dimension

**Source**: Multi-agent audit (Kimi K3 lead, Kat Coder Pro 2.5, Minimax M3), 2026-07-24.  
**Status**: Design only. No α/β or k/n encoded until verified from papers (`data/verified_isotope_adna.yaml`).

## Problem

`physical_loglik()` returns a **scalar** with no H1–H5 dimension. At r=0 the model returns the prior and learns nothing from the floor. "Only the floor remains" is true as data availability, not as inference.

Four of six constants feeding the scalar are stipulated (n_adna=80, termin_in_us_frac=0.85, erasure_log_ratio=4.5, n_regime_jurisdictions=12) — violating the project's own §7 discipline.

## Target

$$P(H_i \mid \text{data}, r{=}0) \propto P(H_i) \times P(\text{floor} \mid H_i)$$

with

$$P(\text{floor}\mid H_i)=\prod_k P(\text{obs}_k \mid H_i)$$

Flagship term — isotope African-born proportion as Beta-Binomial:

$$P(k \text{ African-born of } n \mid H_i) = \binom{n}{k}\frac{B(k+\alpha_i,\, n-k+\beta_i)}{B(\alpha_i,\beta_i)}$$

- H1: trajectory with higher African-born early, declining over generations under exceptional NI  
- H2: different (classification/absorption does not require the same birthplace trajectory)  
- α_i, β_i documented from isotope literature after paper pull  
- Sampling model: port burial grounds skew first-generation independent of mechanism

## Implementation sketch

1. New flag `is_floor_quantitative` on streams (or a parallel floor-stream table).  
2. These streams **bypass** `apply_reliability` — active at all r, including r=0.  
3. Administrative totals remain undefined at r→0; collapse rule untouched.  
4. `bayes_update` / `collapse_posterior` multiply floor likelihoods into the posterior at every r.  
5. Stipulated constants replaced by counted inventories as they become available (P2).

## What this does *not* do

- Does not invent national totals  
- Does not encode proportions from recall  
- Does not weaken the zero-weight rule on administrative records  

## Dependency

P1: extract Goodman et al. Sr/Pb tables and any published birthplace calls with page/table refs into `data/verified_isotope_adna.yaml` before setting α/β or k/n.

## Related audit items

- M2: Manski partial-identification bounds (upgrade UNDEFINED from declaration to identified set)  
- M5: `region_probabilities()` in hierarchical_skeleton.py is a hardwired score, not a derived region integral — fix or label illustrative-only  
- Fabrication catch: "29/36 Anson Street Lowcountry-born ⇒ H2" is **not** in Fleskes et al. 2023; genomic ancestry ≠ birthplace. Validates verify-before-encode.
