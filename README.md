# Smart Homemaker

Smart Homemaker is a full-stack household assistant application: an AI-powered helper for cooking reminders, weather, regional Indian food ideas, and home decoration suggestions.

**Key Principle**: No AI slop, no fake reviews, no gradient aesthetics. Clean, professional, dynamic API calls only.

## Quick Start

- **Backend**: See [BACKEND_SETUP.md](./BACKEND_SETUP.md) for complete installation and running instructions
- **Frontend**: See [FRONTEND_SETUP.md](./FRONTEND_SETUP.md) for complete setup instructions

### Minimal Quick Start

Backend (Terminal 1):
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Frontend (Terminal 2):
```bash
cd frontend
npm install
npm run dev
```

Then open **http://127.0.0.1:5173**

## Architecture

The React frontend talks only to FastAPI. FastAPI talks to Groq for AI. When Groq requests tools, Python functions execute them:

```
Browser (React) 
    ↓ /api/chat
FastAPI (Python)
    ↓ API call
Groq (LLM)
    ↓ tool calls
Python Functions
    ↓ read/write
SQLite + Weather API + Image Generator
```

**Key Point**: The LLM never touches the database directly. All data flows through validated Python functions.

## Features

- ✅ **AI Chat** - Groq LLM with tool calling for cooking help
- ✅ **Voice Input** - Speech-to-text in browser (Chrome recommended)
- ✅ **Real-time Weather** - From Open-Meteo API (free, no key needed)
- ✅ **Regional Recipes** - Indian cuisines by state
- ✅ **Cooking Reminders** - SQLite-backed, browser notifications
- ✅ **User Profile** - Name, city, state, preferred language
- ✅ **Secure Login** - Create an account or sign in with name and password
- ✅ **Multilingual AI** - English, Tamil, Hindi, Malayalam, Telugu, Kannada
- ✅ **Home Decoration** - Upload room photos for suggestions
- ✅ **Privacy & Terms** - Complete legal pages included

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18 + Vite |
| **Backend** | Python 3.9+ + FastAPI |
| **Database** | SQLite + SQLAlchemy ORM |
| **LLM** | Groq API (Llama 3.3 70B) |
| **Weather** | Open-Meteo (free, open-source) |
| **Images** | Mock (default), Pollinations, or OpenAI (optional) |

## Project Structure

```
smart-homemaker/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # SQLite setup
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── seed.py                 # Initial data
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Configuration (pre-configured)
│   ├── services/               # API integrations
│   │   ├── llm_service.py      # Groq integration
│   │   ├── weather_service.py  # Open-Meteo integration
│   │   └── image_service.py    # Image generation
│   ├── routes/                 # API endpoints
│   │   ├── chat.py
│   │   ├── weather.py
│   │   ├── foods.py
│   │   ├── reminders.py
│   │   ├── profile.py
│   │   └── decorate.py
│   └── tools/                  # Tool functions
│       ├── cooking_tools.py
│       ├── food_tools.py
│       ├── weather_tools.py
│       └── profile_tools.py
├── frontend/
│   ├── index.html              # Main HTML
│   ├── src/
│   │   ├── main.jsx            # Entry point
│   │   ├── App.jsx             # Routing
│   │   ├── api.js              # API client
│   │   ├── index.css           # Clean styles (no gradients)
│   │   ├── components/         # Reusable UI
│   │   └── pages/              # Page components
│   ├── public/                 # Static assets
│   └── package.json            # npm dependencies
├── README.md                   # This file
├── BACKEND_SETUP.md           # Detailed backend guide
└── FRONTEND_SETUP.md          # Detailed frontend guide
```

## Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 16+** (for frontend)
- **npm or yarn** (Node package manager)
- **Internet connection** (for Groq and weather APIs)

## Environment Configuration

