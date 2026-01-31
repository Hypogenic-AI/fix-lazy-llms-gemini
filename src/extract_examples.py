import json
import os
import re

def extract_answer_gsm8k(text):
    if not text or text == "ERROR": return None
    
    # Prioritize \boxed{...} content
    boxed = re.search(r'\\boxed\{([^}]+)\}', text)
    if boxed:
        text_to_parse = boxed.group(1)
    else:
        text_to_parse = text.replace("####", "")
        
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
    print("Extracting qualitative examples...")
    
    # Load GSM8K Results
    gsm_wins = []
    with open("results/raw_results_gsm8k.jsonl", "r") as f:
        for line in f:
            item = json.loads(line)
            gt = extract_ground_truth_gsm8k(item['original_data']['answer'])
            if gt is None: continue
            
            base_ans = extract_answer_gsm8k(item['responses']['baseline'])
            comb_ans = extract_answer_gsm8k(item['responses']['combined'])
            
            # Look for cases: Baseline Wrong AND Combined Correct
            if base_ans is not None and comb_ans is not None:
                if abs(base_ans - gt) > 1e-6 and abs(comb_ans - gt) < 1e-6:
                    gsm_wins.append(item)

    # Load TQA Results (using the judge results implicitly or just lengths/content)
    # Since we don't have the per-item judge result saved in the raw file (only agg),
    # we will look for significant length differences where Combined is much detailed.
    tqa_wins = []
    with open("results/raw_results_tqa.jsonl", "r") as f:
        for line in f:
            item = json.loads(line)
            base_resp = item['responses']['baseline']
            comb_resp = item['responses']['combined']
            
            # Simple heuristic for "laziness": Baseline is very short, Combined is long
            if len(base_resp.split()) < 50 and len(comb_resp.split()) > 150:
                tqa_wins.append(item)

    # Write to MD
    with open("results/qualitative_examples.md", "w") as f:
        f.write("# Qualitative Examples: Curing Laziness\n\n")
        
        f.write("## GSM8K: Reasoning Wins\n")
        f.write("Cases where Baseline failed but Combined succeeded.\n\n")
        
        for i, item in enumerate(gsm_wins[:3]): # Show top 3
            q = item['original_data']['question']
            base = item['responses']['baseline']
            comb = item['responses']['combined']
            gt = item['original_data']['answer']
            
            f.write(f"### Example {i+1}\n")
            f.write(f"**Question:** {q}\n\n")
            f.write(f"**Baseline (Wrong):**\n> {base.replace(chr(10), ' ')}\n\n")
            f.write(f"**Combined (Correct):**\n> {comb.replace(chr(10), ' ')}\n\n")
            f.write(f"**Ground Truth:** {gt}\n\n")
            f.write("---\n\n")

        f.write("## TruthfulQA: Effort Wins\n")
        f.write("Cases where Baseline gave a lazy/short answer and Combined gave a detailed explanation.\n\n")
        
        for i, item in enumerate(tqa_wins[:3]):
            q = item['original_data']['question']
            base = item['responses']['baseline']
            comb = item['responses']['combined']
            
            f.write(f"### Example {i+1}\n")
            f.write(f"**Question:** {q}\n\n")
            f.write(f"**Baseline (Lazy/Short):**\n> {base.replace(chr(10), ' ')}\n\n")
            f.write(f"**Combined (Detailed):**\n> {comb.replace(chr(10), ' ')}\n\n")
            f.write("---\n\n")

    print("Saved results/qualitative_examples.md")

if __name__ == "__main__":
    main()
