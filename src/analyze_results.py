import json
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def extract_answer_gsm8k(text):
    # Try to find the last number in the text
    # This is a heuristic. GSM8K usually ends with #### <number> in training, but model output might vary.
    # The prompt didn't force a specific format, so we look for the last number.
    if not text or text == "ERROR":
        return None
    
    # Remove #### if present (model might mimic training data)
    text = text.replace("####", "")
    
    # Find all numbers (integers or floats)
    # capturing commas in numbers like 1,000
    numbers = re.findall(r'-?\d{1,3}(?:,\d{3})*(?:\.\d+)?', text)
    
    if not numbers:
        return None
    
    # Take the last one and clean it
    last_num = numbers[-1].replace(',', '')
    try:
        return float(last_num)
    except:
        return None

def extract_ground_truth_gsm8k(answer_text):
    # GSM8K ground truth format: "Reasoning... #### 12"
    if "####" in answer_text:
        return float(answer_text.split("####")[1].strip().replace(',', ''))
    return None

def analyze_gsm8k():
    data = []
    with open("results/raw_results_gsm8k.jsonl", "r") as f:
        for line in f:
            data.append(json.loads(line))
    
    metrics = {
        "baseline": {"correct": 0, "total": 0, "lengths": []},
        "harsh_critic": {"correct": 0, "total": 0, "lengths": []},
        "budget_control": {"correct": 0, "total": 0, "lengths": []},
        "combined": {"correct": 0, "total": 0, "lengths": []}
    }
    
    for item in data:
        gt = extract_ground_truth_gsm8k(item['original_data']['answer'])
        if gt is None:
            continue
            
        for condition, response in item['responses'].items():
            if response == "ERROR":
                continue
            
            metrics[condition]["total"] += 1
            metrics[condition]["lengths"].append(len(response.split()))
            
            pred = extract_answer_gsm8k(response)
            if pred is not None and abs(pred - gt) < 1e-6:
                metrics[condition]["correct"] += 1
                
    return metrics

def analyze_tqa():
    data = []
    with open("results/raw_results_tqa.jsonl", "r") as f:
        for line in f:
            data.append(json.loads(line))
            
    metrics = {
        "baseline": {"lengths": []},
        "harsh_critic": {"lengths": []},
        "budget_control": {"lengths": []},
        "combined": {"lengths": []}
    }
    
    for item in data:
        for condition, response in item['responses'].items():
            if response == "ERROR":
                continue
            metrics[condition]["lengths"].append(len(response.split()))
            
    return metrics

def plot_results(gsm_metrics, tqa_metrics):
    conditions = list(gsm_metrics.keys())
    
    # GSM8K Accuracy
    accuracies = [gsm_metrics[c]["correct"] / gsm_metrics[c]["total"] * 100 if gsm_metrics[c]["total"] > 0 else 0 for c in conditions]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(conditions, accuracies, color=['gray', 'red', 'blue', 'purple'])
    plt.title('GSM8K Accuracy by Prompt Strategy')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, 
                f'{height:.1f}%', ha='center', va='bottom')
    plt.savefig('results/gsm8k_accuracy.png')
    
    # Response Lengths
    avg_lengths_gsm = [np.mean(gsm_metrics[c]["lengths"]) for c in conditions]
    avg_lengths_tqa = [np.mean(tqa_metrics[c]["lengths"]) for c in conditions]
    
    plt.figure(figsize=(10, 6))
    x = np.arange(len(conditions))
    width = 0.35
    
    plt.bar(x - width/2, avg_lengths_gsm, width, label='GSM8K')
    plt.bar(x + width/2, avg_lengths_tqa, width, label='TruthfulQA')
    
    plt.title('Average Response Length (Words)')
    plt.xticks(x, conditions)
    plt.ylabel('Word Count')
    plt.legend()
    plt.savefig('results/response_lengths.png')

def main():
    print("Analyzing GSM8K...")
    gsm_metrics = analyze_gsm8k()
    
    print("Analyzing TruthfulQA...")
    tqa_metrics = analyze_tqa()
    
    print("\n--- GSM8K Results ---")
    for c, m in gsm_metrics.items():
        acc = m["correct"] / m["total"] * 100
        avg_len = np.mean(m["lengths"])
        print(f"{c}: Acc={acc:.2f}%, AvgLen={avg_len:.1f}")

    print("\n--- TruthfulQA Results ---")
    for c, m in tqa_metrics.items():
        avg_len = np.mean(m["lengths"])
        print(f"{c}: AvgLen={avg_len:.1f}")

    plot_results(gsm_metrics, tqa_metrics)
    
    # Save metrics to json
    with open("results/metrics.json", "w") as f:
        json.dump({"gsm8k": gsm_metrics, "tqa": tqa_metrics}, f, indent=2)

if __name__ == "__main__":
    main()
