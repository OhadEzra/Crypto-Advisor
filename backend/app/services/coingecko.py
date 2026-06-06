import httpx

ASSET_TO_ID = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Polygon": "matic-network",
    "BNB": "binancecoin",
    "Avalanche": "avalanche-2",
    "Chainlink": "chainlink",
    "XRP": "ripple",
}

FALLBACK_PRICES = [
    {"id": "bitcoin", "name": "Bitcoin", "price": 67000, "change24h": 1.4},
    {"id": "ethereum", "name": "Ethereum", "price": 3500, "change24h": -0.7},
    {"id": "solana", "name": "Solana", "price": 145, "change24h": 3.2},
    {"id": "dogecoin", "name": "Dogecoin", "price": 0.15, "change24h": 5.8},
    {"id": "cardano", "name": "Cardano", "price": 0.46, "change24h": -1.1},
    {"id": "matic-network", "name": "Polygon", "price": 0.72, "change24h": 2.4},
    {"id": "binancecoin", "name": "BNB", "price": 610, "change24h": 0.9},
    {"id": "avalanche-2", "name": "Avalanche", "price": 32, "change24h": -2.3},
]


def _asset_name(coin_id: str):
    return next(
        (name for name, mapped_id in ASSET_TO_ID.items() if mapped_id == coin_id),
        coin_id.replace("-", " ").title(),
    )


async def get_prices(assets: list[str]):
    requested_assets = assets or ["Bitcoin", "Ethereum", "Solana", "Dogecoin", "Cardano"]

    coin_ids = []
    for asset in requested_assets:
        coin_id = ASSET_TO_ID.get(asset, asset.strip().lower().replace(" ", "-"))
        if coin_id not in coin_ids:
            coin_ids.append(coin_id)

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": ",".join(coin_ids),
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                },
            )
            response.raise_for_status()
            data = response.json()

        prices = []

        for coin_id in coin_ids:
            coin_data = data.get(coin_id)

            if not coin_data:
                continue

            price = coin_data.get("usd")
            change = coin_data.get("usd_24h_change")

            if price is None or change is None:
                continue

            prices.append({
                "id": coin_id,
                "name": _asset_name(coin_id),
                "price": price,
                "change24h": change,
            })

        return prices if len(prices) >= 4 else FALLBACK_PRICES

    except Exception:
        return FALLBACK_PRICES