from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch

model_path = "model/classifier_model"

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

labels = ["Benign", "Malicious", "Jailbreak"]

print("ThreatGPT Classifier – Interactive Mode")
print("Type 'exit' to stop.\n")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        break

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    pred = torch.argmax(outputs.logits).item()

    print("Prediction:", labels[pred], "\n")