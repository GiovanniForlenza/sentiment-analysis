# Analisi del Sentiment sulla Maternità Surrogata nei Social Media

Questo progetto, sviluppato per l'esame di Reti Geografiche, si concentra sull'analisi del sentiment dei commenti sui social media riguardanti la recente legge italiana che ha reso la maternità surrogata un reato universale.

## 📋 Descrizione del Progetto

Il progetto si articola in diverse fasi:
1. Raccolta di commenti da Reddit relativi alla legge sulla maternità surrogata
2. Creazione di un dataset strutturato con i commenti raccolti
3. Identificazione dei commenti ironici utilizzando le API di OpenAI
4. Preprocessing dei testi utilizzando spaCy
5. Analisi del sentiment attraverso due approcci:
   - Utilizzo del modello Feel-IT
   - Analisi tramite API OpenAI

## 🛠️ Tecnologie Utilizzate

- **Python**: Linguaggio di programmazione principale
- **PRAW (Python Reddit API Wrapper)**: Per la raccolta dei commenti da Reddit
- **OpenAI API**: Per l'identificazione dell'ironia e l'analisi del sentiment
- **spaCy**: Per il preprocessing e la pulizia dei testi
- **Feel-IT**: Modello di sentiment analysis specifico per la lingua italiana
- **Pandas**: Per la manipolazione e l'analisi dei dati

## 🚀 Installazione

```bash
# Clona il repository
git clone https://github.com/GiovanniForlenza/sentiment-analysis.git

# Entra nella directory del progetto
cd sentiment-analysis

# Installa le dipendenze
pip install -r requirements.txt

# Configura le variabili d'ambiente per le API keys
```

## 📊 Risultati

Il progetto ha permesso di:
- Analizzare il sentiment generale della popolazione sui social media riguardo la legge sulla maternità surrogata
- Confrontare i risultati ottenuti attraverso diversi approcci di analisi

## 📝 Note

- È necessario configurare le proprie API key di OpenAI
- I commenti raccolti sono stati anonimizzati per proteggere la privacy degli utenti
