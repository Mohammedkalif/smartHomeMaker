from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import create_token, current_user, hash_password, verify_password
from database import get_db
from models import User
from schemas import AuthCredentials

router = APIRouter(prefix="/auth", tags=["authentication"])


def _response(user: User):
    return {"token": create_token(user.id), "user": {"id": user.id, "name": user.name}}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: AuthCredentials, db: Session = Depends(get_db)):
    name = payload.name.strip()
    existing = db.query(User).filter(User.name.ilike(name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="That name already has an account. Sign in instead.")
    user = User(name=name, password_hash=hash_password(payload.password), state="Tamil Nadu", city="Chennai", language="English")
    db.add(user)
    db.commit()
    db.refresh(user)
    return _response(user)


@router.post("/login")
def login(payload: AuthCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name.ilike(payload.name.strip())).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect name or password.")
    return _response(user)


@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "name": user.name}
