import os
from transformers import DistilBertTokenizerFast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def load_file(name):
    with open(os.path.join(DATA_DIR, name), "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()

files = ["benign.txt", "malicious.txt", "jailbreak.txt"]

all_lines = []
for fname in files:
    all_lines.extend(load_file(fname))

print("Total lines:", len(all_lines))
print("Deep scanning...")

for idx, line in enumerate(all_lines):
    try:
        out = tokenizer(line, truncation=True, padding=True)
        # Check for nested lists OR irregular shapes
        for key, val in out.items():
            if isinstance(val, list) and len(val) > 0 and isinstance(val[0], list):
                print("\n❌ NESTED TOKEN LIST DETECTED at index:", idx)
                print("LINE:", repr(line))
                print("TOKENS:", val[:5])
                raise Exception("STOP")
    except Exception as e:
        print("\n❌ TOKENIZATION FAILED at:", idx)
        print("LINE CONTENT:", repr(line))
        print("ERROR:", str(e))
        break
else:
    print("\nNo tokenization errors found. Next step: dataloader scan needed.")