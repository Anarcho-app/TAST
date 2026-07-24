# Stream 1 — Generative likelihood (documented arrivals + NI)

## Result

Under a simple H1 path (1790 admin stock grown at ~2.5%/yr NI + residual post-1790 imports):

| Quantity | Value |
|----------|-------|
| N_1790 (census admin) | 697,681 |
| N_1860 observed (census admin) | 3,953,760 |
| N_1860 predicted (H1 path) | ~4.35e6 |
| obs/pred | ~0.91 |
| **L(H1)** (lognormal kernel, σ=0.15) | **≈ 0.82** |

**Previous cell was 0.07** — inverted relative to the hypothesis that predicts exceptional growth. The generative number is **0.82**, not 0.07.

## What this does and does not do

- **Does:** Replace an asserted anti-H1 cell with a transparent computation. Code: `model/stream1_generative.py`.
- **Does not:** Make H1 win at r=1. The other ~10 quant streams still encode low H1; the product still yields H1≈0%. That confirms Opus: magnitude across many cells, not Stream 1 alone.
- **Does not:** Convert census/voyage totals into facts. Inputs remain conditional admin series under `victors_reliability`.

## Sensitivity (honest)

| r_ni | σ_log | L_H1 |
|------|-------|------|
| 1.5% | 0.15 | ~0.00 |
| 2.0% | 0.15 | ~0.28 |
| **2.5%** | **0.15** | **~0.82** |
| 3.0% | 0.15 | ~0.02 |

The cell is sensitive to the NI rate assumption. 2.5%/yr matches the *observed admin* growth order of magnitude; that is circular if used as proof of NI, but it is the right check for “is observed growth *surprising* under H1?” — answer: **no**, not under this error model.

## Epistemic status

GENERATIVE / CONDITIONAL. First Stream 1 cell that is earned rather than hand-set. Still admin-conditioned. Caribbean/Brazilian contrast remains compressed in Stream 2 — next refinement, not a new stream count.
