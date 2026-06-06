import httpx


def _matches_asset(item, assets):
    text = f"{item.get('title', '')} {item.get('body', '')}".lower()

    keywords = []
    for asset in assets:
        clean = asset.lower()
        keywords.append(clean)

        if clean == "bitcoin":
            keywords.append("btc")
        elif clean == "ethereum":
            keywords.append("eth")
        elif clean == "solana":
            keywords.append("sol")
        elif clean == "dogecoin":
            keywords.append("doge")
        elif clean == "cardano":
            keywords.append("ada")
        elif clean == "polygon":
            keywords.append("matic")

    return any(keyword in text for keyword in keywords)


def _fallback_news(assets):
    main_asset = assets[0] if assets else "Bitcoin"

    return [
        {
            "id": "fallback-news-1",
            "title": f"{main_asset} market momentum stays in focus",
            "source": "Market Brief",
            "url": "#",
            "summary": f"{main_asset} remains a key asset for investors watching short-term volatility, sentiment shifts, and broader crypto market direction.",
        },
        {
            "id": "fallback-news-2",
            "title": "Crypto investors monitor volatility across major assets",
            "source": "Market Brief",
            "url": "#",
            "summary": "Major crypto assets continue to react to liquidity, market sentiment, and macro expectations, making context important before reacting to price movement.",
        },
        {
            "id": "fallback-news-3",
            "title": "Personalized dashboards help investors filter market noise",
            "source": "Market Brief",
            "url": "#",
            "summary": "Combining news, price movement, watchlists, and user feedback can create a clearer daily view for crypto investors.",
        },
    ]

async def get_market_news(assets: list[str], content_types: list[str]):
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    params = {
        "lang": "EN",
        "sortOrder": "latest",
    }

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            items = response.json().get("Data", [])[:20]

        matched = [item for item in items if _matches_asset(item, assets)]

        selected = matched[:6] if len(matched) >= 3 else items[:6]

        return [
            {
                "id": str(item.get("id")),
                "title": item.get("title") or "Untitled crypto update",
                "source": item.get("source_info", {}).get("name", "CryptoCompare"),
                "url": item.get("url") or "#",
                "summary": (item.get("body") or "No summary available.")[:220],
            }
            for item in selected
        ]

    except Exception:
        return _fallback_news(assets)