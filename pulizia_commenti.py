import pandas as pd
import openai
import time
from tqdm import tqdm

# Leggi la chiave API da un file
with open("openai.txt", "r") as f:
    openai.api_key = f.read().strip()

# Carica i dati
comments_df = pd.read_csv("reddit_comments.csv")

# Funzione per ottimizzare un batch di commenti con GPT
def optimize_batch_with_gpt(comments_batch):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei un assistente per l'elaborazione del testo. "
                    "Ottimizza questi commenti per un'analisi dei sentimenti. "
                    "Rimuovi rumore, rendi il testo chiaro e normale, e indica se c'è ironia. "
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

        # Estrai i risultati dal completamento
        return response['choices'][0]['message']['content'].split("\n")
    except Exception as e:
        print(f"Errore nell'elaborazione del batch: {e}")
        return ["Errore nell'elaborazione"] * len(comments_batch)

# Funzione per elaborare i commenti in batch e salvare progressivamente
def process_comments_with_progressive_saving(comments_df, batch_size=10):
    # Verifica se esiste già una colonna di testo ottimizzato
    if 'optimized_text' not in comments_df.columns:
        comments_df['optimized_text'] = ""

    # Identifica gli indici non ancora elaborati
    unprocessed_indices = comments_df[comments_df['optimized_text'] == ""].index.tolist()

    for i in tqdm(range(0, len(unprocessed_indices), batch_size), desc="Elaborazione Commenti"):
        # Prendi il batch di indici
        batch_indices = unprocessed_indices[i:i + batch_size]
        batch = comments_df.loc[batch_indices, 'text'].tolist()

        # Combina i commenti in un batch
        batch_as_text = "\n".join(batch)

        # Processa il batch
        optimized_batch = optimize_batch_with_gpt(batch_as_text)

        # Salva i risultati nel DataFrame
        for idx, optimized_text in zip(batch_indices, optimized_batch):
            comments_df.at[idx, 'optimized_text'] = optimized_text

        # Salva progressivamente il DataFrame
        comments_df.to_csv("reddit_comments_optimized.csv", index=False)
        time.sleep(1.5)  # Rispetta i limiti delle API

    return comments_df

# Avvia l'elaborazione
comments_df = process_comments_with_progressive_saving(comments_df, batch_size=10)

print("Elaborazione completata. Il file aggiornato è 'reddit_comments_optimized.csv'.")