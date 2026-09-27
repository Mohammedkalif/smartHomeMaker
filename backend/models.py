from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(100), nullable=False)
    password_hash = mapped_column(String(255), nullable=True)
    state = mapped_column(String(100), nullable=False)
    city = mapped_column(String(100), nullable=False)
    language = mapped_column(String(50), nullable=False, default="English")

    reminders = relationship("Reminder", back_populates="user")


class State(Base):
    __tablename__ = "states"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(100), unique=True, nullable=False)


class Food(Base):
    __tablename__ = "foods"

    id = mapped_column(Integer, primary_key=True, index=True)
    state = mapped_column(String(100), nullable=False, index=True)
    dish_name = mapped_column(String(150), nullable=False)
    meal_type = mapped_column(String(50), nullable=False)
    description = mapped_column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="food", uselist=False)


class Recipe(Base):
    __tablename__ = "recipes"

    id = mapped_column(Integer, primary_key=True, index=True)
    food_id = mapped_column(Integer, ForeignKey("foods.id"), nullable=True)
    dish_name = mapped_column(String(150), nullable=False, index=True)
    ingredients = mapped_column(Text, nullable=False)
    instructions = mapped_column(Text, nullable=False)

    food = relationship("Food", back_populates="recipe")


class Reminder(Base):
    __tablename__ = "reminders"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = mapped_column(String(150), nullable=False)
    reminder_message = mapped_column(Text, nullable=False)
    remind_at = mapped_column(DateTime, nullable=False)
    has_timing = mapped_column(Boolean, default=True, nullable=False)
    completed = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reminders")
