import pandas as pd

def analyze_sentiment_emotion():
    # Caricamento dei dataset
    feelit_df = pd.read_csv('/workspaces/sentiment-analysis/model/result_feelit.csv')
    openai_df = pd.read_csv('/workspaces/sentiment-analysis/model/results_openai_cleaned_comments.csv')

    # Rinomina colonna per uniformità
    openai_df = openai_df.rename(columns={'Commento': 'Comment'})

    # Rimozione duplicati
    dup_feelit = feelit_df.duplicated(subset=['Comment']).sum()
    dup_openai = openai_df.duplicated(subset=['Comment']).sum()
    feelit_df = feelit_df.drop_duplicates(subset=['Comment'])
    openai_df = openai_df.drop_duplicates(subset=['Comment'])

    # Merge dei dataset
    merged_df = pd.merge(openai_df, feelit_df, on='Comment', how='inner')

    # Statistiche dataset
    total_rows_merged = len(merged_df)
    only_in_openai = len(openai_df) - total_rows_merged
    only_in_feelit = len(feelit_df) - total_rows_merged

    print(f"Duplicati in Feelit: {dup_feelit}")
    print(f"Duplicati in OpenAI: {dup_openai}")
    print(f"Totale righe dopo merge: {total_rows_merged}")
    print(f"Commenti in OpenAI ma non in Feelit: {only_in_openai}")
    print(f"Commenti in Feelit ma non in OpenAI: {only_in_feelit}\n")

    # Analisi della distribuzione dei sentimenti ed emozioni
    def print_distribution(df, title):
        print(f"\n{title}")
        print("=" * len(title))

        sentiment_counts = df['Sentiment'].value_counts()
        print("\nSentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(df)) * 100
            print(f"{sentiment}: {count} ({percentage:.1f}%)")

        emotion_counts = df['Emotion'].value_counts()
        print("\nEmotion Distribution:")
        for emotion, count in emotion_counts.items():
            percentage = (count / len(df)) * 100
            print(f"{emotion}: {count} ({percentage:.1f}%)")

    print_distribution(feelit_df, "FEELIT ANALYSIS")
    print_distribution(openai_df, "OPENAI ANALYSIS")

    # Analisi delle corrispondenze per commenti "neutro" ed "errore" in OpenAI
    def analyze_classification(label, mask):
        filtered_df = merged_df[mask].groupby(['Sentiment_y', 'Emotion_y']).size()
        total_count = mask.sum()

        print(f"\nClassificazione FeelIt dei commenti {label} di OpenAI:")
        print(filtered_df)
        print(f"Totale conteggio {label}: {total_count}")

    analyze_classification("neutri", merged_df['Sentiment_x'] == 'neutro')
    analyze_classification("errore", merged_df['Sentiment_x'] == 'Errore')

if __name__ == "__main__":
    analyze_sentiment_emotion()
