import requests
import praw
from newspaper import Article, Config
import time
import random
import tweepy
from datetime import datetime
from dotenv import load_dotenv
import hashlib
import json
import os
from pathlib import Path
from parser_social import parse_reddit, parse_tweet
from db import get_mongo_collection

load_dotenv()
#twitter
bearer_token = os.getenv("bearer_token")
#reddit
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
user_agent = os.getenv("user_agent")

data_path = Path(__file__).resolve().parents[1] / "data" / "raw"
data_path.mkdir(parents=True, exist_ok=True)

articles_col = get_mongo_collection()

def collect_reddit_news(subreddit="CryptoCurrency", limit=100, flair="GENERAL-NEWS"):
    results = list(parse_reddit(subreddit, limit, flair))
    print(f"\nCollected {len(results)} reddit articles")
    return results

def collect_twitter(query="bitcoin OR BTC OR crypto", limit=50):
    client = tweepy.Client(bearer_token=bearer_token)

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
    print(f"Saved {len(data)} articles in {file_path}")

def save_mongo(data):
    if not data:
        return
    articles_col.insert_many(data)
    print(f"Insertados {len(data)} documentos en MongoDB")

# --- Main ---
def main():
    reddit_data = collect_reddit_news("CryptoCurrency", limit=100)
    # twitter_data = collect_twitter(limit=50)  # comentamos hasta que se restablezca la cuota

    all_data = reddit_data  # + twitter_data cuando esté disponible
    save_json(all_data, source="social")
    save_mongo(all_data)

    print(f'Reddit: {len(reddit_data)}')
    # print(f'Twitter: {len(twitter_data)}')

if __name__ == "__main__":
    main()
