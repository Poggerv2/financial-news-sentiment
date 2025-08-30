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
    """Normaliza un articulo de CryptoCompare al esquema definido"""
    return {
        "id": generate_id(article.get("title", "")),
        "title": article.get("title") or "Untitled",
        "description": article.get("subtitle") or "",
        "content": article.get("body") or "",
        "url": article.get("url"),
        "source": article.get("source_info", {}).get("name"),
        "published_at": (
            datetime.fromtimestamp(article["published_on"])
            if article.get("published_on") is not None else None
        ),
        "collected_at": datetime.now(),
        "extra": {
            "lang": article.get("lang") or "unknown",
            "keywords": article.get("keywords", []),
            "image": article.get("image_url") or "",
            "source_id": article.get("source_id"),
        },
    }
