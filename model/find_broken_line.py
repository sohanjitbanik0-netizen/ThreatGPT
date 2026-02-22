import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

def load(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()

files = ["benign.txt", "malicious.txt", "jailbreak.txt"]

all_lines = []
for fname in files:
    path = os.path.join(DATA_DIR, fname)
    print("Loading:", path)
    lines = load(path)
    all_lines.extend(lines)

print("Total lines loaded:", len(all_lines))

def is_bad(line):
    if not isinstance(line, str):
        return True
    if line.strip() == "":
        return True
    # Detect lists disguised as strings
    if line.startswith("[") and line.endswith("]"):
        return True
    # Extra protection: detect accidental JSON
    try:
        parsed = json.loads(line)
        if isinstance(parsed, list):
            return True
    except:
        pass
    return False

for i, line in enumerate(all_lines):
    if is_bad(line):
        print("\n❌ BAD LINE FOUND at index:", i)
        print("CONTENT:", repr(line))
        break
else:
    print("\nNo obvious bad lines found — next step is deeper parsing.")