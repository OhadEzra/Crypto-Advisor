import json
from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import User, Vote, WatchlistItem
from ..schemas import VoteRequest
from ..services.ai import generate_insight
from ..services.coingecko import get_prices
from ..services.memes import get_random_meme
from ..services.news import get_market_news

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _preferences(user: User):
    if not user.preference:
        return ["Bitcoin", "Ethereum"], "HODLer", ["Market News", "Charts", "Fun"]

    return (
        json.loads(user.preference.assets),
        user.preference.investor_type,
        json.loads(user.preference.content_types),
    )


def _feedback_summary(votes):
    likes = [v for v in votes if v.vote == 1]
    dislikes = [v for v in votes if v.vote == -1]

    liked_sections = Counter([v.section for v in likes]).most_common(3)
    disliked_sections = Counter([v.section for v in dislikes]).most_common(3)

    return {
        "totalVotes": len(votes),
        "likes": len(likes),
        "dislikes": len(dislikes),
        "likedSections": [section for section, _ in liked_sections],
        "dislikedSections": [section for section, _ in disliked_sections],
    }


def _market_sentiment(prices):
    valid_prices = [
        p for p in prices
        if isinstance(p.get("change24h"), (int, float))
    ]

    if not valid_prices:
        return {
            "label": "Neutral",
            "score": 50,
            "summary": "Not enough price data to calculate market sentiment.",
        }

    positive = len([p for p in valid_prices if p.get("change24h", 0) >= 0])
    score = round((positive / len(valid_prices)) * 100)

    if score >= 70:
        label = "Bullish"
    elif score <= 35:
        label = "Bearish"
    else:
        label = "Neutral"

    return {
        "label": label,
        "score": score,
        "summary": f"{positive} out of {len(valid_prices)} tracked assets are positive in the last 24h.",
    }

def _risk_profile(investor_type: str, assets):
    risky_assets = {"Dogecoin", "Solana", "Polygon", "Cardano"}
    stable_assets = {"Bitcoin", "Ethereum"}

    risky_count = len([a for a in assets if a in risky_assets])
    stable_count = len([a for a in assets if a in stable_assets])

    if investor_type.lower() in ["trader", "aggressive"] or risky_count > stable_count:
        level = "High"
        summary = "Your portfolio leans toward higher volatility assets and short-term market movement."
    elif stable_count >= risky_count:
        level = "Medium"
        summary = "Your portfolio has a relatively balanced crypto risk profile led by major assets."
    else:
        level = "Medium"
        summary = "Your current watchlist contains a mix of major assets and higher-volatility coins."

    return {
        "level": level,
        "summary": summary,
        "suggestion": "Use watchlist changes and feedback votes to continuously personalize the dashboard.",
    }

def _portfolio_score(prices, investor_type):
    valid_prices = [
        p for p in prices
        if isinstance(p.get("change24h"), (int, float))
    ]

    if not valid_prices:
        return {
            "score": 50,
            "strengths": [],
            "weaknesses": [],
        }

    positive = len(
        [p for p in valid_prices if p["change24h"] > 0]
    )

    score = 50 + round(
        (positive / len(valid_prices)) * 40
    )

    score = min(score, 100)

    strengths = []
    weaknesses = []

    if positive >= len(valid_prices) / 2:
        strengths.append("Positive market momentum")
    else:
        weaknesses.append("Most tracked assets are declining")

    if investor_type.lower() == "hodler":
        strengths.append("Long-term investment profile")

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }
def _build_recommendations(assets, investor_type, prices, feedback, news):
    recommendations = []

    valid_prices = [
        p for p in prices
        if isinstance(p.get("change24h"), (int, float))
    ]

    if valid_prices:
        best = max(
            valid_prices,
            key=lambda p: p.get("change24h", 0)
        )

        worst = min(
            valid_prices,
            key=lambda p: p.get("change24h", 0)
        )

        recommendations.append({
            "id": "momentum-watch",
            "title": f"Watch {best['name']} momentum",
            "asset": best["name"],
            "type": "Momentum",
            "confidence": 82,
            "reason": f"{best['name']} is currently showing the strongest 24h movement in your tracked assets.",
            "action": "Review recent price movement before making any decision.",
        })

        recommendations.append({
            "id": "risk-check",
            "title": f"Review {worst['name']} risk",
            "asset": worst["name"],
            "type": "Risk",
            "confidence": 76,
            "reason": f"{worst['name']} is the weakest performer in your watchlist over the last 24h.",
            "action": "Check whether the move is news-driven or part of a wider market trend.",
        })

    if len(news) > 0:
        recommendations.append({
            "id": "news-context",
            "title": "Use news as confirmation, not as a trigger",
            "asset": "Market",
            "type": "Education",
            "confidence": 88,
            "reason": "Your dashboard includes market news, but news should support analysis rather than replace it.",
            "action": "Compare news sentiment with price movement before reacting.",
        })

    if feedback["likes"] or feedback["dislikes"]:
        recommendations.append({
            "id": "feedback-personalization",
            "title": "Your feedback is shaping the advisor",
            "asset": "Personalization",
            "type": "AI Learning",
            "confidence": 91,
            "reason": f"You have submitted {feedback['totalVotes']} feedback votes. The system can now better understand what content you prefer.",
            "action": "Keep voting on insights, news, prices and memes to improve future recommendations.",
        })
    else:
        recommendations.append({
            "id": "start-feedback",
            "title": "Start training your AI advisor",
            "asset": "Personalization",
            "type": "AI Learning",
            "confidence": 72,
            "reason": "No feedback patterns were found yet, so the advisor is still using your onboarding preferences.",
            "action": "Like or dislike dashboard items to make future insights more personal.",
        })

    return recommendations[:4]
