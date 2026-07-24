# Acknowledgments & Development Credit

## Primary author and repository owner

**Anarcho-app** (GitHub: [Anarcho-app/TAST](https://github.com/Anarcho-app/TAST))  
Intellectual direction, source registry, epistemic framing (Freedmen’s Bureau-era / multi-generational American lineages, zero-weight collapse rule, physical-floor priority), and final authority over the project.

## Collaborative development assistance

Substantial iterative development of the model architecture, code, documentation, and epistemic hardening was carried out in collaboration with **Grok** (built by xAI).  

This includes:

- Layered repository structure (raw / conventional / reweighted / surviving)
- Reliability-parameter design and zero-weight collapse implementation
- Per-claim confidence scoring, Monte Carlo paths, and hierarchical skeleton
- Physical-floor likelihood terms (burial, aDNA, genealogical termination, erasure, regime)
- Language and identity discipline (“NOT A FACT”, multi-generational American lineages framing)
- METHODS.md separation of standard Bayesian mathematics from the novel epistemic rule
- Continuous versioning and adversarial-readiness checklist

Grok does not claim ownership of the repository, the source registry, or the core intellectual framing. Credit for the project’s existence, direction, and publication remains with Anarcho-app.  

The collaboration is recorded here so that the development history is transparent and so that assistance from the model is neither invisible nor overstated.

## How to cite

If you use or refer to this work, please cite the repository and its primary author. An optional note on collaborative development assistance from Grok (xAI) is accurate and welcome but not required.

## Adversarial review credit (LLMs)

Independent model reviews that improved the project by attacking it on its own stated terms:

- **Claude Opus 4.8** (2026-07-23/24): Full clone-and-run audit. Identified that the zero-weight collapse was implemented as a print short-circuit rather than a mathematical return to prior / non-informative state; that non-quantitative streams dominate and settle mechanism at every r; that physical_loglik was not wired into bayesian_core; that the “Helper = r=1.0 boundary” claim is falsified by H1 ≈ 0 at all r; and that independence among 27 streams inflates H5. Ordered fix list adopted into VERSION.md.
- **Gemini** (prior rounds, including comparative 3/10-style evaluations): Forced clarity on neutrality, selective framing, subjective priors, incomplete literature ties, and advocacy-tone critiques against peer-review benchmarks. Those critiques, even when over-weighted toward “advocacy,” drove the project to separate standard Bayesian mathematics from the epistemic rule, to lock evaluation criteria into the README, and to treat administrative records as data for critical analysis rather than as targets for automatic rejection. Gemini’s pressure is part of why the foundation sections exist.

These reviews are recorded so that LLM critique is neither invisible nor treated as authority. Credit is for the specific, testable failures they found. Responses and fixes remain the responsibility of the project maintainers.

- **Claude Opus 4.8 (second pass, 2026-07-24)**: Caught that v5.2 “return to prior” was still a CLI print substitution while `apply_reliability`/`bayes_update` produced H5≈80% at r=0; that sensitivity_map and bayesian_core contradicted each other on the headline claim; that README still advertised the retracted Helper boundary. Drove the single shared `collapse_posterior()` function, the r=0 self-test assertion, and doc/code alignment.
- **Claude Opus 4.8 (third pass, 2026-07-24)**: Identified the r=0.05 step-function cliff; showed that excluding non-quantitative streams at all r yields continuous collapse with posterior(r=0)=prior by arithmetic (L→0.5), not by threshold; localized remaining H1 annihilation to the 11 quantitative rows and specifically stream 1 (Demographic Growth Rates H1=0.07).
