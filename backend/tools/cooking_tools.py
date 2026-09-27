from datetime import datetime, timedelta

from models import Reminder


def create_cooking_reminder(db, food_name: str, duration_minutes: int, reminder_message: str, has_timing: bool = True, user_id: int | None = None):
    if user_id is None:
        return {"success": False, "error": "A signed-in user is required to create a reminder."}
    minutes = max(1, min(int(duration_minutes), 24 * 60))
    reminder = Reminder(
        user_id=user_id,
        food_name=food_name.strip(),
        reminder_message=reminder_message.strip(),
        remind_at=datetime.utcnow() + timedelta(minutes=minutes),
        has_timing=has_timing,
        completed=False,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return {
        "success": True,
        "id": reminder.id,
        "food_name": reminder.food_name,
        "reminder_message": reminder.reminder_message,
        "duration_minutes": minutes,
        "has_timing": has_timing,
        "remind_at": reminder.remind_at.isoformat() + "Z",
    }
