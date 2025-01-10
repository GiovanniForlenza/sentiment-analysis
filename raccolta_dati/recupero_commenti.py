import praw
from langdetect import DetectorFactory
import pandas as pd

with open("/workspaces/sentiment-analysis/secret/client_ID.txt", "r") as f:
    client_id = f.read().strip()

with open("/workspaces/sentiment-analysis/secret/client_secret.txt", "r") as f:
    client_secret = f.read().strip()

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="sentiment-analysis-surrogacy/0.1"
)

queries = ['"maternità surrogata" AND legge', '"reato universale" AND maternità', '"legge 19 febbraio 2004"', '"utero in affitto"', '"reato universale"', '"maternita surrogata"']
keywords = ["maternità surrogata", "reato universale", "legge 19 febbraio 2004", "utero in affitto"]

DetectorFactory.seed = 0

processed_ids = set()
posts = []
comments = []
comments_ids = set()

def get_comments(submission):
    submission.comments.replace_more(limit=0)
    comments_data = []
    for comment in submission.comments.list():
        comments_data.append({
            "submission_id": submission.id,
            "comment_id": comment.id,
            "text": comment.body,
            "score": comment.score
        })
    return comments_data

for query in queries:
    for submission in reddit.subreddit("all").search(query, sort="relevance"):        
        if submission.id not in processed_ids and submission.created_utc:
            if any(keyword in submission.title.lower() or keyword in submission.selftext.lower() for keyword in keywords):
                processed_ids.add(submission.id)

                posts.append({
                    "id": submission.id,
                    "title": submission.title,
                    "text": submission.selftext,
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "num_comments": submission.num_comments
                })

                submission_comments = get_comments(submission)
                for comment in submission_comments: 
                    if comment["comment_id"] not in comments_ids:
                        comments_ids.add(comment["comment_id"])
                        comments.append(comment)

posts_df = pd.DataFrame(posts)
posts_df.to_csv("reddit_posts.csv", index=False)

comments_df = pd.DataFrame(comments)
comments_df.to_csv("reddit_comments.csv", index=False)

print(f"Dataset salvato: {len(posts)} post e {len(comments)} commenti.")
