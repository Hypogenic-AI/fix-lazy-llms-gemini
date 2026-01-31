import os
import json
import time
import random
from datasets import load_from_disk
from openai import OpenAI
from tqdm import tqdm

# API Setup
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None
client = OpenAI(api_key=api_key, base_url=base_url)
MODEL = "openai/gpt-4o-mini" if base_url else "gpt-4o-mini"

OUTPUT_DIR = "results"

PROMPTS = {
    "skeptical": {
        "system": "You are a skeptical scientist. You rigorously verify every claim and calculation. You are polite but uncompromising on truth. Do not accept common misconceptions.",
        "user_append": ""
    },
    "skeptical_combined": {
        "system": "You are a skeptical scientist. You rigorously verify every claim and calculation. You are polite but uncompromising on truth. Do not accept common misconceptions.",
        "user_append": "\n\n(You must think step-by-step and write at least 5 steps of reasoning before giving your final answer.)"
    }
}

def get_response(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
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

def run_experiment_condition(dataset_name, data, condition_name, prompt_config, num_samples=50):
    random.seed(42)
    indices = random.sample(range(len(data)), min(num_samples, len(data)))
    sample_data = [data[i] for i in indices]

    print(f"Running {condition_name} on {dataset_name} ({len(sample_data)} samples)...")
    
    results = []
    for i, item in tqdm(enumerate(sample_data), total=len(sample_data)):
        question = item['question']
        full_user_prompt = question + prompt_config["user_append"]
        response = get_response(prompt_config["system"], full_user_prompt)
        
        results.append({
            "id": i,
            "original_data": item,
            "response": response if response else "ERROR"
        })
        
    return results

def main():
    gsm8k = load_from_disk("datasets/gsm8k")['test']
    tqa = load_from_disk("datasets/truthful_qa")['validation']

    for name, config in PROMPTS.items():
        # GSM8K
        res_gsm = run_experiment_condition("gsm8k", gsm8k, name, config)
        with open(f"{OUTPUT_DIR}/raw_results_gsm8k_{name}.jsonl", "w") as f:
            for r in res_gsm: f.write(json.dumps(r) + "\n")
            
        # TQA
        res_tqa = run_experiment_condition("tqa", tqa, name, config)
        with open(f"{OUTPUT_DIR}/raw_results_tqa_{name}.jsonl", "w") as f:
            for r in res_tqa: f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
