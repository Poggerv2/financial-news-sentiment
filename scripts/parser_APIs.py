import hashlib
from datetime import datetime


def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def parse_cryptocompare(article: dict) -> dict:
    title = article.get("TITLE") or "Untitled"
    content = article.get("BODY") or ""
    keywords = article.get("KEYWORDS", "").lower()

    text_blob = " ".join([title.lower(), content.lower(), keywords])

    relevance = (
        text_blob.count("bitcoin") * 2 +
        text_blob.count("BTC") * 1
    )

    return {
        "id": generate_id(title),
        "title": title,
        "description": article.get("SUBTITLE") or "",
        "content": content,
        "url": article.get("URL"),
        "source": article.get("SOURCE_DATA", {}).get("NAME"),
        "published_at": (
            datetime.fromtimestamp(article["PUBLISHED_ON"])
            if article.get("PUBLISHED_ON") else None
        ),
        "collected_at": datetime.now(),
        "extra": {
            "lang": article.get("LANG") or "unknown",
            "keywords": article.get("KEYWORDS", "").split(",") if article.get("KEYWORDS") else [],
            "image": article.get("IMAGE_URL") or "",
            "source_id": article.get("SOURCE_ID"),
            "score": article.get("SCORE"),
            "bitcoin_relevance": relevance
        },
    }
