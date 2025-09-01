import hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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

def get_article_content(url):
    # 1. Hacer la petición
    response = requests.get(url)
    if response.status_code != 200:
        return None

    # 2. Parsear el HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 3. Seleccionar el div principal del artículo
    content_div = soup.find('div', class_='document-body font-body-lg')
    if not content_div:
        return None

    # 4. Extraer párrafos y listas
    article_text = []

    # Párrafos
    for p in content_div.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            article_text.append(text)

    # Listas
    for li in content_div.find_all('li'):
        text = li.get_text(strip=True)
        if text:
            article_text.append(text)

    # 5. Devolver todo como un solo string
    return "\n".join(article_text)


def parse_coindesk(article: dict) -> dict:
    url = f"https://www.coindesk.com{article.get('pathname')}" if article.get("pathname") else None
    
    return {
        "id": generate_id(article.get("title", "")),
        "title": article.get("title") or "Untitled",
        "description": article.get("description") or "",
        "content": get_article_content(url) if url else None,
        "url": url,
        "source": "Coindesk",
        "published_at": (
            datetime.fromisoformat(article["articleDates"]["displayDate"].replace("Z", "+00:00"))
            if article.get("articleDates", {}).get("displayDate") else None
        ),
        "collected_at": datetime.now(),
        "extra": {
            "lang": "en",
            "tags": [tag.get("title") for tag in (article.get("tagDetails") or [])],
            "image": (article.get("__featuredImages") or [{}])[0].get("source", {}).get("src", ""),
            "author": (article.get("authorDetails") or [{}])[0].get("byline")
        },
    }