@router.get("")
async def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assets, investor_type, content_types = _preferences(current_user)

    watchlist_assets = [item.asset for item in current_user.watchlist]
    default_market = [
    "Bitcoin",
    "Ethereum",
    "Solana",
    "Dogecoin",
    "Cardano",
]
    final_assets = list(
    dict.fromkeys(
        watchlist_assets +
        assets +
        default_market
    ))

    prices = await get_prices(final_assets)
    news = await get_market_news(final_assets, content_types)
    feedback = _feedback_summary(current_user.votes)

    insight = await generate_insight(
        assets=final_assets,
        investor_type=investor_type,
        content_types=content_types,
        prices=prices,
        feedback=feedback,
    )

    meme = get_random_meme()

    sentiment = _market_sentiment(prices)
    risk_profile = _risk_profile(investor_type, final_assets)
    portfolio_score = _portfolio_score(
    prices,
    investor_type
)
    recommendations = _build_recommendations(
        final_assets,
        investor_type,
        prices,
        feedback,
        news if isinstance(news, list) else [],
    )

    return {
        "user": {
            "name": current_user.name,
            "investorType": investor_type,
            "assets": assets,
            "contentTypes": content_types,
        },
        "stats": {
            "watchlistCount": len(final_assets),
            "newsCount": len(news) if isinstance(news, list) else 0,
            "feedbackCount": feedback["totalVotes"],
            "likes": feedback["likes"],
            "dislikes": feedback["dislikes"],
        },
        "feedbackSummary": feedback,
        "aiAdvisor": {
            "sentiment": sentiment,
            "riskProfile": risk_profile,
            "recommendations": recommendations,
            "portfolioScore": portfolio_score,
        },
        "sections": {
            "prices": prices,
            "news": news,
            "insight": {
                "id": "daily-insight",
                "text": insight,
            },
            "meme": meme,
            "watchlist": watchlist_assets,
        },
    }


@router.post("/vote")
def vote(
    payload: VoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.vote not in [1, -1]:
        raise HTTPException(status_code=400, detail="Vote must be 1 or -1")

    saved = Vote(
        user_id=current_user.id,
        section=payload.section,
        item_id=payload.item_id,
        vote=payload.vote,
    )

    db.add(saved)
    db.commit()

    return {
        "status": "saved",
        "message": "Feedback stored for future recommendation improvements.",
    }


@router.get("/feedback-summary")
def feedback_summary(current_user: User = Depends(get_current_user)):
    return _feedback_summary(current_user.votes)


@router.get("/watchlist")
def get_watchlist(current_user: User = Depends(get_current_user)):
    return {
        "watchlist": [item.asset for item in current_user.watchlist]
    }


@router.post("/watchlist/{asset}")
def add_to_watchlist(
    asset: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    normalized_asset = asset.strip()

    if not normalized_asset:
        raise HTTPException(status_code=400, detail="Asset cannot be empty")

    exists = (
        db.query(WatchlistItem)
        .filter(
            WatchlistItem.user_id == current_user.id,
            WatchlistItem.asset.ilike(normalized_asset),
        )
        .first()
    )

    if exists:
        return {
            "status": "exists",
            "watchlist": [item.asset for item in current_user.watchlist],
        }

    item = WatchlistItem(user_id=current_user.id, asset=normalized_asset)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "status": "added",
        "asset": item.asset,
    }


@router.delete("/watchlist/{asset}")
def remove_from_watchlist(
    asset: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(WatchlistItem)
        .filter(
            WatchlistItem.user_id == current_user.id,
            WatchlistItem.asset.ilike(asset),
        )
        .first()
    )

    if not item:
        return {
            "status": "not_in_watchlist",
            "asset": asset,
        }

    db.delete(item)
    db.commit()

    return {
        "status": "removed",
        "asset": asset,
    }