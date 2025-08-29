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
        "id": generate_id(article.get("TITLE", "")),
        "title": article.get("TITLE"),
        "description": article.get("SUBTITLE"),
        "content": article.get("BODY"),
        "url": article.get("URL"),
        "source": article.get("SOURCE_INFO", {}).get("NAME"),
        "published_at": datetime.fromtimestamp(article["PUBLISHED_ON"]) if article.get("PUBLISHED_ON") is not None else None,
        "collected_at": datetime.now(),
        "extra": {
            "lang": article.get("LANG"),
            "keywords": article.get("KEYWORDS"),
            "image": article.get("IMAGE_URL"),
            "source_id": article.get("SOURCE_INFO", {}).get("ID"),
        },
    }
