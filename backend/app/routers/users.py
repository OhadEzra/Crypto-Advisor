import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Preference, User
from ..schemas import PreferenceRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    prefs = current_user.preference
    preferences = None
    if prefs:
        preferences = {
            "assets": json.loads(prefs.assets),
            "investor_type": prefs.investor_type,
            "content_types": json.loads(prefs.content_types),
        }
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        is_onboarded=current_user.is_onboarded,
        preferences=preferences,
    )


@router.post("/preferences")
def save_preferences(
    payload: PreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assets = json.dumps(payload.assets)
    content_types = json.dumps(payload.content_types)

    existing = db.query(Preference).filter(Preference.user_id == current_user.id).first()
    if existing:
        existing.assets = assets
        existing.investor_type = payload.investor_type
        existing.content_types = content_types
    else:
        db.add(
            Preference(
                user_id=current_user.id,
                assets=assets,
                investor_type=payload.investor_type,
                content_types=content_types,
            )
        )

    current_user.is_onboarded = True
    db.commit()
    return {"status": "ok"}
