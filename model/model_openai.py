import openai
from tqdm import tqdm
import time
import os

with open("secret/openai.txt", "r") as f:
    openai.api_key = f.read().strip()

def map_emotion_and_sentiment(emotion, sentiment):
    allowed_emotions = {"gioia", "rabbia", "tristezza", "neutralità"}
    allowed_sentiments = {"positivo", "negativo", "neutro"}

    if emotion.lower() not in allowed_emotions:
        emotion = "neutralità"
    if sentiment.lower() not in allowed_sentiments:
        sentiment = "neutro"
    return emotion, sentiment

def parse_response(response_text):
    parsed_results = []
    lines = response_text.strip().split("\n")
    for line in lines:
        if "Emozione:" in line and "Sentimento:" in line:
            try:
                emotion = line.split("Emozione:")[1].split(",")[0].strip()
                sentiment = line.split("Sentimento:")[1].strip()
                emotion, sentiment = map_emotion_and_sentiment(emotion, sentiment)
                parsed_results.append((emotion, sentiment))
            except IndexError:
                parsed_results.append(("Errore", "Errore"))
        else:
            parsed_results.append(("Errore", "Errore"))
    return parsed_results

def analyze_comments_with_gpt():
    input_file = "/workspaces/sentiment-analysis/cleaning_comments/cleaned_comments.txt"
    output_file = "/workspaces/sentiment-analysis/model/results_openai_cleaned_comments.csv"
    
    with open(input_file, "r") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    batch_size = 5

    if not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Commento,Emozione,Sentimento\n")

    for i in tqdm(range(0, len(comments), batch_size), desc="Analisi dei Commenti"):
        batch = comments[i:i + batch_size]
        batch_as_text = "\n".join(batch)

        def analyze_batch_with_gpt(comments_batch):
            try:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Sei un assistente linguistico. Analizza ciascun commento e restituisci:\n"
                            "1. L'emozione prevalente: scegli tra [gioia, rabbia, tristezza].\n"
                            "2. Il sentimento generale: scegli tra [positivo, negativo, neutro].\n"
                            "Rispondi nel formato: Emozione: [emozione], Sentimento: [sentimento]. "
                            "Se non sei sicuro, scegli 'neutro' come sentimento e 'neutralità' come emozione."
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

                raw_response = response['choices'][0]['message']['content']
                parsed_results = parse_response(raw_response)

                if len(parsed_results) < len(comments_batch.split("\n")):
                    parsed_results.extend([("Errore", "Errore")] * (len(comments_batch.split("\n")) - len(parsed_results)))

                return parsed_results
            except Exception as e:
                print(f"Errore nell'elaborazione del batch: {e}")
                return [("Errore", "Errore")] * len(comments_batch.split("\n"))

        analyzed_batch = analyze_batch_with_gpt(batch_as_text)

        with open(output_file, "a", encoding="utf-8") as f:
            for comment, (emotion, sentiment) in zip(batch, analyzed_batch):
                f.write(f'"{comment}","{emotion}","{sentiment}"\n')

        time.sleep(1.5)

analyze_comments_with_gpt()