from models import User


def get_user_profile(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User profile not found."}
    return {
        "name": user.name,
        "state": user.state,
        "city": user.city,
        "language": user.language,
    }
