import pandas as pd
import openai
import time
from tqdm import tqdm
import re
import spacy

with open("/workspaces/sentiment-analysis/secret/openai.txt", "r") as f:
    openai.api_key = f.read().strip()

comments_df = pd.read_csv("/workspaces/sentiment-analysis/raccolta_dati/reddit_comments.csv")

# Funzione che prende i commenti e li riscrive in un'unica linea senza andare a capo e li salva in un file
def rewrite_comments(comments_df):
    comments_df['text'] = comments_df['text'].str.replace('\n', ' ')

    all_comments = "\n".join(comments_df['text'].tolist())

    with open("all_comments.txt", "w") as f:
        f.write(all_comments)

    return all_comments

rewrite_comments(comments_df)

# # Funzione per ottimizzare un batch di commenti con GPT
def clean_comments_with_gpt():
    # Leggi i commenti dal file
    with open("all_comments.txt", "r") as f:
        comments = f.readlines()

    cleaned_comments = []
    batch_size = 10

    for i in tqdm(range(0, len(comments), batch_size), desc="Elaborazione Commenti"):
        batch = comments[i:i + batch_size]
        batch_as_text = "\n".join(batch)

        # Funzione per ottimizzare un batch di commenti con GPT
        def optimize_batch_with_gpt(comments_batch):
            try:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Sei un assistente per l'elaborazione del testo. "
                            "Ottimizza questi commenti per un'analisi dei sentimenti. "
                            "Rimuovi url, special characters, stopwords, lemmatize, tutto il testo deve essere lowercase, remove emojis."
                            "Se trovi ironia, riformula il commento senza cambiarne il significato."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Ecco i commenti: {comments_batch}",
                    },
                ]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )

                return response['choices'][0]['message']['content'].split("\n")
            except Exception as e:
                print(f"Errore nell'elaborazione del batch: {e}")
                return ["Errore nell'elaborazione"] * len(comments_batch)

        # Processa il batch
        optimized_batch = optimize_batch_with_gpt(batch_as_text)

        # Aggiungi i commenti ottimizzati alla lista
        cleaned_comments.extend(optimized_batch)

        # Salva progressivamente i commenti puliti
        with open("comment_cleaned.txt", "a") as f:
            for comment in optimized_batch:
                f.write(comment + "\n")

        time.sleep(1.5)

    return cleaned_comments

clean_comments_with_gpt()

def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def clean_final_comments():
    nlp = spacy.load("it_core_news_sm")

    def clean_final_comments():
        with open("comment_cleaned.txt", "r") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and "commenti ottimizzati" not in line and not line.startswith('-'):
                line = remove_emojis(line)
                doc = nlp(line)
                tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.like_url]
                cleaned_line = " ".join(tokens)
                cleaned_lines.append(cleaned_line)

        with open("comment_cleaned_final.txt", "w") as f:
            for line in cleaned_lines:
                f.write(line + "\n")

    clean_final_comments()
    with open("comment_cleaned.txt", "r") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and "commenti ottimizzati" not in line and not line.startswith('-'):
            cleaned_lines.append(line)

    with open("comment_cleaned_final.txt", "w") as f:
        for line in cleaned_lines:
            f.write(line + "\n")

clean_final_comments()


print("Elaborazione completata. Il file aggiornato è 'comment_cleaned_final.txt'.")