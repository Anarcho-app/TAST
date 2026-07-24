# Observable Facts — Confidence vs Probability

## What `confidence` means

In `observable_facts.yaml`, **`confidence` ∈ [0, 1]** is a **source / observability score**:

- How solid is the primary or physical basis for treating the statement as an observable?
- Derived from provenance, physical character, enslaved-voice presence, and related rules.
- **It is not** \(P(\text{claim is true} \mid \text{evidence})\).

| Term | Meaning | In repo? |
|------|---------|----------|
| `confidence` | Source-quality / observability score | Yes |
| `p_claim` | Model-based P(statement true \| floor evidence) | Optional / provisional |
| Uncertainty on `p_claim` | Monte Carlo spread over that probability | Via MC helpers |

## Rule

Administrative national totals are never listed as facts.  
Physical presence, structural silence, legal regime, and genealogical termination are prioritized.

High `confidence` (≥ 0.85) marks strong observables for the physical floor.  
All entries remain open to revision with new primary evidence.
