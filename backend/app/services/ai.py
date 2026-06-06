import os
import httpx


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def _safe_number(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _analyze_market(prices):
    valid_prices = [
        p for p in prices
        if p.get("price") is not None and p.get("change24h") is not None
    ]

    if not valid_prices:
        return {
            "summary": "Market data is limited right now.",
            "best": None,
            "worst": None,
            "positive_count": 0,
            "negative_count": 0,
            "average_change": 0,
        }

    best = max(valid_prices, key=lambda p: _safe_number(p.get("change24h")))
    worst = min(valid_prices, key=lambda p: _safe_number(p.get("change24h")))

    positive_count = len([p for p in valid_prices if _safe_number(p.get("change24h")) >= 0])
    negative_count = len(valid_prices) - positive_count

    average_change = sum(_safe_number(p.get("change24h")) for p in valid_prices) / len(valid_prices)

    if positive_count > negative_count:
        mood = "mostly positive"
    elif negative_count > positive_count:
        mood = "mostly negative"
    else:
        mood = "mixed"

    return {
        "summary": (
            f"The tracked market is {mood}: {positive_count} assets are up, "
            f"{negative_count} are down, with an average 24h change of {average_change:.2f}%."
        ),
        "best": best,
        "worst": worst,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "average_change": round(average_change, 2),
    }


def _fallback_insight(assets, investor_type, content_types, prices, feedback=None):
    assets_text = ", ".join(assets)
    content_text = ", ".join(content_types)

    market = _analyze_market(prices)

    liked = ", ".join(feedback.get("likedSections", [])) if feedback and feedback.get("likedSections") else "no strong likes yet"
    disliked = ", ".join(feedback.get("dislikedSections", [])) if feedback and feedback.get("dislikedSections") else "no clear dislikes yet"

    best = market.get("best")
    worst = market.get("worst")

    best_text = (
        f"{best['name']} is showing the strongest 24h momentum at {best['change24h']:.2f}%."
        if best else
        "No clear strongest asset was detected."
    )

    worst_text = (
        f"{worst['name']} is currently the weakest tracked asset at {worst['change24h']:.2f}%."
        if worst else
        "No clear weakest asset was detected."
    )

    return (
    f"Market read: {market['summary']}\n\n"
    f"Top momentum: {best_text}\n"
    f"Risk signal: {worst_text}\n\n"
    f"AI take: For a {investor_type} profile watching {assets_text}, avoid reacting to one price candle. "
    f"Compare market movement with {content_text} before deciding whether the move is signal or noise.\n\n"
    f"Personalization: Your feedback suggests you like {liked}, while {disliked} seems less relevant so far.\n\n"
    f"Educational content only, not financial advice."
)

async def generate_insight(assets, investor_type, content_types, prices, feedback=None):
    market = _analyze_market(prices)

    if not OPENROUTER_API_KEY:
        return _fallback_insight(assets, investor_type, content_types, prices, feedback)

    prompt = f"""
You are an AI crypto advisor inside a personalized investor dashboard.

User profile:
- Investor type: {investor_type}
- Assets: {assets}
- Preferred content: {content_types}

Computed market analysis:
- Market summary: {market["summary"]}
- Best performer: {market["best"]}
- Weakest performer: {market["worst"]}
- Positive assets: {market["positive_count"]}
- Negative assets: {market["negative_count"]}
- Average 24h change: {market["average_change"]}%

Raw prices:
{prices}

User feedback summary:
{feedback}

Write one strong daily insight for the dashboard.

Rules:
- Sound like a smart product, not a generic chatbot.
- Mention the strongest asset and weakest asset if available.
- Explain what the movement may imply.
- Adapt the advice to the investor type.
- Mention how the user should use news/feedback/watchlist.
- Keep it practical and concise.
- No hype.
- No promises.
- No direct buy/sell instruction.
- End with: "Educational content only, not financial advice."
"""

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    "temperature": 0.4,
                    "max_tokens": 180,
                },
            )

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return _fallback_insight(assets, investor_type, content_types, prices, feedback)