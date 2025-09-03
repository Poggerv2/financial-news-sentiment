import hashlib
from datetime import datetime


def generate_id(text: str) -> str:
    """Hash id unico para evitar duplicados como en el sample de Infoabae"""
    return hashlib.md5(text.encode()).hexdigest()


def parse_newsapi(article: dict) -> dict:
    """Normaliza un articulo de NewsAPI al esquema definido"""
    return {
        "id": generate_id(article.get("title", "")),
        "title": article.get("title"),
        "description": article.get("description"),
        "content": article.get("content") or None,
        "url": article.get("url"),
        "source": article.get("source", {}).get("name"),
        "published_at": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
        "collected_at": datetime.now(),
        "extra": {
            "author": article.get("author"),
        },
    }


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
