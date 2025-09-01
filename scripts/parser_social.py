from datetime import datetime
import hashlib

def generate_id(text) -> str:
    return hashlib.md5(str(text).encode()).hexdigest()


def parse_reddit_post(post, allowed_flairs=None) -> dict:
    if allowed_flairs and (post.link_flair_text or "").lower() not in [f.lower() for f in allowed_flairs]:
        return None

    content = post.selftext if post.selftext else post.url
    return {
        "id": generate_id(post.title),
        "title": post.title,
        "description": None,
        "content": content,
        "url": post.url,
        "source": f"Reddit/{post.subreddit.display_name}",
        "published_at": datetime.fromtimestamp(post.created_utc),
        "collected_at": datetime.now(),
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