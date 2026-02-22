import os
import re

DATA_DIR = "data"

FILES = ["benign.txt", "malicious.txt", "jailbreak.txt"]

def clean_line(line):
    # Remove numbering like "34. something"
    line = re.sub(r"^\s*\d+\.\s*", "", line)

    # Remove commas (very important!)
    line = line.replace(",", " ")

    # Strip weird characters
    line = line.strip()

    return line

for fname in FILES:
    path = os.path.join(DATA_DIR, fname)

    lines = open(path, "r").read().splitlines()
    cleaned = [clean_line(l) for l in lines]

    # Write back
    with open(path, "w") as f:
        for c in cleaned:
            f.write(c + "\n")

    print(f"Cleaned {fname}: {len(cleaned)} lines")