# Smart Homemaker Frontend Setup and Run Guide

## Prerequisites

Before running the frontend, ensure you have the following installed:

- **Node.js 16+** (preferably Node.js 18+ or 20+)
- **npm** or **yarn** (Node package manager)
- **Backend Server** running on `http://127.0.0.1:8000`

## Installation Steps

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

Or if you prefer yarn:
```bash
yarn install
```

### 3. Configure Backend URL (if needed)

By default, the frontend connects to `http://127.0.0.1:8000`. If your backend runs on a different URL:

Edit `frontend/src/api.js` and update the base URL:

```javascript
const API_BASE = "http://your-backend-url:8000/api";
```

## Running the Development Server

### Start the Frontend

```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.0  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

Open your browser and navigate to: **http://localhost:5173**

## Build for Production

To create an optimized production build:

```bash
npm run build
```

This will generate a `dist/` folder with optimized files ready for deployment.

### Preview Production Build

```bash
npm run preview
```

## Understanding the Frontend Structure

```
frontend/
├── index.html                 # Main HTML file
├── src/
│   ├── App.jsx               # Main app component with routing
│   ├── index.css             # Global styles (clean, no gradients)
│   ├── main.jsx              # Entry point
│   ├── api.js                # API client functions
│   ├── useReminderAlerts.js  # Custom hook for reminders
│   ├── components/           # Reusable components
│   │   ├── Chat.jsx          # Chat interface
│   │   ├── WeatherCard.jsx   # Weather display
│   │   ├── ReminderList.jsx  # Reminders display
│   │   ├── FoodSuggestions.jsx # Food suggestions
│   │   └── Decorator.jsx     # Room decoration tool
│   └── pages/                # Page components
│       ├── Home.jsx          # Home/dashboard
│       ├── Assistant.jsx     # AI Assistant page
│       ├── Food.jsx          # Food suggestions page
│       ├── Reminders.jsx     # Reminders management
│       ├── Decorate.jsx      # Room decoration page
│       ├── PrivacyPolicy.jsx # Privacy policy
│       └── TermsConditions.jsx # Terms & conditions
├── public/                   # Static assets
│   └── favicon.svg          # Website favicon
├── package.json             # Dependencies
└── vite.config.js          # Build configuration
```

## Key Features

### UI Design
- ✅ Clean, professional design (no purple gradients)
- ✅ Professional rectangular buttons (not pill-shaped)
- ✅ No emoji icons or excessive animations
- ✅ Responsive layout for mobile and desktop
- ✅ Minimal, accessible color scheme

### Pages
- ✅ **Home** - User profile and quick info
- ✅ **Assistant** - AI chat interface
- ✅ **Food** - Food suggestions and recipes
- ✅ **Reminders** - Cooking reminders management
- ✅ **Decorate** - Room decoration suggestions
- ✅ **Privacy Policy** - Complete privacy policy
- ✅ **Terms & Conditions** - Full T&C page

### Features
- **Dynamic API Calls** - All data is fetched from backend in real-time
- **User Profile** - Save name, city, state, language
- **Weather** - Real-time weather from Open-Meteo API
- **Recipes** - Browse and save recipes by region
- **AI Chat** - Interact with Groq LLM for cooking help
- **Reminders** - Set cooking reminders
- **Voice Input** - Voice-to-text chat (browser dependent)

## Development Guidelines

### No Prohibited Elements
- ❌ No purple gradients - Use solid colors only
- ❌ No pill-shaped buttons - Use rectangular with subtle radius
- ❌ No fake reviews - No testimonials
- ❌ No fake metrics - No visitor counts or testimonials
- ❌ No vague hero text - Clear, descriptive sections
- ❌ No emoji icons - Use text or SVG only
- ❌ No em dashes — Use regular hyphens or spaces
- ❌ No over-the-top animations - Subtle transitions only
- ❌ No AI slop photos - Real photos only (when needed)
- ❌ No cursor animations - Standard pointer cursor
- ❌ No fake customer counters - No misleading metrics

### Design Principles
- **Professional** - Business-grade design
- **Minimal** - Only essential UI elements
- **Fast** - Quick load times, smooth interactions
- **Accessible** - Screen reader friendly
- **Responsive** - Works on all devices

## Styling Reference

### Color Palette
```css
--bg: #f6f1e8;        /* Background */
--card: #fffdf8;      /* Card background */
--ink: #243027;       /* Text color */
--muted: #5d6b62;     /* Secondary text */
--green: #2e5c45;     /* Primary accent */
--accent: #c46b3a;    /* Secondary accent */
--line: #e6ddd0;      /* Borders */
```

### Typography
- **Font Family**: System fonts (no serif)
  - `-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif`
- **Line Height**: 1.6 (readable)
- **Font Sizes**: Consistent, no extremes

### Buttons
```css
/* Primary Button */
background: #2e5c45;      /* Green */
padding: 12px 16px;       /* Comfortable */
border-radius: 4px;       /* Subtle corners, not pill-shaped */
transition: all 0.2s ease; /* Smooth, not instant */

