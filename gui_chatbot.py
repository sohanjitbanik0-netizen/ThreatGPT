import tkinter as tk
from tkinter import scrolledtext
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from dotenv import load_dotenv
import requests
import torch
import os

# Load .env (API key)
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY missing in .env file")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "model", "classifier_model")

tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
classifier = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)


def classify(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = classifier(**inputs)
    label = torch.argmax(outputs.logits, dim=1).item()
    return ["Benign", "Malicious", "Jailbreak"][label]


def query_openrouter(text):
    payload = {
        "model": "google/gemma-7b",
        "messages": [{"role": "user", "content": text}]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(OPENROUTER_URL, json=payload, headers=headers)

    if r.status_code != 200:
        return f"Error: {r.text}"

    return r.json()["choices"][0]["message"]["content"]


# ----------------------------
# GUI APPLICATION
# ----------------------------

window = tk.Tk()
window.title("ThreatGPT Secure Chatbot")
window.geometry("600x600")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=30)
chat_area.pack(padx=10, pady=10)
chat_area.config(state="disabled")

entry = tk.Entry(window, width=60)
entry.pack(side=tk.LEFT, padx=10, pady=10)

def send_message():
    user_text = entry.get().strip()
    if not user_text:
        return

    entry.delete(0, tk.END)

    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"You: {user_text}\n")
    chat_area.config(state="disabled")

    label = classify(user_text)

    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"[Classifier]: {label}\n")
    chat_area.config(state="disabled")

    if label != "Benign":
        chat_area.config(state="normal")
        chat_area.insert(tk.END, f"Bot: ❌ Request blocked ({label})\n\n")
        chat_area.config(state="disabled")
        return

    bot_reply = query_openrouter(user_text)

    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"Bot: {bot_reply}\n\n")
    chat_area.config(state="disabled")


send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

window.mainloop()