import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json
import time
from parser_scraping import parse_cronista, parse_coindesk
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

def collect_coindesk(max_articles=50, page_size=16):
    session = requests.Session()
    base_url = "https://www.coindesk.com/api/v1/articles/timeline"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.coindesk.com/latest-crypto-news",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.coindesk.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    }

    articles = []
    last_id = None
    last_display_date = None

    while len(articles) < max_articles:
        params = {"size": page_size, "lang": "en"}
        if last_id and last_display_date:
            params["lastId"] = last_id
            params["lastDisplayDate"] = last_display_date

        response = session.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Coindesk request failed: {response.status_code}")
            break

        data = response.json()
        new_articles = data.get("articles", [])
        if not new_articles:
            break

        for a in new_articles:
            parsed = parse_coindesk(a)
            articles.append(parsed)
            time.sleep(0.3)

        last_article = new_articles[-1]
        last_id = last_article["_id"]
        last_display_date = last_article["articleDates"]["displayDate"]

    return articles[:max_articles]


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

# --- Main ---
def main():
    print("Recolectando Cronista...")
    raw_cronista = fetch_cronista()
    parsed_cronista = [parse_cronista(a) for a in raw_cronista]
    save_json(parsed_cronista, "cronista")
    save_mongo(parsed_cronista)

    print("Recolectando Coindesk...")
    raw_coindesk = collect_coindesk(max_articles=100)
    save_json(raw_coindesk, "coindesk")
    save_mongo(raw_coindesk)

    print(f"Total artículos Cronista: {len(parsed_cronista)}, Coindesk: {len(raw_coindesk)}")

if __name__ == "__main__":
    main()

