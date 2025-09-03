# config
import os
import json
import time
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path
from parser_APIs import parse_newsapi, parse_cryptocompare
from db import get_mongo_collection

# paths
data_path = Path(__file__).resolve().parents[1] / "data" / "raw"
data_path.mkdir(parents=True, exist_ok=True)

load_dotenv()
newsapi_key = os.getenv("NEWS_API_KEY")

articles = get_mongo_collection()

# requests
def fetch_newsapi(query='bitcoin', language='en', page_size=100):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "pageSize": page_size,
        "apiKey": newsapi_key,
        "from": "2025-08-03",
        "to": "2025-09-02"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()['articles']


def fetch_cryptocompare_day(query="BTC", source="coindesk", date=None, per_day=2):
    if date is None:
        date = datetime.utcnow()
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
    to_ts = int(end_of_day.timestamp())

    url = "https://data-api.coindesk.com/news/v1/article/list"
    params = {
        "search_string": query,
        "lang": "EN",
        "limit": per_day,
        "to_ts": to_ts,
        "source_key": source,
    }
    headers = {"Content-type": "application/json; charset=UTF-8"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()["Data"]


def fetch_historical_crypto(query="BTC", source="coindesk", days_back=60, per_day=2, max_total=100):
    all_articles = []
    seen_ids = set()
    today = datetime.utcnow()

    for i in range(days_back):
        day = today - timedelta(days=i)
        try:
            raw = fetch_cryptocompare_day(query=query, source=source, date=day, per_day=per_day)
            parsed = [parse_cryptocompare(a) for a in raw]

            unique = [p for p in parsed if p["id"] not in seen_ids]
            for p in unique:
                seen_ids.add(p["id"])
            
            all_articles.extend(unique)
            print(f"{day.date()} → {len(unique)} nuevos artículos (total {len(all_articles)})")

        except Exception as e:
            print(f"Error {day.date()}: {e}")

        if len(all_articles) >= max_total:
            break
        time.sleep(1)

    return all_articles

# saves 
def save_json(data, source):
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = data_path / f"{source}_{today}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=2)
    print(f"Saved {len(data)} articles in {file_path}")

def save_mongo(data):
    if not data:
        return
    articles.insert_many(data)
    print(f"Inserted {len(data)} documents into MongoDB")

# main
def main():
    all_articles = []

    # newsapi
    try:
        raw_newsapi = fetch_newsapi()
        parsed_newsapi = [parse_newsapi(a) for a in raw_newsapi]
        save_json(parsed_newsapi, "newsapi")
        save_mongo(parsed_newsapi)
        all_articles.extend(parsed_newsapi)
    except Exception as e:
        print(f"Error NewsAPI: {e}")

    # cryptocompare
    try:
        parsed_crypto = fetch_historical_crypto(
            query="BTC", source="cryptocompare", days_back=190, per_day=5, max_total=950
        )
        save_json(parsed_crypto, "cryptocompare_historical")
        save_mongo(parsed_crypto)
        all_articles.extend(parsed_crypto)
    except Exception as e:
        print(f"Error CryptoCompare: {e}")

    print(f"Total articles collected: {len(all_articles)}")

if __name__ == "__main__":
    main()