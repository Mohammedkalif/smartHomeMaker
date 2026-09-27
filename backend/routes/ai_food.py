from fastapi import APIRouter, HTTPException

from schemas import AIFoodRequest
from services.food_ai_service import suggest_foods

router = APIRouter()


@router.post("/ai/food-suggestions")
def ai_food_suggestions(payload: AIFoodRequest):
    try:
        return {"dishes": suggest_foods(payload.state, payload.meal_type, payload.language)}
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(status_code=502, detail="Food ideas are unavailable right now. Please try again.")
