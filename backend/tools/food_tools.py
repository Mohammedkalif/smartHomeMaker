from typing import Optional

from models import Food, Recipe


def get_food_suggestions(db, state: str, meal_type: str, ingredients: Optional[str] = None):
    query = db.query(Food)
    if state:
        query = query.filter(Food.state.ilike(f"%{state.strip()}%"))
    if meal_type:
        query = query.filter(Food.meal_type.ilike(meal_type.strip()))

    foods = query.limit(6).all()
    if not foods:
        foods = db.query(Food).filter(Food.state.ilike(f"%{state.strip()}%")).limit(6).all()

    results = [
        {
            "id": food.id,
            "state": food.state,
            "dish_name": food.dish_name,
            "meal_type": food.meal_type,
            "description": food.description,
        }
        for food in foods
    ]

    if ingredients:
        results.append(
            {
                "note": (
                    "These dishes come from the local food database. "
                    f"The user mentioned ingredients: {ingredients}."
                )
            }
        )
    return {"suggestions": results}


def get_recipe(db, dish_name: str):
    recipe = (
        db.query(Recipe)
        .filter(Recipe.dish_name.ilike(f"%{dish_name.strip()}%"))
        .first()
    )
    if not recipe:
        return {"found": False, "message": f"No recipe found for {dish_name}. Try asking me to create a new recipe!"}
    return {
        "found": True,
        "dish_name": recipe.dish_name,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
    }


def generate_ai_recipe(dish_name: str, cuisine: str = ""):
    """Generate a recipe using AI when database doesn't have it."""
    return {
        "source": "ai_generated",
        "dish_name": dish_name,
        "cuisine": cuisine or "Indian",
        "note": f"AI recipe for {dish_name}. Ask me to provide detailed ingredients and cooking instructions.",
    }

