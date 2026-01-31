import json
from scipy.stats import chi2_contingency

def main():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)

    print("Running Statistical Significance Tests (Chi-squared)...\n")
    
    # GSM8K
    gsm = data['gsm8k']
    # Contingency table: [[Baseline Correct, Baseline Wrong], [Combined Correct, Combined Wrong]]
    base_corr = gsm['baseline']['correct']
    base_wrong = gsm['baseline']['total'] - base_corr
    comb_corr = gsm['combined']['correct']
    comb_wrong = gsm['combined']['total'] - comb_corr
    
    table_gsm = [[base_corr, base_wrong], [comb_corr, comb_wrong]]
    res_gsm = chi2_contingency(table_gsm)
    p_gsm = res_gsm.pvalue
    
    print(f"GSM8K (Baseline vs Combined):")
    print(f"Table: {table_gsm}")
    print(f"P-value: {p_gsm:.4f}")
    if p_gsm < 0.05:
        print(">> Significant!")
    else:
        print(">> Not significant (likely due to small n=50).")

    # TruthfulQA
    # We need the counts. We have percentages in metrics.json, let's reconstruct or load.
    # Actually metrics.json doesn't have raw counts for TQA judge, only %. 
    # Let's infer counts from % * 50 (since n=50).
    tqa = data['tqa']
    base_acc = tqa['baseline']['truthfulness_acc']
    comb_acc = tqa['combined']['truthfulness_acc']
    
    base_corr_tqa = int(round((base_acc / 100) * 50))
    base_wrong_tqa = 50 - base_corr_tqa
    comb_corr_tqa = int(round((comb_acc / 100) * 50))
    comb_wrong_tqa = 50 - comb_corr_tqa
    
    table_tqa = [[base_corr_tqa, base_wrong_tqa], [comb_corr_tqa, comb_wrong_tqa]]
    res_tqa = chi2_contingency(table_tqa)
    p_tqa = res_tqa.pvalue

    print(f"\nTruthfulQA (Baseline vs Combined):")
    print(f"Table: {table_tqa}")
    print(f"P-value: {p_tqa:.4f}")
    
    # Save stats
    with open("results/stats.txt", "w") as f:
        f.write(f"GSM8K P-value: {p_gsm:.4f}\n")
        f.write(f"TruthfulQA P-value: {p_tqa:.4f}\n")

if __name__ == "__main__":
    main()