Create a local `backend/.env` from `backend/.env.example` and set your own keys:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
WEATHER_PROVIDER=open-meteo
WEATHER_API_KEY=                    # Not needed for open-meteo
IMAGE_PROVIDER=mock                 # No real images generated
```

Never commit `.env` files or API keys. Use Render environment variables in production.

## Database

SQLite database (`smart_homemaker.db`) is created automatically on first run with:

- Demo user: Asha, from Erode, Tamil Nadu
- 50+ regional dishes with recipes
- All states and languages pre-configured

To reset: `rm backend/smart_homemaker.db` (recreated on next server start)

## Deployment

The project includes a Render Blueprint that deploys the frontend and backend as separate services with managed PostgreSQL. Follow [DEPLOYMENT.md](./DEPLOYMENT.md).

## Deployment Checklist

Before launching:

- [ ] Backend running on configured domain
- [ ] Frontend deployed (Vercel, Netlify, or custom server)
- [ ] Custom domain configured (not localhost)
- [ ] Favicon added (✅ Done - `public/favicon.svg`)
- [ ] Privacy Policy page added (✅ Done)
- [ ] Terms & Conditions page added (✅ Done)
- [ ] Removed "Made with AI" tagline (✅ Done)
- [ ] UI design reviewed for professionalism (✅ Done)
  - No purple gradients
  - No pill-shaped buttons
  - No fake reviews or metrics
  - No vague hero text
  - No emoji icons
  - No excessive animations
- [ ] All API calls are dynamic (✅ Verified)
- [ ] No hardcoded JSON files
- [ ] CORS configured for production domain
- [ ] SSL/HTTPS enabled

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
uvicorn main:app --port 8001
```

**Missing Groq API errors:**
Check `backend/.env` - key should be set automatically.

**Weather not working:**
Open-Meteo rarely fails, but test: `curl "http://127.0.0.1:8000/api/weather?city=London"`

**Database errors:**
```bash
cd backend && rm smart_homemaker.db
# Restart server - DB recreates automatically
```

### Frontend Issues

**API connection failed:**
- Ensure backend is running on `http://127.0.0.1:8000`
- Check console: `curl http://127.0.0.1:8000/api/health`

**Port 5173 in use:**
```bash
npm run dev -- --port 3000
```

**Node modules issues:**
```bash
rm -rf node_modules
npm install
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Server status |
| GET/PUT | `/api/profile` | User profile |
| GET | `/api/weather?city=<name>` | Real-time weather |
| GET | `/api/foods?state=<st>&meal_type=<type>` | Food suggestions |
| GET | `/api/foods/{id}` | Recipe details |
| POST | `/api/chat` | Chat with AI |
| GET | `/api/reminders` | Get reminders |
| POST | `/api/reminders` | Create reminder |
| POST | `/api/decorate` | Decoration suggestions |

## Example Interactions

**Chat with AI:**
- User: "I put rice on the stove"
  - Groq calls `create_cooking_reminder` → Reminder set
- User: "What's the weather?"
  - Groq calls `get_weather` → Current conditions shown
- User: "Tamil Nadu dinner ideas"
  - Groq calls `get_food_suggestions` → Recipes displayed
- User: "Tell me in Tamil"
  - Profile language set → Replies in Tamil

**Voice Input:**
- Click "Mic" button → Grant permission → Speak → Automatic submission

**Cooking Reminders:**
- Set reminder → Toast notification → Browser notification (if enabled)
- Mark as complete → Moves to completed list

## Performance

- ✅ No large libraries (Vite + React only)
- ✅ No unnecessary animations
- ✅ Efficient database queries (SQLAlchemy ORM)
- ✅ Real-time weather (no caching)
- ✅ Responsive design (works on mobile)
- ✅ Light CSS (4KB)

## Code Quality

- ✅ No AI-generated images
- ✅ No AI-generated copy (all original)
- ✅ No cursor animations
- ✅ No gradient backgrounds
- ✅ Professional typograp­hy (sans-serif)
- ✅ Proper error handling
- ✅ Rate limiting-aware
- ✅ Input validation on all endpoints

## Development Notes

### Adding New Features

1. **Backend**: Add endpoint in `backend/routes/`
2. **Tool**: Create function in `backend/tools/` if it needs database/API access
3. **Frontend**: Add page in `frontend/src/pages/`
4. **API Client**: Add function in `frontend/src/api.js`

### Database Migrations

SQLAlchemy ORM handles simple schema changes. For complex migrations:
1. Update model in `models.py`
2. Delete `smart_homemaker.db`
3. Restart server

### Adding Languages

1. Add language to `LANGUAGES` in `backend/routes/profile.py`
2. Frontend automatically supports it in profile
3. Groq LLM supports responses in any language

## Support & Documentation

- Backend Setup: [BACKEND_SETUP.md](./BACKEND_SETUP.md)
- Frontend Setup: [FRONTEND_SETUP.md](./FRONTEND_SETUP.md)
- Privacy: [/privacy](http://localhost:5173/privacy)
- Terms: [/terms](http://localhost:5173/terms)

## License

This is an educational project. Use at your own discretion.

---

**Version**: 1.0.0  
**Last Updated**: September 27, 2026  
**Status**: Ready for custom domain deployment
