from feel_it import EmotionClassifier, SentimentClassifier
import csv

# Initialize the classifiers
emotion_classifier = EmotionClassifier()
sentiment_classifier = SentimentClassifier()

# Read the comments from the file
with open('/workspaces/sentiment-analysis/cleaning comments/comment_cleaned_final.txt', 'r') as file:
    comments = file.readlines()

# Open the CSV file and write the header
with open('result_feelit.csv', 'w', newline='') as csvfile:
    fieldnames = ['Comment', 'Emotion', 'Sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Analyze each comment and write to the CSV file
    for comment in comments:
        comment = comment.strip()
        if comment:
            emotion = emotion_classifier.predict([comment])[0]
            sentiment = sentiment_classifier.predict([comment])[0]
            writer.writerow({'Comment': comment, 'Emotion': emotion, 'Sentiment': sentiment})