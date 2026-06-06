from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Vote, Preference, WatchlistItem

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    votes = db.query(Vote).all()
    preferences_count = db.query(Preference).count()
    watchlist_count = db.query(WatchlistItem).count()

    likes = len([v for v in votes if v.vote == 1])
    dislikes = len([v for v in votes if v.vote == -1])

    section_counter = Counter([v.section for v in votes])
    top_sections = [
        {"section": section, "votes": count}
        for section, count in section_counter.most_common(5)
    ]

    return {
        "users": users_count,
        "onboardedUsers": preferences_count,
        "votes": len(votes),
        "likes": likes,
        "dislikes": dislikes,
        "watchlistItems": watchlist_count,
        "topVotedSections": top_sections,
        "trainingSuggestion": {
            "currentStatus": "Feedback is stored in the database.",
            "futureImprovement": "Use votes to rank content, enrich AI prompts, and train a recommendation model.",
            "flow": [
                "User consumes dashboard content",
                "User votes thumbs up/down",
                "Vote is stored with section and item ID",
                "User preference profile is updated",
                "Future AI prompts include feedback summary",
                "Recommendations become more personalized over time",
            ],
        },
    }


@router.get("/votes")
def votes(db: Session = Depends(get_db)):
    rows = db.query(Vote).order_by(Vote.created_at.desc()).limit(100).all()

    return [
        {
            "id": row.id,
            "userId": row.user_id,
            "section": row.section,
            "itemId": row.item_id,
            "vote": row.vote,
            "createdAt": row.created_at,
        }
        for row in rows
    ]