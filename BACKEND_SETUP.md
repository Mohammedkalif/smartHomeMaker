# Smart Homemaker Backend Setup and Run Guide

## Prerequisites

Before running the backend, ensure you have the following installed:

- **Python 3.9+** (preferably Python 3.10 or higher)
- **pip** (Python package manager)
- **git** (optional, but recommended)

## Installation Steps

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create a Virtual Environment

It's recommended to use a Python virtual environment to isolate dependencies.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

The `.env` file is already configured with:
- **GROQ_API_KEY**: Set this to a valid key from your Groq Console. Never commit or share it.
- **WEATHER_PROVIDER**: Set to `open-meteo` (free, open-source weather API)
- **WEATHER_API_KEY**: Empty (not required for open-meteo)

If you need to modify any settings, edit the `.env` file:

```bash
nano .env  # or open with your preferred editor
```

### 5. Initialize the Database

On first run, the database will be automatically created and seeded with sample data:

```bash
# The database is initialized automatically when the server starts
# But you can manually verify it with:
python -c "from database import init_db; init_db()"
```

## Running the Backend

### Option 1: Using Python (Simple)

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The server will start at `http://127.0.0.1:8000`

### Option 2: Using Uvicorn Directly

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Option 3: Production Mode (No Auto-Reload)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Verifying the Backend is Running

Once started, you should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Quick Health Check

Open your browser or use curl:

```bash
curl http://127.0.0.1:8000/api/health
```

Expected response:
```json
{"status":"ok"}
```

## Available API Endpoints

### Health Check
- `GET /api/health` - Check if server is running

### Profile Management
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `GET /api/states` - List available states

### Weather
- `GET /api/weather?city=<city_name>` - Get current weather for a city

Example:
```bash
curl "http://127.0.0.1:8000/api/weather?city=Chennai"
```

### Food & Recipes
- `GET /api/foods?state=<state>&meal_type=<breakfast|lunch|dinner>` - Get food suggestions
- `GET /api/foods/{food_id}` - Get specific food details and recipe

Example:
```bash
curl "http://127.0.0.1:8000/api/foods?state=Tamil%20Nadu&meal_type=breakfast"
```

### Chat & AI Assistant
- `POST /api/chat` - Send chat message to AI assistant

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I cook for dinner?"}'
```

### Reminders
- `GET /api/reminders` - Get all reminders
- `POST /api/reminders` - Create new reminder
- `PUT /api/reminders/{reminder_id}` - Update reminder
- `DELETE /api/reminders/{reminder_id}` - Delete reminder

### Decoration & Image Generation
- `POST /api/decorate` - Generate room decoration suggestions

## Configuration Details

### Environment Variables (in `.env`)

| Variable | Value | Description |
|----------|-------|-------------|
| `GROQ_API_KEY` | Your private Groq key | API key for Groq LLM service |
| `GROQ_MODEL` | `openai/gpt-oss-20b` | The configured Groq model |
| `WEATHER_PROVIDER` | `open-meteo` | Weather data provider (no API key needed) |
| `WEATHER_API_KEY` | (empty) | Leave empty for open-meteo |
| `IMAGE_PROVIDER` | `mock` | Image generation provider |

### Weather API

The backend uses **Open-Meteo** (https://open-meteo.com/), which is:
- ✅ Free
- ✅ No API key required
- ✅ Open-source
- ✅ Accurate
- ✅ Rate-limited generously

All weather data is fetched dynamically - no cached/hardcoded values.

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
# Use a different port
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### Database Issues

To reset the database:
```bash
rm smart_homemaker.db  # Delete the database file
# On next run, it will be recreated and seeded automatically
```

### Missing Dependencies

If you encounter import errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Groq API Errors

Verify your internet connection and that the API key is correctly set in `.env`. Test with:
```python
python -c "from services.llm_service import chat_with_tools; print('Groq API is configured')"
```

### Weather API Not Responding

Open-meteo rarely goes down, but if it does:
```bash
# Test weather endpoint
curl "http://127.0.0.1:8000/api/weather?city=London"
```

## Connecting Frontend to Backend

Make sure your frontend is configured to connect to the backend:

**Frontend Default Configuration:**
- Backend URL: `http://127.0.0.1:8000` (as per `frontend/src/api.js`)

**For Development:**
- Backend runs on `localhost:8000`
- Frontend runs on `localhost:5173`

**For Production:**
- Update CORS settings in `backend/main.py` (currently allows only localhost)
- Update frontend API endpoint in `frontend/src/api.js`

## Developer Notes

### Dynamic API Calls

All data in this application is fetched dynamically:
- **Weather**: Real-time from Open-Meteo API
- **Recipes & Foods**: From SQLite database (populated on startup)
- **Chat**: Dynamic calls to Groq API with real tool execution
- **Reminders**: Stored in SQLite, queried dynamically

No hardcoded JSON files or mock data are used after initialization.

### Database Schema

The application uses SQLite with the following main tables:
- `users` - User profiles
- `foods` - Food/dish database
- `recipes` - Recipe details
- `reminders` - Cooking reminders
- `states` - Available states/regions

### Key Services

- **`services/llm_service.py`** - Groq API integration for AI chat
- **`services/weather_service.py`** - Open-Meteo weather integration
- **`services/image_service.py`** - Image generation (currently mocked)

## Support & Further Help

For issues or questions:
1. Check the error logs in the terminal
2. Verify all environment variables are set correctly in `.env`
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check that your API keys are valid (especially for Groq)

---

**Version**: 1.0.0  
**Last Updated**: September 27, 2026
