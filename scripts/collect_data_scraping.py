import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json
from parser_scraping import parse_cronista
from db import get_mongo_collection

BASE_URL = "https://www.cronista.com"
SECTION_URL = "https://www.cronista.com/criptomonedas/"
headers = {"User-Agent": "Mozilla/5.0"}

data_path = Path(__file__).resolve().parents[1] / "data" / "raw"
data_path.mkdir(parents=True, exist_ok=True)

articles_col = get_mongo_collection()

def fetch_cronista():
    resp = requests.get(SECTION_URL, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    articles_html = soup.find_all("article", class_=lambda x: x and "item" in x)
    articles = []

    for art in articles_html:
        a_tag = art.find("a", class_="link")
        if not a_tag:
            continue

        title_tag = a_tag.find("h2", class_="title")
        kicker_tag = a_tag.find("span", class_="kicker")
        img_tag = art.find("div", class_="image").find("img") if art.find("div", class_="image") else None

        link = a_tag.get("href")
        if link.startswith("/"):
            link = BASE_URL + link

        img_url = img_tag["src"] if img_tag else None

        try:
            art_resp = requests.get(link, headers=headers)
            art_resp.raise_for_status()
            art_soup = BeautifulSoup(art_resp.text, "html.parser")

            body = art_soup.find("div", class_="block-content")
            content = "\n".join([p.get_text(strip=True) for p in body.find_all("p")]) if body else None

            time_tag = art_soup.find("time") or art_soup.find("span", class_="date")
            published_at = time_tag.get_text(strip=True) if time_tag else None

        except Exception as e:
            print(f"Error extrayendo {link}: {e}")
            content = None
            published_at = None

        article_dict = {
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "description": kicker_tag.get_text(strip=True) if kicker_tag else None,
            "content": content,
            "url": link,
            "source": "El Cronista",
            "published_at": published_at,
            "extra": {"image_url": img_url},
        }

        articles.append(article_dict)

    return articles

def save_json(data, source="cronista"):
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = data_path / f"{source}_{today}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=2)
    print(f"Guardados {len(data)} artículos en {file_path}")

def save_mongo(data):
    if not data:
        return
    articles_col.insert_many(data)
    print(f"Insertados {len(data)} documentos en MongoDB")

def main():
    raw_articles = fetch_cronista()
    parsed_articles = [parse_cronista(a) for a in raw_articles]
    save_json(parsed_articles)
    save_mongo(parsed_articles)
    print(f"Total artículos recolectados: {len(parsed_articles)}")

if __name__ == "__main__":
    main()