# TAST status handoff (2026-07-24)

## Architecture
- Legacy: bayesian_core product of streams (triaged 13→6 quant; Streams 1–2 generative)
- **Current estimand path:** `model/joint_alpha_model.py` — joint posterior on absorption fraction
- Shared latents; O1 counts, O2 post-trade gap, O3 NA ceiling
- Double-counting of derived streams fixed by construction in joint model

## Illustrative joint result (seed=42)
- α median ~0.8–1%, 90% CI upper ~4%, p99 ~5–6%
- **O3 does almost all work on α**; O1+O2 nearly silent (H2b ≈ H1 on growth)
- Must publish O3-on/off and prior sensitivity

## Open issues (do not rubber-stamp α headline)
1. Proxy chain: modern NA% ↛ α_admin (lookerism ≠ genome)
2. Split α_admin vs α_I — see model/RESOLUTION_alpha_lookerism.md
3. O3 hinge width 0.02 not from Bryc SE
4. Beta(1,20) prior load-bearing
5. implied_na = alpha assumes Indigenous pool composition

## Not on critical path
Streams 15, 22 as product rows (would worsen correlation). Optional as joint observables later.
