# Resources Catalog

## Summary
This document catalogs resources gathered for the "Fixing Lazy LLMs" project.

## Papers
Total papers downloaded: 5 (processed)

| Title | Key Relevance | File |
|-------|---------------|------|
| LLM Critics Help Catch LLM Bugs | Harsh Critic Baseline | papers/llm_critics_bugs.pdf |
| CRITIC: Self-Correct with Tools | Tool-based Criticism | papers/critic_self_correct.pdf |
| Token-Budget-Aware Reasoning | Budget Control | papers/token_budget_reasoning.pdf |
| Budget-Aware Anytime Reasoning | Budget/Anytime | papers/budget_anytime_reasoning.pdf |
| MCQG-SRefine | Self-Critique Loop | papers/self_critique_adapt.pdf |

See `papers/README.md` for abstracts.

## Datasets
Total datasets: 2

| Name | Task | Size | Location |
|------|------|------|----------|
| GSM8K | Math Reasoning | ~7.5k | datasets/gsm8k |
| TruthfulQA | Truthfulness | ~800 | datasets/truthful_qa |

See `datasets/README.md` for details.

## Code Repositories
Total repositories: 2

| Name | Purpose | Location |
|------|---------|----------|
| ProphetNet (CRITIC) | Self-Correction Impl | code/ProphetNet/CRITIC |
| TALE | Token Budget Impl | code/TALE |

See `code/README.md` for details.

## Resource Gathering Notes
- **Search Strategy**: Used keywords "LLM laziness", "Harsh Critic", "Response Budget" on arXiv and Google.
- **Challenges**: "Lazy Learners" original paper was tricky to pinpoint via API, but "Lack Understanding" and others filled the gap.
- **Selection**: Prioritized papers with "Critic" and "Budget" in titles as they map directly to the hypothesis.

## Recommendations
1.  **Primary Dataset**: GSM8K is best for starting (fast, objective).
2.  **Baseline**: Run CRITIC's self-correction loop as a baseline for "Critic".
3.  **Experiment**: Modify the "Critic" prompt to be "Harsh" (e.g., "You are a ruthless reviewer...") and measure impact on GSM8K accuracy.
