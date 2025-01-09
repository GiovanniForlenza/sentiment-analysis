import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy

# Carica i dati (commenti) dal CSV
comments_df = pd.read_csv("reddit_comments.csv")

# Inizializza la lingua per stopwords e spacy
nltk.download('stopwords')
stop_words = set(stopwords.words('italian'))
nlp = spacy.load('it_core_news_sm')

# Funzioni di pre-elaborazione
def remove_urls(text):
    return re.sub(r'http\S+|www\S+|https\S+', '', text)

def remove_special_chars(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stop_words])

def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def preprocess_text(text):
    text = remove_urls(text)
    text = remove_special_chars(text)
    text = text.lower()
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    text = remove_emojis(text)
    return text

# Applica la pre-elaborazione a ogni commento
comments_df['cleaned_text'] = comments_df['text'].apply(preprocess_text)

# Seleziona solo la colonna del testo ripulito
cleaned_df = comments_df[['cleaned_text']]

# Salva solo la colonna cleaned_text in un nuovo CSV
cleaned_df.to_csv("reddit_comments_cleaned.csv", index=False)

print("Pulizia e pre-elaborazione completata. Il file è stato salvato in 'reddit_comments_cleaned.csv'.")