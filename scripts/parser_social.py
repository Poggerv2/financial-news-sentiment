import praw
from datetime import datetime
import hashlib
import tweepy

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def parse_reddit_post(post) -> dict:
    return {
        "id": generate_id(post.title),
        "title": post.title,
        "description": None,
        "content": post.selftext,
        "url": post.url,
        "source": f"Reddit/{post.subreddit.display_name}",
        "published_at": datetime.fromtimestamp(post.created_utc),
        "collected_at": datetime.now(),
        "extra": {
            "author": post.author.name if post.author else None,
            "score": post.score,
            "num_comments": post.num_comments
        }
    }

def parse_tweet(tweet) -> dict:
    return {
        "id": generate_id(tweet.id_str),
        "title": tweet.text[:100],
        "description": None,
        "content": tweet.text,
        "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}",
        "source": f"Twitter/{tweet.user.screen_name}",
        "published_at": tweet.created_at,
        "collected_at": datetime.now(),
        "extra": {
            "retweets": tweet.retweet_count,
            "likes": tweet.favorite_count
        }
    }