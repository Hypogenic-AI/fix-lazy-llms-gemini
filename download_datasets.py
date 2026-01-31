from datasets import load_dataset
import os
import json

os.makedirs("datasets", exist_ok=True)

# 1. GSM8K
print("Downloading GSM8K...")
gsm8k = load_dataset("gsm8k", "main")
gsm8k.save_to_disk("datasets/gsm8k")

# 2. TruthfulQA
print("Downloading TruthfulQA...")
truthful_qa = load_dataset("truthful_qa", "generation")
truthful_qa.save_to_disk("datasets/truthful_qa")

# Create .gitignore
with open("datasets/.gitignore", "w") as f:
    f.write("*\n!.gitignore\n!README.md\n!**/samples.json\n")

# Create README
readme_content = """# Downloaded Datasets

## 1. GSM8K
- **Task**: Grade School Math (Reasoning)
- **Location**: datasets/gsm8k
- **Loading**:
  ```python
  from datasets import load_from_disk
  dataset = load_from_disk("datasets/gsm8k")
  ```

## 2. TruthfulQA
- **Task**: Truthfulness / Hallucination
- **Location**: datasets/truthful_qa
- **Loading**:
  ```python
  from datasets import load_from_disk
  dataset = load_from_disk("datasets/truthful_qa")
  ```
"""
with open("datasets/README.md", "w") as f:
    f.write(readme_content)

# Save samples
def save_sample(dataset, name):
    # Select validation or test or train
    if 'test' in dataset:
        split = 'test'
    elif 'validation' in dataset:
        split = 'validation'
    else:
        split = 'train'
        
    sample = [dict(x) for x in dataset[split].select(range(5))]
    os.makedirs(f"datasets/{name}", exist_ok=True)
    with open(f"datasets/{name}/samples.json", "w") as f:
        json.dump(sample, f, indent=2)

save_sample(gsm8k, "gsm8k")
save_sample(truthful_qa, "truthful_qa")