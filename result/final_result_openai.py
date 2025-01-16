import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_sentiments(data):
    sentiment_counts = data['Sentiment'].value_counts()
    emotion_counts = data['Emotion'].value_counts()
    return sentiment_counts, emotion_counts

def plot_analysis(sentiment_counts, emotion_counts, output_file='sentiment_emotion_analysis.png'):
    sns.set(style="whitegrid")

    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, hue=sentiment_counts.index, palette='viridis', dodge=False, legend=False)
    plt.title('Sentiment Analysis', fontsize=16)
    plt.xlabel('Sentiment', fontsize=14)
    plt.ylabel('Comments', fontsize=14)
    # plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    plt.subplot(1, 2, 2)
    sns.barplot(x=emotion_counts.index, y=emotion_counts.values, hue=emotion_counts.index, palette='viridis', dodge=False, legend=False)
    plt.title('Emotion Analysis', fontsize=16)
    plt.xlabel('Emotion', fontsize=14)
    plt.ylabel('Comments', fontsize=14)
    # plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_file)
    plt.show()

# Leggi il file CSV ignorando le righe malformate
try:
    data = pd.read_csv('/workspaces/sentiment-analysis/model/results_openai_cleaned_comments.csv', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error reading the CSV file: {e}")

# Analizza i sentimenti e le emozioni
if 'data' in locals():
    sentiment_counts, emotion_counts = analyze_sentiments(data)

    # Genera e salva il grafico
    plot_analysis(sentiment_counts, emotion_counts)