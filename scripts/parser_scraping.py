import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def parse_article(article_html: str) -> dict:
    soup = BeautifulSoup(article_html, "html.parser")
    
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    description = soup.find("meta", {"name": "description"})
    description = description["content"] if description else None
    content_div = soup.find("div", {"class": "article-content"})
    content = content_div.get_text(separator="\n", strip=True) if content_div else None
    published_at_tag = soup.find("time")
    published_at = datetime.strptime(published_at_tag["datetime"], "%Y-%m-%dT%H:%M:%S") if published_at_tag else None
    
    return {
        "id": generate_id(title or ""),
        "title": title,
        "description": description,
        "content": content,
        "url": "",
        "source": "Infobae",
        "published_at": published_at,
        "collected_at": datetime.now(),
        "extra": {}
    }
