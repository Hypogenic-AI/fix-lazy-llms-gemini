from datasets import load_from_disk

def main():
    print("Loading GSM8K...")
    gsm8k = load_from_disk("datasets/gsm8k")
    print("GSM8K Keys:", gsm8k.keys())
    print("GSM8K Columns:", gsm8k['test'].column_names)
    print("GSM8K Sample:", gsm8k['test'][0])

    print("\nLoading TruthfulQA...")
    tqa = load_from_disk("datasets/truthful_qa")
    print("TQA Keys:", tqa.keys())
    print("TQA Columns:", tqa['validation'].column_names)
    print("TQA Sample:", tqa['validation'][0])

if __name__ == "__main__":
    main()

