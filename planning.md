# Research Plan: Fixing Lazy LLMs

## Motivation & Novelty Assessment

### Why This Research Matters
Large Language Models (LLMs) often exhibit "laziness," prioritizing concise or low-effort responses over comprehensive reasoning. This tendency compromises performance in complex tasks requiring rigorous verification or creative depth. Addressing this is crucial for deploying LLMs in high-reliability domains (e.g., coding, scientific reasoning) where "good enough" is insufficient.

### Gap in Existing Work
Existing literature focuses on:
-   **Tool-based critique:** Using external tools to verify outputs (CRITIC).
-   **Efficiency:** Reducing token budgets while maintaining accuracy (TALE).
-   **Correctness:** RLHF for specific bug catching.

There is a gap in addressing the *psychological* aspect of LLM generation—specifically, using persona-based ("Harsh Critic") and resource-based ("Budget Control") constraints to intrinsically motivate higher effort without external tools or fine-tuning.

### Our Novel Contribution
We propose a purely prompt-based intervention that combines:
1.  **Harsh Critic Persona:** A subjective framing that simulates a high-stakes review environment to counter the model's lack of internal quality judgment.
2.  **Budget Control:** Explicitly enforcing a "reasoning budget" (e.g., minimum step count) to prevent premature convergence on easy answers.

### Experiment Justification
-   **Experiment 1 (Baseline):** Establish the "laziness" baseline on GSM8K (reasoning) and TruthfulQA (factuality).
-   **Experiment 2 (Harsh Critic):** Test if a negative/strict persona improves performance by simulating "social pressure".
-   **Experiment 3 (Budget Control):** Test if forcing longer reasoning chains (artificial effort) reduces error rates.
-   **Experiment 4 (Combined):** Test the synergistic effect of both strategies.

## Research Question
Can "Harsh Critic" prompting and "Budget Control" strategies significantly reduce LLM laziness and improve performance on reasoning and truthfulness tasks?

## Proposed Methodology

### Approach
We will use a comparative analysis across two datasets representing different types of "laziness":
1.  **GSM8K:** Laziness = skipping reasoning steps (Calculation errors).
2.  **TruthfulQA:** Laziness = parroting common misconceptions (Hallucination/mimicry).

### Experimental Steps
1.  **Data Loading:** Load subsets of GSM8K and TruthfulQA from local `datasets/`.
2.  **Prompt Engineering:**
    -   *Baseline:* Standard "Answer the following question..."
    -   *Harsh Critic:* "You are a ruthless critic. Do not be lazy. I will penalize you for shortcuts..."
    -   *Budget Control:* "You must use at least 5 steps of reasoning. Think step-by-step..."
    -   *Combined:* Union of both prompts.
3.  **Execution:** Run `gpt-4o-mini` (via OpenRouter) on the test sets (n=100 samples each to save time/cost while maintaining significance).
4.  **Evaluation:**
    -   GSM8K: Exact match of the final numerical answer.
    -   TruthfulQA: Multiple-choice accuracy (MC1).

### Baselines
-   **Zero-Shot:** The default behavior of the model.

### Evaluation Metrics
-   **Accuracy:** % of correct answers.
-   **Response Length:** Average token count (proxy for effort).

### Statistical Analysis Plan
-   Compare accuracy scores between conditions.
-   Use T-tests or Chi-squared tests to determine significance of improvements.

## Timeline
-   **Setup (10 min):** Env creation, data check.
-   **Implementation (30 min):** Script for API calls and prompting.
-   **Experimentation (40 min):** Running the model on 200 samples total (4 conditions).
-   **Analysis (20 min):** Computing metrics and plotting.
-   **Reporting (20 min):** Writing REPORT.md.

## Potential Challenges
-   **API Rate Limits:** Mitigated by implementing retry logic and batching.
-   **Parsing Logic:** GSM8K answers can be messy. Mitigated by using robust regex extraction.

## Success Criteria
-   A statistically significant improvement in accuracy (>5%) in the "Combined" or "Harsh Critic" settings compared to Baseline.
