from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import current_user
from database import get_db
from models import User
from schemas import ProfileUpdate
from seed import STATES

router = APIRouter()

LANGUAGES = ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"]


def _profile_dict(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "state": user.state,
        "city": user.city,
        "language": user.language,
        "states": STATES,
        "languages": LANGUAGES,
    }


@router.get("/profile")
def get_profile(user: User = Depends(current_user)):
    return _profile_dict(user)


@router.put("/profile")
def update_profile(payload: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if payload.name:
        user.name = payload.name.strip()
    if payload.state:
        user.state = payload.state.strip()
    if payload.city:
        user.city = payload.city.strip()
    if payload.language:
        user.language = payload.language.strip()
    user = db.merge(user)
    db.commit()
    db.refresh(user)
    return _profile_dict(user)
