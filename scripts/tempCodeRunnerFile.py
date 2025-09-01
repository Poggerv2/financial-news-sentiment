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