import hashlib
from datetime import datetime

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def parse_cronista(article: dict) -> dict:
    return {
        "id": generate_id(article.get("url", "")),
        "title": article.get("title") or "Untitled",
        "description": article.get("description") or "",
        "content": article.get("content") or None,
        "url": article.get("url"),
        "source": article.get("source") or "El Cronista",
        "published_at": article.get("published_at"),
        "collected_at": datetime.utcnow(),
        "extra": article.get("extra") or {},
    }