/* Secondary Button */
background: white;
border: 1px solid #2e5c45;
color: #2e5c45;
```

### Cards
```css
background: white;
border: 1px solid #e0e0e0;      /* Light border */
border-radius: 6px;              /* Subtle corners */
box-shadow: 0 1px 2px rgba(...); /* Minimal shadow */
padding: 20px;                   /* Comfortable spacing */
```

## Connecting to Backend

### API Configuration
The frontend uses a simple API client in `src/api.js`. All backend calls go through this file.

**Example API Call:**
```javascript
// In api.js
export async function getWeather(city) {
  const res = await fetch(`${API_BASE}/weather?city=${encodeURIComponent(city)}`);
  if (!res.ok) throw new Error("Weather fetch failed");
  return res.json();
}

// In a component
const weather = await getWeather("Chennai");
```

### Required Backend Endpoints
- `GET /api/health` - Server status
- `GET /api/profile` - User profile
- `PUT /api/profile` - Update profile
- `GET /api/weather?city=<city>` - Weather data
- `GET /api/foods` - Food suggestions
- `GET /api/foods/{id}` - Food details
- `GET /api/reminders` - Get reminders
- `POST /api/reminders` - Create reminder
- `POST /api/chat` - Send chat message

## Troubleshooting

### Port Already in Use

If port 5173 is already in use:
```bash
npm run dev -- --port 3000
```

### Backend Connection Issues

1. **Error: Cannot reach backend**
   - Verify backend is running: `curl http://127.0.0.1:8000/api/health`
   - Check `API_BASE` URL in `src/api.js`
   - Ensure CORS is enabled in backend

2. **CORS errors**
   - Backend CORS settings in `backend/main.py` may need updating
   - For development, should allow `http://localhost:5173`

### Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
npm run build
```

## Production Deployment

### Using a Static Host (Vercel, Netlify, etc.)

1. Build the project:
   ```bash
   npm run build
   ```

2. Deploy the `dist/` folder

3. Update backend URL in environment variables if needed

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Environment Variables

For production, you may need to set the backend URL. Create a `.env.production`:
```
VITE_API_BASE=https://your-api-domain.com/api
```

Then update `src/api.js`:
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";
```

## Performance Tips

- ✅ Images are optimized
- ✅ No large animation libraries
- ✅ Minimal CSS (only what's needed)
- ✅ Efficient React patterns (no unnecessary re-renders)
- ✅ Fast API calls (no polling, event-based)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Voice input requires modern browsers (Chrome, Edge, Safari)

## Package Dependencies

Key packages used:
- **React** - UI library
- **React Router** - Client-side routing
- **Vite** - Build tool (fast, modern)

See `package.json` for complete list.

---

**Version**: 1.0.0  
**Last Updated**: September 27, 2026

## Next Steps

1. ✅ Start backend: `cd backend && python -m uvicorn main:app --reload`
2. ✅ Start frontend: `cd frontend && npm run dev`
3. ✅ Open http://localhost:5173
4. ✅ Configure custom domain before launch
5. ✅ Test all features end-to-end
