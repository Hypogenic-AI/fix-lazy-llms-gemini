import json
import re
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pointbiserialr, ttest_ind

def extract_answer_gsm8k(text):
    if not text or text == "ERROR": return None
    boxed = re.search(r'\\boxed\{([^}]+)\}', text)
    if boxed: text_to_parse = boxed.group(1)
    else: text_to_parse = text.replace("####", "")
    numbers = re.findall(r'-?\d{1,3}(?:,\d{3})*(?:\.\d+)?', text_to_parse)
    if not numbers: return None
    last_num = numbers[-1].replace(',', '')
    try: return float(last_num)
    except: return None

def extract_ground_truth_gsm8k(answer_text):
    if "####" in answer_text:
        return float(answer_text.split("####")[1].strip().replace(',', ''))
    return None

def main():
    print("Running Correlation Analysis (Length vs Accuracy)...")
    
    # Gather all GSM8K data
    all_lengths = []
    all_correct = []
    
    # 1. Main file (baseline, harsh, budget, combined)
    with open("results/raw_results_gsm8k.jsonl", "r") as f:
        for line in f:
            item = json.loads(line)
            gt = extract_ground_truth_gsm8k(item['original_data']['answer'])
            if gt is None: continue
            
            for cond, resp in item['responses'].items():
                if resp == "ERROR": continue
                pred = extract_answer_gsm8k(resp)
                is_correct = 1 if (pred is not None and abs(pred - gt) < 1e-6) else 0
                length = len(resp.split())
                
                all_lengths.append(length)
                all_correct.append(is_correct)

    # 2. Other files (high_standards, skeptical, etc.)
    for filename in glob.glob("results/raw_results_gsm8k_*.jsonl"):
        with open(filename, "r") as f:
            for line in f:
                item = json.loads(line)
                gt = extract_ground_truth_gsm8k(item['original_data']['answer'])
                if gt is None: continue
                
                resp = item['response'] # Structure is different in these files
                if resp == "ERROR": continue
                pred = extract_answer_gsm8k(resp)
                is_correct = 1 if (pred is not None and abs(pred - gt) < 1e-6) else 0
                length = len(resp.split())
                
                all_lengths.append(length)
                all_correct.append(is_correct)

    # Convert to arrays
    lengths = np.array(all_lengths)
    correct = np.array(all_correct)
    
    print(f"Total Data Points: {len(lengths)}")
    
    # Statistical Test
    corr, p_val = pointbiserialr(correct, lengths)
    print(f"Point-Biserial Correlation (Length vs Correctness): r={corr:.3f}, p={p_val:.4f}")
    
    # T-test
    len_correct = lengths[correct == 1]
    len_wrong = lengths[correct == 0]
    t_stat, t_p = ttest_ind(len_correct, len_wrong)
    
    print(f"Avg Length (Correct): {np.mean(len_correct):.1f}")
    print(f"Avg Length (Wrong): {np.mean(len_wrong):.1f}")
    print(f"T-test Difference: p={t_p:.4f}")

    # Plot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=correct, y=lengths, palette=["#ff9999", "#99ff99"])
    plt.xticks([0, 1], ['Incorrect', 'Correct'])
    plt.ylabel('Response Length (Words)')
    plt.title('Does Effort (Length) Predict Accuracy?')
    
    # Add stats to plot
    plt.text(0.5, max(lengths)*0.9, f"Correlation: r={corr:.2f} (p={p_val:.3f})", 
             ha='center', bbox=dict(facecolor='white', alpha=0.5))
    
    plt.savefig('results/correlation_length_accuracy.png')
    print("Saved results/correlation_length_accuracy.png")

    # Append stats to stats.txt
    with open("results/stats.txt", "a") as f:
        f.write(f"\nCorrelation (Length vs Accuracy): r={corr:.3f}, p={p_val:.4f}\n")
        f.write(f"Avg Length Correct: {np.mean(len_correct):.1f}\n")
        f.write(f"Avg Length Wrong: {np.mean(len_wrong):.1f}\n")

if __name__ == "__main__":
    main()
