import hashlib
from datetime import datetime


def generate_id(text: str) -> str:
    """Hash id unico para evitar duplicados como en el sample de Infoabae"""
    return hashlib.md5(text.encode()).hexdigest()


def parse_newsapi(article: dict) -> dict:
    """Normaliza un articulo de NewsAPI al esquema definido"""
    return {
        "id": generate_id(article["title"]),
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "source": article["source"]["name"],
        "published_at": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
        "collected_at": datetime.now()
    }


def parse_cryptocompare(article: dict) -> dict:
    """Normaliza un articulo de CryptoCompare al esquema definido"""
    return {
        "id": generate_id(article["title"]),
        "title": article["title"],
        "description": article["body"],
        "url": article["url"],
        "source": article["source_info"]["name"],
        "published_at": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
        "collected_at": datetime.now()
    }
