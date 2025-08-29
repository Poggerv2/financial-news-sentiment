# config
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from parser import parse_newsapi, parse_cryptocompare

data_path = Path(__file__).resolve().parents[1] / "data" / "raw"
data_path.mkdir(parents=True, exist_ok=True)

load_dotenv()
newsapi_key = os.getenv("NEWS_API_KEY")

# requests
def fetch_newsapi(query='bitcoin', language='en', page_size=100):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "pageSize": page_size,
        "apiKey": newsapi_key,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()['articles']


def fetch_cryptocompare(query='BTC', limit=200):
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    params = {'lang': 'EN', 'limit': limit}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()['Data']


def save_json(data, source):
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = data_path / f"{source}_{today}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=2)
    print(f"Saved {len(data)} articles in {file_path}")

# main
def main():
    all_articles = []

    #newsapi
    try:
        raw_newsapi = fetch_newsapi()
        parsed_newsapi = [parse_newsapi(a) for a in raw_newsapi]
        save_json(parsed_newsapi, "newsapi")
        all_articles.extend(parsed_newsapi)
    except Exception as e:
        print(f"Error NewsAPI: {e}")

    #cryptocompare
    try:
        raw_crypto = fetch_cryptocompare()
        parsed_crypto = [parse_cryptocompare(a) for a in raw_crypto]
        save_json(parsed_crypto, "cryptocompare")
        all_articles.extend(parsed_crypto)
    except Exception as e:
        print(f"Error CryptoCompare: {e}")

    print(f"Total articles collected: {len(all_articles)}")

if __name__ == "__main__":
    main()