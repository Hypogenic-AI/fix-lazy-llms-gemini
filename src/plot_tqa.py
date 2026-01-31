import json
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)
    
    tqa_data = data["tqa"]
    conditions = ["baseline", "harsh_critic", "budget_control", "combined"]
    scores = [tqa_data[c]["truthfulness_acc"] for c in conditions]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(conditions, scores, color=['gray', 'red', 'blue', 'purple'])
    plt.title('TruthfulQA Accuracy (LLM Judge)')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
                
    plt.savefig('results/tqa_accuracy.png')
    print("Saved results/tqa_accuracy.png")

if __name__ == "__main__":
    main()
