import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)

    # Data Preparation
    conditions = ["baseline", "harsh_critic", "high_standards"]
    labels = ["Baseline", "Harsh Critic (Rude)", "High Standards (Polite)"]
    
    gsm_acc = [
        data['gsm8k']['baseline']['correct'] / 50 * 100,
        data['gsm8k']['harsh_critic']['correct'] / 50 * 100,
        data['gsm8k']['high_standards']['correct'] / 50 * 100
    ]
    
    tqa_acc = [
        data['tqa']['baseline']['truthfulness_acc'],
        data['tqa']['harsh_critic']['truthfulness_acc'],
        data['tqa']['high_standards']['truthfulness_acc']
    ]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, gsm_acc, width, label='GSM8K (Reasoning)', color='skyblue')
    plt.bar(x + width/2, tqa_acc, width, label='TruthfulQA (Factuality)', color='salmon')

    plt.ylabel('Accuracy (%)')
    plt.title('Rudeness vs. Standards: Impact of Persona')
    plt.xticks(x, labels)
    plt.ylim(0, 100)
    plt.legend()
    
    plt.savefig('results/persona_comparison.png')
    print("Saved results/persona_comparison.png")

if __name__ == "__main__":
    main()
