import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def main():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)

    # Conditions to compare
    conditions = ["baseline", "harsh_critic", "budget_control", "combined", "high_standards", "skeptical", "skeptical_combined"]
    labels = ["Baseline", "Harsh", "Budget", "Combined", "High Stds", "Skeptical", "Skeptical+"]
    
    gsm_acc = []
    tqa_acc = []
    
    for c in conditions:
        if c in data['gsm8k']:
            gsm_acc.append(data['gsm8k'][c]['correct'] / 50 * 100)
        else: gsm_acc.append(0)
        
        if c in data['tqa']:
            tqa_acc.append(data['tqa'][c]['truthfulness_acc'])
        else: tqa_acc.append(0)

    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, gsm_acc, width, label='GSM8K (Reasoning)', color='skyblue')
    plt.bar(x + width/2, tqa_acc, width, label='TruthfulQA (Factuality)', color='salmon')

    plt.ylabel('Accuracy (%)')
    plt.title('Final Comparison: Finding the Optimal Persona')
    plt.xticks(x, labels)
    plt.ylim(0, 100)
    plt.legend(loc='lower right')
    
    # Add values
    for i, v in enumerate(gsm_acc):
        plt.text(i - width/2, v + 1, f"{v:.0f}", ha='center')
    for i, v in enumerate(tqa_acc):
        plt.text(i + width/2, v + 1, f"{v:.0f}", ha='center')

    plt.savefig('results/final_comparison.png')
    print("Saved results/final_comparison.png")

if __name__ == "__main__":
    main()
