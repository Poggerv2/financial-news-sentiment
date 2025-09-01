import requests
import praw
import tweepy
from datetime import datetime
import hashlib
import json
from pathlib import Path
from parser_social import parse_reddit_post, parse_tweet
from db import get_mongo_collection

data_path = Path(__file__).resolve().parents[1] / "data" / "raw"
data_path.mkdir(parents=True, exist_ok=True)

articles_col = get_mongo_collection()

def collect_reddit(subreddit_name="cryptocurrency", limit=200, allowed_flairs=None):
    reddit = praw.Reddit(
        client_id="wcgoWTJ2JQdpvKvWDWq0fg",
        client_secret="ipr9OEOC6USZ3iALk1DRnLkMIBMXQw",
        user_agent="financial-news-sentiment"
    )
    posts = reddit.subreddit(subreddit_name).new(limit=limit)
    results = []
    for post in posts:
        parsed = parse_reddit_post(post, allowed_flairs=allowed_flairs)
        if parsed:
            results.append(parsed)
    return results

def collect_twitter(query="bitcoin OR BTC OR crypto", limit=50):
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAPeO3wEAAAAAS7lfw1Z%2F1aENBLB5mYf6AW5hB14%3DiHWH3AqioR36UqQDppVcdrZkW7473xFe6VAVy4d8CZLRhbOff9")
    
    tweets = client.search_recent_tweets(
        query=query,
        max_results=min(limit, 50),
        tweet_fields=["created_at", "public_metrics", "author_id"],
        expansions="author_id",
        user_fields=["username"]
    )
    
    users_map = {u.id: u for u in tweets.includes["users"]} if hasattr(tweets, "includes") else {}
    return [parse_tweet(tweet, users_map) for tweet in tweets.data]

def save_json(data, source="cronista"):
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = data_path / f"{source}_{today}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=2)
    print(f"Guardados {len(data)} artículos en {file_path}")

def save_mongo(data):
    if not data:
        return
    articles_col.insert_many(data)
    print(f"Insertados {len(data)} documentos en MongoDB")

# --- Main ---
def main():
    reddit_data = collect_reddit("cryptocurrency", limit=200, allowed_flairs=["GENERAL-NEWS"])
    #twitter_data = collect_twitter(limit=50)
    
    all_data = reddit_data# + twitter_data
    
    save_json(all_data, source="social")
    save_mongo(all_data)
    print(f'Total articulos reddit: {len(reddit_data)}')
    #print(f'Total articulos twitter: {len(twitter_data)}')

if __name__ == "__main__":
    main()
