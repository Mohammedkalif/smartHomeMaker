from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth import current_user
from models import Reminder, User
from schemas import ReminderCreate, ReminderUpdate
from tools.cooking_tools import create_cooking_reminder

router = APIRouter()


def _to_dict(reminder: Reminder):
    return {
        "id": reminder.id,
        "user_id": reminder.user_id,
        "food_name": reminder.food_name,
        "reminder_message": reminder.reminder_message,
        "remind_at": reminder.remind_at.isoformat() + "Z",
        "has_timing": reminder.has_timing,
        "completed": reminder.completed,
        "created_at": reminder.created_at.isoformat() + "Z" if reminder.created_at else None,
        "due": reminder.has_timing and (not reminder.completed) and reminder.remind_at <= datetime.utcnow(),
        "near": reminder.has_timing and (not reminder.completed) and datetime.utcnow() < reminder.remind_at <= datetime.utcnow() + timedelta(minutes=5),
    }


@router.get("/reminders")
def list_reminders(user: User = Depends(current_user), db: Session = Depends(get_db)):
    reminders = (
        db.query(Reminder)
        .filter(Reminder.user_id == user.id)
        .order_by(Reminder.remind_at.desc())
        .all()
    )
    items = [_to_dict(item) for item in reminders]
    return {
        "reminders": items,
        "active": [item for item in items if not item["completed"]],
        "due": [item for item in items if item["due"]],
        "near": [item for item in items if item["near"]],
        "completed": [item for item in items if item["completed"]],
    }


@router.post("/reminders")
def create_reminder(payload: ReminderCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return create_cooking_reminder(
        db,
        food_name=payload.food_name,
        duration_minutes=payload.duration_minutes,
        reminder_message=payload.reminder_message,
        has_timing=payload.has_timing,
        user_id=user.id,
    )


@router.patch("/reminders/{reminder_id}")
def update_reminder(reminder_id: int, payload: ReminderUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    reminder.completed = payload.completed
    db.commit()
    return _to_dict(reminder)
