from fastapi import APIRouter, HTTPException, Query

from services.weather_service import get_weather

router = APIRouter()


@router.get("/weather")
def weather(city: str = Query(..., min_length=1)):
    result = get_weather(city)
    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])
    return result
