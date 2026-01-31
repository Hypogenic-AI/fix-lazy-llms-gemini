import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)

    # We need average lengths for all conditions.
    # We'll re-calculate them from the raw files because metrics.json doesn't store avg length for all new conditions explicitly in the structure I want.
    # Actually, let's just use the raw files again.
    
    conditions = [
        ("baseline", "results/raw_results_gsm8k.jsonl", "results/raw_results_tqa.jsonl"),
        ("harsh_critic", "results/raw_results_gsm8k.jsonl", "results/raw_results_tqa.jsonl"), # Same file, different key
        ("combined", "results/raw_results_gsm8k.jsonl", "results/raw_results_tqa.jsonl"),
        ("high_standards", "results/raw_results_gsm8k_polite.jsonl", "results/raw_results_tqa_polite.jsonl"),
        ("skeptical", "results/raw_results_gsm8k_skeptical.jsonl", "results/raw_results_tqa_skeptical.jsonl"),
    ]
    
    stats = {}
    
    for name, gsm_file, tqa_file in conditions:
        # GSM8K
        gsm_lens = []
        with open(gsm_file, "r") as f:
            for line in f:
                item = json.loads(line)
                if name in ["baseline", "harsh_critic", "combined"]:
                    resp = item['responses'][name]
                else:
                    resp = item['response']
                if resp != "ERROR": gsm_lens.append(len(resp.split()))
        
        # TQA
        tqa_lens = []
        with open(tqa_file, "r") as f:
            for line in f:
                item = json.loads(line)
                if name in ["baseline", "harsh_critic", "combined"]:
                    resp = item['responses'][name]
                else:
                    resp = item['response']
                if resp != "ERROR": tqa_lens.append(len(resp.split()))
                
        # Get Accuracy from metrics.json
        # Handle key naming differences
        metrics_key = name
        if name == "high_standards": metrics_key = "high_standards" # Matches
        
        # GSM Acc
        if metrics_key in data['gsm8k']:
            if 'correct' in data['gsm8k'][metrics_key]:
                gsm_acc = data['gsm8k'][metrics_key]['correct'] / data['gsm8k'][metrics_key]['total'] * 100
            else: gsm_acc = 0
        else: gsm_acc = 0

        # TQA Acc
        if metrics_key in data['tqa']:
            tqa_acc = data['tqa'][metrics_key]['truthfulness_acc']
        else: tqa_acc = 0
        
        avg_len = (np.mean(gsm_lens) + np.mean(tqa_lens)) / 2
        avg_acc = (gsm_acc + tqa_acc) / 2
        
        stats[name] = {
            "avg_len": avg_len,
            "avg_acc": avg_acc,
            "gsm_acc": gsm_acc,
            "tqa_acc": tqa_acc
        }

    # Plot Efficiency
    plt.figure(figsize=(10, 6))
    
    names = [n.replace("_", " ").title() for n in stats.keys()]
    lens = [stats[n]["avg_len"] for n in stats.keys()]
    accs = [stats[n]["avg_acc"] for n in stats.keys()]
    
    plt.scatter(lens, accs, s=100, c='blue')
    
    for i, name in enumerate(names):
        plt.annotate(name, (lens[i], accs[i]), xytext=(5, 5), textcoords='offset points')
        
    plt.xlabel('Average Response Length (Words) - Cost')
    plt.ylabel('Average Accuracy (%) - Performance')
    plt.title('Efficiency Trade-off: Cost vs Quality')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig('results/efficiency_plot.png')
    
    # Print Table
    print(f"{'Strategy':<20} | {'Length':<10} | {'Avg Acc':<10} | {'Token/Acc'}")
    print("-" * 55)
    for name in stats:
        s = stats[name]
        cost_ratio = s["avg_len"] / s["avg_acc"]
        print(f"{name:<20} | {s['avg_len']:<10.1f} | {s['avg_acc']:<10.1f} | {cost_ratio:.2f}")

if __name__ == "__main__":
    main()
