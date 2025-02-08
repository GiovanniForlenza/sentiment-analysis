import pandas as pd
import numpy as np

def analyze_sentiment_emotion():

    feelit_df = pd.read_csv('/workspaces/sentiment-analysis/model/result_feelit.csv')
    openai_df = pd.read_csv('/workspaces/sentiment-analysis/model/results_openai_cleaned_comments.csv')
    

    openai_df = openai_df.rename(columns={'Commento': 'Comment'})
    

    print("FEELIT ANALYSIS")
    print("===============")
    

    feelit_sentiment = feelit_df['Sentiment'].value_counts()
    print("\nSentiment Distribution:")
    for sentiment, count in feelit_sentiment.items():
        percentage = (count/len(feelit_df))*100
        print(f"{sentiment}: {count} ({percentage:.1f}%)")
    

    feelit_emotion = feelit_df['Emotion'].value_counts()
    print("\nEmotion Distribution:")
    for emotion, count in feelit_emotion.items():
        percentage = (count/len(feelit_df))*100
        print(f"{emotion}: {count} ({percentage:.1f}%)")
    

    print("\nOPENAI ANALYSIS")
    print("===============")
    

    openai_sentiment = openai_df['Sentiment'].value_counts()
    print("\nSentiment Distribution:")
    for sentiment, count in openai_sentiment.items():
        percentage = (count/len(openai_df))*100
        print(f"{sentiment}: {count} ({percentage:.1f}%)")

    openai_emotion = openai_df['Emotion'].value_counts()
    print("\nEmotion Distribution:")
    for emotion, count in openai_emotion.items():
        percentage = (count/len(openai_df))*100
        print(f"{emotion}: {count} ({percentage:.1f}%)")
    

    print("\nANALISI CORRISPONDENZE NEUTRO/ERRORE")
    print("====================================")
    

    merged_df = pd.merge(openai_df, feelit_df, on='Comment')
    

    neutral_mask = merged_df['Sentiment_x'] == 'neutro'
    neutral_analysis = merged_df[neutral_mask].groupby(['Sentiment_y', 'Emotion_y']).size()
    
    print("\nClassificazione Feelit dei commenti neutri di OpenAI:")
    total_neutral = neutral_mask.sum()
    for (sentiment, emotion), count in neutral_analysis.items():
        percentage = (count/total_neutral)*100
        print(f"{sentiment}-{emotion}: {count} ({percentage:.1f}%)")
    print(f"Totale commenti neutri: {total_neutral}")
    

    error_mask = merged_df['Sentiment_x'] == 'Errore'
    error_analysis = merged_df[error_mask].groupby(['Sentiment_y', 'Emotion_y']).size()
    
    print("\nClassificazione Feelit dei commenti errore di OpenAI:")
    total_error = error_mask.sum()
    for (sentiment, emotion), count in error_analysis.items():
        percentage = (count/total_error)*100
        print(f"{sentiment}-{emotion}: {count} ({percentage:.1f}%)")
    print(f"Totale commenti errore: {total_error}")

if __name__ == "__main__":
    analyze_sentiment_emotion()