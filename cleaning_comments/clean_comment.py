import re

def clean_comment(comment):
    # Rimuove link
    comment = re.sub(r"http\S+|www\S+|https\S+", "", comment, flags=re.MULTILINE)
    # Rimuove punteggiatura ed emoji
    comment = re.sub(r'[^\w\s]', '', comment)
    # Rimuove caratteri speciali
    comment = re.sub(r'[#@]', '', comment)
    # Converti in minuscolo
    comment = comment.lower()
    # Rimuove spazi extra
    comment = re.sub(r'\s+', ' ', comment).strip()
    return comment

with open("/workspaces/sentiment-analysis/cleaning_comments/all_comments.txt", "r") as f:
    comments = [line.strip() for line in f.readlines()]

cleaned_comments = [clean_comment(comment) for comment in comments if clean_comment(comment)]

# Salva i commenti puliti
with open("/workspaces/sentiment-analysis/cleaning_comments/cleaned_comments.txt", "w") as f:
    for comment in cleaned_comments:
        f.write(comment + "\n")