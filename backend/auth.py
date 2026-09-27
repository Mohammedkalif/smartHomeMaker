"""Small, dependency-free password and signed-session helpers."""
import base64
import hashlib
import hmac
import os
import secrets
import time
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User

security = HTTPBearer(auto_error=False)
SESSION_TTL_SECONDS = 60 * 60 * 24 * 7


def _secret() -> bytes:
    value = os.getenv("SESSION_SECRET", "").strip()
    if not value:
        # Local development remains usable; production must explicitly set this.
        value = "local-development-secret-change-me"
    return value.encode()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"{base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, stored: Optional[str]) -> bool:
    if not stored or "$" not in stored:
        return False
    try:
        salt_text, digest_text = stored.split("$", 1)
        salt = base64.urlsafe_b64decode(salt_text.encode())
        expected = base64.urlsafe_b64decode(digest_text.encode())
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return hmac.compare_digest(actual, expected)


def create_token(user_id: int) -> str:
    payload = f"{user_id}.{int(time.time()) + SESSION_TTL_SECONDS}"
    signature = hmac.new(_secret(), payload.encode(), hashlib.sha256).digest()
    return f"{payload}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"


def current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in to continue.")
    try:
        user_id, expiry, signature = credentials.credentials.split(".")
        payload = f"{user_id}.{expiry}"
        expected = base64.urlsafe_b64encode(hmac.new(_secret(), payload.encode(), hashlib.sha256).digest()).decode().rstrip("=")
        valid = hmac.compare_digest(signature, expected) and int(expiry) >= int(time.time())
    except (TypeError, ValueError):
        valid = False
    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Please sign in again.")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is no longer available.")
    return user
