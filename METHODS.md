# Methods & Mathematical Pedigree

This document exists to make one fact undeniable:

**The inference machinery of TAST is standard Bayesian statistics.**  
The novel contribution is the epistemic rule (the continuous `victors_reliability` parameter and the zero-weight collapse applied to administrative records produced by trading and slaveholding societies).

## Formal objects and classic references

| Object in TAST | Standard name | Classic / textbook reference |
|----------------|---------------|------------------------------|
| Product of likelihoods in log-space | Bayes’ theorem + numerical stability | Gelman et al., *Bayesian Data Analysis*; any modern Bayesian textbook |
| Monte Carlo over a reliability hyperparameter | Monte Carlo / ancestral sampling | Robert & Casella, *Monte Carlo Statistical Methods* |
| Hierarchical / weakly informative hyperpriors on rates and reliability | Hierarchical Bayes, weakly informative priors | Gelman et al., *Bayesian Data Analysis*; Gelman (2006) on weakly informative priors |
| Poisson likelihoods on burial site counts, aDNA individuals, jurisdictions | Poisson process / counting model | Classic point-process and count-data literature |
| Beta distributions for proportions and concentrations | Beta-Binomial / rate modeling | Standard conjugate analysis |
| Reliability or bias parameter that can be driven to zero and marginalized | Measurement-error / selection-bias / missing-data models | Bayesian measurement-error literature; selection models |
| Log-sum-exp normalization | Numerical linear algebra / stable softmax | Standard numerical analysis |

None of the rows above is experimental.

## What *is* the novel (and deliberately experimental) contribution

1. Treating a single continuous reliability parameter as able to render an entire class of administrative head-counts, growth rates, and import totals **UNDEFINED**.
2. Elevating the physical and structural evidence (burial grounds, aDNA remains interred on American soil, genealogical termination in U.S. records, structural silence produced by anti-literacy laws, regime intensity) as the only quantitative floor that survives that collapse.
3. Enforcing language that refuses to convert “least-bad / best-available / historical consensus” into “fact.”
4. Framing the focal population as multi-generational American lineages of African and mixed ancestry (Freedmen’s Bureau-era and earlier U.S. lineages) rather than treating continental-African origin as the unmarked residual identity.

These four decisions are the point of the project. They are not claims about new mathematics.

## Predictive checks and adversarial re-analysis

- Prior and posterior predictive checks are the correct way to make residual prior influence visible. Their expansion is active work.
- The repository is designed so that any LLM or human with basic tools can re-run the Monte Carlo, re-derive claim confidence scores, inspect every stream, and attack every piece. See `CONTRIBUTING.md` and `model/inference_extensions.py --adversarial`.

## What this project does *not* claim

- It does not offer a replacement national population total for 1790 or 1860.
- It does not claim the administrative series are fabricated; it claims they are conditional on a decision to trust them.
- It does not claim the physical floor yields a precise national head-count; it claims the floor yields lower bounds and structural patterns that survive maximal skepticism of the administrative series.

The known knowns are not experimental.  
The decision to treat them as the floor is the contribution.
