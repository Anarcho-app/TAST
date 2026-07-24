# Floor isotope / aDNA terms scaffold (P1 / M1)

**Rule**: Encode only verified per-site counts from `data/verified_isotope_adna.yaml`.  
No invented African-born proportions. Birthplace requires isotopes; ancestry ≠ birthplace.

## Target generative form (per site s)

$$
k_s \mid n_s, H_i \sim \mathrm{BetaBinomial}(n_s, \alpha_i, \beta_i)
\quad\text{or}\quad
k_s \mid n_s, p_s(H_i) \sim \mathrm{Binomial}(n_s, p_s(H_i))
$$

with explicit sampling fraction / coverage $c_s$ (often tiny).  
$H_1$ and $H_2$ supply different predicted trajectories for $p_s$ over time/region; residual subclaims must also make predictions so they can lose.

## Wiring (when counts are verified)

1. Flag streams or terms `is_floor_quantitative=1` → **bypass** `apply_reliability` (active at all $r$).
2. Contribute to `physical_loglik` **and** to mechanism update via hypothesis-conditional likelihood (M1).
3. Administrative totals remain UNDEFINED at $r=0$; collapse rule untouched.
4. Conservative coverage: real $n$ is small; do not inflate.

## Currently verified anchors (see yaml)

| Site | Verified n | Birthplace method | Status |
|------|------------|-------------------|--------|
| Catoctin (Harney 2023) | 27 individuals | ancestry only (≠ birthplace) | presence/continuity OK; no birthplace $k/n$ yet |
| Anson Street (Fleskes 2023) | 36 ind.; 18 genomes | ancestry only | same |
| Saint Martin (Schroeder 2015) | 3 African-born | paper asserts African-born | proof-of-concept only |
| NYABG Goodman Sr/Pb | tables not extracted | isotopes | **blocked until tables pulled** |

## Blocked until

Goodman et al. Sr/Pb tables (and any other published birthplace calls) extracted with page/table refs into the yaml. Then set $k_s, n_s$ and document $\alpha_i, \beta_i$ from the same literature.

## Operational hygiene (every new term)

- raw/ excerpt or page citation  
- credible intervals under likelihood uncertainty  
- r=0 self-test still returns exactly prior on administrative path  
- prior-sweep + leave-one-out after material change  
- adversarial pass logged in VERSION/DECISIONS with exact failure fixed  
