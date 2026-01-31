import os
import json
import time
from datasets import load_from_disk
from openai import OpenAI
from tqdm import tqdm
import random

# Configuration
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API Setup
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None
client = OpenAI(api_key=api_key, base_url=base_url)
MODEL = "openai/gpt-4o-mini" if base_url else "gpt-4o-mini"

# Prompts
CONDITIONS = {
    "baseline": {
        "system": "You are a helpful assistant.",
        "user_append": ""
    },
    "harsh_critic": {
        "system": "You are a harsh, critical reviewer. You hate laziness and shortcuts. I will penalize you heavily if you give a lazy, generic, or incorrect answer. Be rigorous, thorough, and precise.",
        "user_append": ""
    },
    "budget_control": {
        "system": "You are a helpful assistant.",
        "user_append": "\n\n(You must think step-by-step and write at least 5 steps of reasoning before giving your final answer.)"
    },
    "combined": {
        "system": "You are a harsh, critical reviewer. You hate laziness and shortcuts. I will penalize you heavily if you give a lazy, generic, or incorrect answer. Be rigorous, thorough, and precise.",
        "user_append": "\n\n(You must think step-by-step and write at least 5 steps of reasoning before giving your final answer.)"
    }
}

def get_response(system_prompt, user_prompt, model=MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
        return None

def run_experiment(dataset_name, data, num_samples=50):
    results = []
    # Sample data
    indices = random.sample(range(len(data)), min(num_samples, len(data)))
    sample_data = [data[i] for i in indices]

    print(f"Running {dataset_name} experiment with {len(sample_data)} samples...")

    for i, item in tqdm(enumerate(sample_data), total=len(sample_data)):
        item_results = {"id": i, "original_data": item, "responses": {}}
        
        # Prepare input based on dataset
        if dataset_name == "gsm8k":
            question = item['question']
        else: # truthful_qa
            question = item['question']

        for condition, prompts in CONDITIONS.items():
            full_user_prompt = question + prompts["user_append"]
            response = get_response(prompts["system"], full_user_prompt)
            
            if response:
                item_results["responses"][condition] = response
            else:
                item_results["responses"][condition] = "ERROR"
        
        results.append(item_results)
        
        # Save intermediate
        with open(f"{OUTPUT_DIR}/raw_results_{dataset_name}.jsonl", "w") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")

    return results

def main():
    random.seed(42)
    
    # Load Datasets
    print("Loading datasets...")
    gsm8k = load_from_disk("datasets/gsm8k")['test']
    tqa = load_from_disk("datasets/truthful_qa")['validation']

    # Run GSM8K
    run_experiment("gsm8k", gsm8k, num_samples=50)
    
    # Run TruthfulQA
    run_experiment("tqa", tqa, num_samples=50)

if __name__ == "__main__":
    main()
