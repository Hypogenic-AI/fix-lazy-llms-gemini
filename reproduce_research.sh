#!/bin/bash
set -e

echo "Starting Full Reproduction Pipeline..."

# 1. Setup
echo "[1/7] Setting up environment..."
if [ ! -d ".venv" ]; then
    uv venv
fi
source .venv/bin/activate
uv add openai pandas datasets tqdm scikit-learn numpy matplotlib seaborn scipy

# 2. Experiments
echo "[2/7] Running Experiments (this may take 10-20 mins)..."
python src/experiment_runner.py
python src/run_politeness_check.py
python src/run_skeptic.py
python src/run_reflexion.py

# 3. Analysis
echo "[3/7] Analyzing Results..."
python src/analyze_results.py
python src/analyze_politeness.py
python src/analyze_skeptic.py
python src/analyze_reflexion.py
python src/evaluate_tqa.py

# 4. Correlation & Stats
echo "[4/7] Running Statistical Tests..."
python src/analyze_correlation.py
python src/stat_test.py
python src/extract_examples.py

# 5. Efficiency
echo "[5/7] Analyzing Efficiency..."
python src/analyze_efficiency.py

# 6. Plots
echo "[6/7] Generating Plots..."
python src/plot_tqa.py
python src/plot_persona.py
python src/plot_final.py
python src/plot_executive_summary.py

echo "[7/7] Reproduction Complete! Check 'results/' for all outputs."
