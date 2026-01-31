# Literature Review: Fixing Lazy LLMs

## Research Area Overview
This research investigates the phenomenon of "laziness" in Large Language Models (LLMs), where models opt for less effortful, shortcut-based, or overly concise responses instead of robust, high-quality reasoning. The proposed solutions involve prompting LLMs to act as "Harsh Critics" to evaluate and refine their own outputs, and controlling "Response Budgets" to force deeper or more efficient reasoning.

## Key Papers

### 1. LLM Critics Help Catch LLM Bugs
- **Authors**: Nat McAleese et al. (OpenAI/Google DeepMind alumni)
- **Year**: 2024
- **Key Contribution**: Trains "Critic" models using RLHF to identify errors in code.
- **Results**: Critics are more effective than humans in some settings (catching more bugs). Critics catch 63% of errors where humans fail.
- **Relevance**: Supports the "Harsh Critic" hypothesis. If a model can be trained/prompted to be a critic, it can catch "lazy" errors (like bugs or shortcuts).

### 2. CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing
- **Authors**: Gou et al. (Microsoft)
- **Year**: 2023
- **Methodology**: "CRITIC" framework where LLMs generate output, then interact with tools (search, code interpreter) to critique and verify the output, then correct it.
- **Key Findings**: Self-correction *with tools* significantly improves performance on QA and code tasks. Without tools, self-correction is often unreliable.
- **Relevance**: Provides a concrete framework for the "Critic" loop. It suggests that "laziness" (hallucinations/errors) can be fixed by an iterative critique-verify-correct cycle.

### 3. Token-Budget-Aware LLM Reasoning (TALE)
- **Authors**: Han et al.
- **Year**: 2024
- **Methodology**: Dynamic adjustment of reasoning tokens (budget) based on problem complexity.
- **Key Findings**: Models can maintain high accuracy even with reduced token budgets if managed correctly.
- **Relevance**: Addresses the "Response Budget" aspect. While TALE focuses on *reducing* cost, the mechanism of *controlling* the budget is key. For "lazy" LLMs, we might need to *enforce* a higher budget or specific budget allocation to prevent premature stopping.

### 4. Budget-Aware Anytime Reasoning
- **Authors**: Zhang et al.
- **Year**: 2026 (Preprint/New)
- **Methodology**: "Anytime reasoning" where models produce best-effort answers within a fixed budget, improving as budget increases.
- **Relevance**: framing reasoning as a resource-constrained optimization. "Laziness" can be seen as stopping at a low-budget point on the curve.

## Common Methodologies
1.  **Iterative Refinement**: Generate -> Critique -> Refine (CRITIC, Self-Refine).
2.  **RLHF for Critics**: Training specific reward models or critics to detect errors.
3.  **Prompt Engineering**: "Chain of Thought" (CoT) to force reasoning steps, effectively increasing the "effort" (budget) used.

## Gaps and Opportunities
-   **Laziness Definition**: "Laziness" is often ill-defined (is it shortness? hallucination? using shortcuts?). This research can clarify it.
-   **Subjective Judgment**: Most critics focus on objective correctness (code, math). The hypothesis mentions "subjective judgment of good or bad". There is a gap in using critics for *qualitative* laziness (e.g., writing a boring story vs. a creative one).
-   **Constraint Satisfaction**: How does a "Harsh Critic" interact with a "Response Budget"? A harsh critic might demand *more* text (fixing laziness), but a budget might constrain it.

## Recommendations for Experiment
-   **Datasets**:
    -   **GSM8K**: For objective reasoning (easy to critique correctness).
    -   **TruthfulQA**: For checking "laziness" in checking facts (hallucinations).
    -   **HumanEval** (or similar): For code generation (lazy = buggy/incomplete code).
-   **Baselines**:
    -   Standard Zero-shot prompting.
    -   Standard Chain-of-Thought (CoT).
    -   Self-Refine (iterative prompting without tools).
-   **Proposed Method**:
    -   Implement a "Harsh Critic" prompt that explicitly penalizes "lazy" traits (brevity, generic phrases).
    -   Combine with a "Budget Controller" that forces the model to spend a certain amount of "compute" (tokens/steps) before answering.
