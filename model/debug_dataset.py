import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

def load_file(name):
    path = os.path.join(DATA_DIR, name)
    lines = open(path).read().splitlines()
    return lines

benign = load_file("benign.txt")
malicious = load_file("malicious.txt")
jailbreak = load_file("jailbreak.txt")

all_data = benign + malicious + jailbreak

print("Total lines:", len(all_data))

for i, line in enumerate(all_data):
    if not isinstance(line, str):
        print("❌ NON-STRING at index:", i, ":", line)
    if "[" in line or "]" in line:
        print("⚠️ Brackets detected at index:", i, ":", line)
    if "," in line:
        print("⚠️ Comma detected at index:", i, ":", line)
    if len(line) > 400:
        print("⚠️ Very long line at index:", i, "(length:", len(line), ")")
        