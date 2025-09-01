from datetime import datetime
from newspaper import Article, Config
import hashlib
import re
import os
import time
import random
from dotenv import load_dotenv
import praw


load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
user_agent = os.getenv("user_agent")

news_config = Config()
news_config.browser_user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def generate_id(text) -> str:
    return hashlib.md5(str(text).encode()).hexdigest()

def generate_id_reddit(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def is_article(url: str) -> bool:
    if not url:
        return False
    if re.search(r"\.(jpg|jpeg|png|gif|mp4|pdf)$", url, re.IGNORECASE):
        return False
    if "reddit.com" in url:
        return False
    return True

def get_content(url: str) -> str:
    try:
        art = Article(url, config=news_config)
        art.download()
        art.parse()
        return art.text.strip()
    except Exception as e:
        return f"[ERROR: {e}]"
    
def parse_reddit(subreddit_name="CryptoCurrency", limit=100, flair="GENERAL-NEWS"):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=limit)

    for post in posts:
        if flair and (post.link_flair_text or "").upper() != flair.upper():
            continue

        url = post.url
        if not is_article(url):
            continue

        time.sleep(random.uniform(1, 2))

        content = get_content(url)

        yield {
            "id": generate_id(post.title),
            "title": post.title,
            "description": post.selftext if post.selftext else None,
            "content": content,
            "url": url,
            "source": f"Reddit/{post.subreddit.display_name}",
            "published_at": datetime.fromtimestamp(post.created_utc).isoformat(),
            "collected_at": datetime.now().isoformat(),
            "extra": {
                "author": post.author.name if post.author else None,
                "score": post.score,
                "num_comments": post.num_comments,
                "flair": post.link_flair_text
            }
        }


def parse_tweet(tweet, users_map) -> dict:
    user_info = users_map.get(tweet.author_id)
    return {
        "id": generate_id(tweet.id),
        "title": tweet.text[:100],
        "description": None,
        "content": tweet.text,
        "url": f"https://twitter.com/{user_info.username}/status/{tweet.id}" if user_info else None,
        "source": f"Twitter/{user_info.username}" if user_info else "Twitter",
        "published_at": tweet.created_at,
        "collected_at": datetime.now(),
        "extra": {
            "author": user_info.username if user_info else None,
            "retweets": tweet.public_metrics.get("retweet_count", 0),
            "likes": tweet.public_metrics.get("like_count", 0),
            "replies": tweet.public_metrics.get("reply_count", 0),
            "quotes": tweet.public_metrics.get("quote_count", 0)
        }
    }