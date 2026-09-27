from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Food, Recipe, State

router = APIRouter()


@router.get("/states")
def list_states(db: Session = Depends(get_db)):
    states = db.query(State).order_by(State.name).all()
    return {"states": [state.name for state in states]}


@router.get("/foods")
def list_foods(
    state: Optional[str] = Query(default=None),
    meal_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Food)
    if state:
        query = query.filter(Food.state.ilike(f"%{state}%"))
    if meal_type:
        query = query.filter(Food.meal_type.ilike(meal_type))
    foods = query.order_by(Food.dish_name).all()
    return {
        "foods": [
            {
                "id": food.id,
                "state": food.state,
                "dish_name": food.dish_name,
                "meal_type": food.meal_type,
                "description": food.description,
            }
            for food in foods
        ]
    }


@router.get("/foods/{food_id}")
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Dish not found.")
    recipe = db.query(Recipe).filter(Recipe.food_id == food.id).first()
    return {
        "id": food.id,
        "state": food.state,
        "dish_name": food.dish_name,
        "meal_type": food.meal_type,
        "description": food.description,
        "recipe": None
        if not recipe
        else {
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
        },
    }
