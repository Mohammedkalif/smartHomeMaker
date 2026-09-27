import os

from sqlalchemy import inspect, text

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smart_homemaker.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
# Render Postgres URLs use postgres://, while SQLAlchemy expects postgresql://.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine_options = {"pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from models import Food, Recipe, Reminder, State, User  # noqa: F401

    Base.metadata.create_all(bind=engine)
    # SQLite does not add newly declared columns to an existing table.
    inspector = inspect(engine)
    reminder_columns = {column["name"] for column in inspector.get_columns("reminders")}
    if "has_timing" not in reminder_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE reminders ADD COLUMN has_timing BOOLEAN NOT NULL DEFAULT 1"))
    user_columns = {column["name"] for column in inspector.get_columns("users")}
    if "password_hash" not in user_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
    from seed import seed_if_empty

    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
