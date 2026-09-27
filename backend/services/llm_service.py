import json
import os
from typing import List

from dotenv import load_dotenv
from groq import Groq
from sqlalchemy.orm import Session

from tools import cooking_tools, food_tools, profile_tools, weather_tools

load_dotenv()

DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You are Smart Homemaker, a helpful household assistant that speaks in the user's preferred language.

Your responsibilities:
1. Help manage the whole home: create a task or reminder whenever the user asks, including tasks extracted from natural chat such as "call the plumber tomorrow"
2. Provide real-time weather information for planning indoor/outdoor activities
3. Suggest regional Indian recipes based on the user's state and meal preferences
4. Generate creative AI recipes when database recipes aren't available

Important guidelines:
- When a user asks to remember, remind, schedule, or add a task, use create_household_task. Set has_timing true only when they give a specific timing; otherwise set it false. Untimed tasks must never be presented as a reminder.
- When a user mentions cooking something with a specific duration, create a reminder (e.g., "rice cooking for 15 minutes")
- If cooking time is uncertain, ask for clarification rather than guessing
- Always use the user's saved state and preferences for suggestions
- Use tools to fetch current/database information - never invent weather, recipes, or user data
- Keep responses brief, friendly and practical
- Always respond in the user's preferred language unless they explicitly ask otherwise
- Be creative with recipe suggestions but stay practical
- Help with multiple reminders if the user is cooking several dishes at once

When tools are unavailable:
- Still help with general cooking advice
- Ask clarifying questions about preferences
- Suggest standard cooking times based on common practices
- When recipe details are needed, provide creative suggestions the user can customize

Remember: Your goal is to make household management easier and more enjoyable."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_household_task",
            "description": "Create a household task or reminder from the user's chat message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {"type": "string"},
                    "duration_minutes": {"type": "integer", "description": "Minutes from now. Use 1440 as a storage value when has_timing is false."},
                    "has_timing": {"type": "boolean", "description": "True only when the user specified a time or duration."},
                    "reminder_message": {"type": "string"},
                },
                "required": ["task_name", "duration_minutes", "reminder_message", "has_timing"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_cooking_reminder",
            "description": "Create a cooking reminder in the household database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_name": {"type": "string"},
                    "duration_minutes": {"type": "integer"},
                    "reminder_message": {"type": "string"},
                },
                "required": ["food_name", "duration_minutes", "reminder_message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_food_suggestions",
            "description": "Get regional food suggestions from the local database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {"type": "string"},
                    "meal_type": {
                        "type": "string",
                        "description": "breakfast, lunch, dinner, or snack",
                    },
                    "ingredients": {"type": "string"},
                },
                "required": ["state", "meal_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recipe",
            "description": "Get a simple recipe from the local database.",
            "parameters": {
                "type": "object",
                "properties": {"dish_name": {"type": "string"}},
                "required": ["dish_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_profile",
            "description": "Get the saved user name, state, city and preferred language.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

_conversation: List[dict] = []


def _run_tool(name: str, arguments: dict, db: Session, user_id: int):
    if name == "create_household_task":
        return cooking_tools.create_cooking_reminder(
            db,
            food_name=arguments.get("task_name", "Household task"),
            duration_minutes=arguments.get("duration_minutes", 1440),
            reminder_message=arguments.get("reminder_message", "Remember this household task."),
            has_timing=arguments.get("has_timing", False),
            user_id=user_id,
        )
    if name == "create_cooking_reminder":
        return cooking_tools.create_cooking_reminder(
            db,
            food_name=arguments.get("food_name", ""),
            duration_minutes=arguments.get("duration_minutes", 15),
            reminder_message=arguments.get("reminder_message", "Check the food."),
            user_id=user_id,
        )
    if name == "get_weather":
        return weather_tools.get_weather(arguments.get("city", ""))
    if name == "get_food_suggestions":
        return food_tools.get_food_suggestions(
            db,
            state=arguments.get("state", ""),
            meal_type=arguments.get("meal_type", ""),
            ingredients=arguments.get("ingredients"),
        )
    if name == "get_recipe":
        return food_tools.get_recipe(db, dish_name=arguments.get("dish_name", ""))
    if name == "get_user_profile":
        return profile_tools.get_user_profile(db, user_id)
    return {"error": f"Unknown tool: {name}"}


def chat_with_tools(user_message: str, db: Session, user_id: int) -> str:
    # Read environment at request time, so a corrected .env works after a reload.
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    groq_model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        return "AI is not configured yet. Add a valid GROQ_API_KEY to backend/.env and restart the server."

    profile = profile_tools.get_user_profile(db, user_id)
    language = profile.get("language", "English")
    system = (
        SYSTEM_PROMPT
        + f"\nThe user's preferred language is {language}."
        + f"\nSaved profile: {json.dumps(profile)}"
    )

    messages = [{"role": "system", "content": system}]
    messages.extend(_conversation[-16:])
    messages.append({"role": "user", "content": user_message})

    client = Groq(api_key=groq_api_key)

    try:
        for _ in range(6):
            completion = client.chat.completions.create(
                model=groq_model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.4,
            )
            choice = completion.choices[0].message
            tool_calls = choice.tool_calls or []

            if not tool_calls:
                reply = (choice.content or "").strip()
                _conversation.append({"role": "user", "content": user_message})
                _conversation.append({"role": "assistant", "content": reply})
                return reply or "I am here if you need help at home."

            assistant_message = {
                "role": "assistant",
                "content": choice.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in tool_calls
                ],
            }
            messages.append(assistant_message)

            for tool_call in tool_calls:
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = _run_tool(tool_call.function.name, arguments, db, user_id)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

        return "I could not finish that request. Please try again with a shorter message."
    except Exception as e:
        error_msg = str(e)
        print(f"Groq API Error: {error_msg}")
        lowered = error_msg.lower()
        if "model" in lowered and ("not found" in lowered or "does not exist" in lowered):
            return f"The configured AI model ({groq_model}) is unavailable. Set GROQ_MODEL={DEFAULT_GROQ_MODEL} in backend/.env and restart the server."
        if "authentication" in lowered or "invalid api key" in lowered:
            return "The Groq API key is invalid or expired. Replace GROQ_API_KEY in backend/.env with a new key from Groq Console, then restart the server."
        elif "rate" in error_msg.lower():
            return "Rate limit reached. Please try again in a moment."
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            return "Network connection issue. Please check your internet connection."
        return f"Assistant error: {error_msg[:100]}"
