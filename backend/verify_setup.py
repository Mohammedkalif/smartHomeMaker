#!/usr/bin/env python3
"""
Smart Homemaker Backend Verification Script
Checks if all services and APIs are properly configured and working.
"""

import os
import sys
import httpx
from dotenv import load_dotenv

print("=" * 60)
print("Smart Homemaker Backend Verification")
print("=" * 60)

# Load environment
load_dotenv()

# 1. Check environment variables
print("\n1. Environment Variables")
print("-" * 60)
groq_key = os.getenv("GROQ_API_KEY", "").strip()
groq_model = os.getenv("GROQ_MODEL", "").strip()
weather_provider = os.getenv("WEATHER_PROVIDER", "").strip()

if groq_key:
    print(f"✅ GROQ_API_KEY: {groq_key[:20]}...{groq_key[-4:]}")
else:
    print("❌ GROQ_API_KEY: NOT SET")
    
if groq_model:
    print(f"✅ GROQ_MODEL: {groq_model}")
else:
    print("❌ GROQ_MODEL: NOT SET")
    
if weather_provider:
    print(f"✅ WEATHER_PROVIDER: {weather_provider}")
else:
    print("❌ WEATHER_PROVIDER: NOT SET (defaulting to openweathermap)")

# 2. Check Python module imports
print("\n2. Python Module Imports")
print("-" * 60)
modules = ["fastapi", "sqlalchemy", "groq", "httpx"]
for module in modules:
    try:
        __import__(module)
        print(f"✅ {module}: OK")
    except ImportError as e:
        print(f"❌ {module}: MISSING ({e})")

# 3. Test Groq API connectivity
print("\n3. Groq API Connection")
print("-" * 60)
try:
    from groq import Groq
    if not groq_key or groq_key == "your_groq_api_key_here":
        print("❌ API Key is missing or invalid")
        print("   → Set GROQ_API_KEY in backend/.env")
    else:
        print("    Testing Groq connection...")
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model=groq_model or "openai/gpt-oss-20b",
            messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
            max_tokens=10
        )
        print("✅ Groq API: Connected successfully!")
        print(f"   Response: {response.choices[0].message.content}")
except Exception as e:
    error_msg = str(e)
    print(f"❌ Groq API: Connection failed")
    print(f"   Error: {error_msg[:150]}")
    if "authentication" in error_msg.lower():
        print("   → Check if API key is valid")
    elif "timeout" in error_msg.lower() or "connection" in error_msg.lower():
        print("   → Check your internet connection")
    elif "rate" in error_msg.lower():
        print("   → Rate limit reached. Please wait and try again.")
    else:
        print("   → Check API key and network connectivity")

# 4. Test Weather API
print("\n4. Weather API Connection")
print("-" * 60)
try:
    print("    Testing Open-Meteo API...")
    with httpx.Client(timeout=10) as client:
        response = client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": "London", "count": 1}
        )
        response.raise_for_status()
        print("✅ Open-Meteo Geocoding: OK")
    
    print("    Testing forecast API...")
    with httpx.Client(timeout=10) as client:
        response = client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 51.5074,
                "longitude": -0.1278,
                "current": "temperature_2m",
            }
        )
        response.raise_for_status()
        print("✅ Open-Meteo Forecast: OK")
except httpx.HTTPError as e:
    print(f"❌ Weather API: Request failed ({e})")
except Exception as e:
    print(f"❌ Weather API: Connection error ({e})")

# 5. Check Database
print("\n5. Database")
print("-" * 60)
try:
    from database import init_db
    print("    Initializing database...")
    init_db()
    print("✅ Database: SQLite OK")
    
    # Check if seeded
    from database import get_db
    from models import Food, User
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///./smart_homemaker.db")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    user_count = db.query(User).count()
    food_count = db.query(Food).count()
    print(f"    Users: {user_count}")
    print(f"    Foods: {food_count}")
    
    if user_count > 0 and food_count > 0:
        print("✅ Database: Properly seeded")
    else:
        print("⚠️  Database: May need seeding")
    db.close()
except Exception as e:
    print(f"❌ Database: Error ({e})")

# 6. Test FastAPI
print("\n6. FastAPI Server")
print("-" * 60)
try:
    import httpx
    print("    Checking if server is running on http://127.0.0.1:8000...")
    with httpx.Client(timeout=5) as client:
        response = client.get("http://127.0.0.1:8000/api/health")
        if response.status_code == 200:
            print("✅ FastAPI: Server is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  FastAPI: Server returned {response.status_code}")
except Exception as e:
    print(f"❌ FastAPI: Server not reachable")
    print(f"   → Start the backend with: python -m uvicorn main:app --reload --port 8000")

# 7. Summary and recommendations
print("\n" + "=" * 60)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 60)

issues = []
if not groq_key or groq_key == "your_groq_api_key_here":
    issues.append("❌ Groq API key not configured")
if not groq_model:
    issues.append("❌ Groq model not configured")

if not issues:
    print("✅ All systems appear to be configured correctly!")
    print("\nNext steps:")
    print("1. Start the backend: python -m uvicorn main:app --reload --port 8000")
    print("2. Start the frontend: npm run dev (from frontend/ directory)")
    print("3. Open http://localhost:5173 in your browser")
else:
    print("Issues found:")
    for issue in issues:
        print(f"  {issue}")
    print("\nFix these issues and try again.")

print("\n" + "=" * 60)
