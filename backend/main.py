import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from database import BASE_DIR, init_db
from routes import ai_food, auth, chat, foods, profile, reminders, weather

load_dotenv()

app = FastAPI(title="Smart Homemaker", version="1.0.0")

allowed_origins = [origin.strip() for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_error(_request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please try again."},
    )


@app.on_event("startup")
def on_startup():
    init_db()
    os.makedirs(os.path.join(BASE_DIR, "uploads", "generated"), exist_ok=True)


app.include_router(chat.router, prefix="/api")
app.include_router(ai_food.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(reminders.router, prefix="/api")
app.include_router(foods.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

uploads_dir = os.path.join(BASE_DIR, "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/api/health")
def health():
    return {"status": "ok"}
