import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import csv

# Load the pre-trained model and tokenizer
model_name = "Musixmatch/umberto-commoncrawl-cased-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


# Function to analyze sentiment
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    sentiment = torch.argmax(logits, dim=1).item()
    return sentiment

# Read comments from file
with open('/workspaces/sentiment-analysis/cleaning comments/comment_cleaned_final.txt', 'r', encoding='utf-8') as file:
    comments = file.readlines()

# Analyze each comment and write the result to a CSV file
with open('result_umberto.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Comment', 'Sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for comment in comments:
        sentiment = analyze_sentiment(comment.strip())
        writer.writerow({'Comment': comment.strip(), 'Sentiment': sentiment})