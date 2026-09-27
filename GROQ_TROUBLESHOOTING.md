# Groq API Connection Troubleshooting

If you're seeing the error: **"The assistant is unavailable right now because the Groq service could not be reached."**

## Quick Diagnosis

Run the verification script to check your setup:

```bash
cd backend
python verify_setup.py
```

This will check:
- Environment variables
- Python imports
- Groq API connectivity
- Weather API connectivity
- Database status
- FastAPI server status

## Common Issues & Solutions

### 1. Invalid or Expired API Key

**Error Signs:**
- `Authentication failed` or `Invalid API key`
- Verification script shows API key check fails

**Solution:**
1. Get a new API key from [Groq Console](https://console.groq.com)
2. Update `backend/.env`:
   ```env
   GROQ_API_KEY=your_new_key_here
   ```
3. Restart the backend server

### 2. Network/Connectivity Issues

**Error Signs:**
- `Connection timeout` or `Connection refused`
- Verification script can't reach Groq API
- Internet seems to work fine otherwise

**Solution:**
1. Check internet connection: `ping google.com`
2. Check if firewall is blocking Groq APIs
3. Try using a different network (mobile hotspot, different WiFi)
4. Check if your country/region blocks Groq API access

### 3. Rate Limiting

**Error Signs:**
- Error mentions `rate_limit` or quota exceeded
- Happens after sending many messages quickly

**Solution:**
- Wait 1-5 minutes before trying again
- Avoid sending rapid consecutive messages
- If persistent, check your Groq account limits

### 4. API Key Doesn't Match Format

**Error Signs:**
- Key starts with `sk_` instead of `gsk_`
- Key seems incomplete or has wrong prefix

**Solution:**
Check the Groq console - API keys should start with `gsk_`

---

## Step-by-Step Verification

### Step 1: Check Environment File

```bash
cd backend
cat .env
```

You should see:
```
GROQ_API_KEY=your_private_groq_key
GROQ_MODEL=openai/gpt-oss-20b
```

### Step 2: Test API Key Directly

```bash
cd backend
python << 'EOF'
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
key = os.getenv("GROQ_API_KEY")
print(f"Key loaded: {bool(key)}")
print(f"Key starts with: {key[:10] if key else 'None'}")

try:
    client = Groq(api_key=key)
    print("✅ Groq client created successfully")
    
    # Quick test
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print("✅ API call succeeded!")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Step 3: Check Network Connection to Groq

```bash
# Test connection to Groq API servers
curl -I https://api.groq.com
```

Should return HTTP 200 or 403 (not connection timeout)

### Step 4: Test Backend Directly

```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Test API
curl "http://127.0.0.1:8000/api/health"
```

Should return: `{"status":"ok"}`

### Step 5: Test Chat Endpoint

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

If this fails, check the backend console for detailed error messages.

---

## Error Messages and Meanings

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid API key` | Wrong key format or revoked | Get new key from Groq Console |
| `Rate limit exceeded` | Too many requests | Wait and retry |
| `Connection timeout` | Network issue | Check internet/firewall |
| `404 Not Found` | Wrong endpoint | Check Groq API URL |
| `503 Service Unavailable` | Groq servers down | Check Groq status page |
| `SSL certificate error` | SSL/TLS issue | Update certificates: `pip install --upgrade certifi` |

---

## Advanced: Enable Debug Logging

Edit `backend/services/llm_service.py` and add logging:

```python
import logging
logger = logging.getLogger(__name__)

# In the try block:
try:
    logger.info(f"Sending request to Groq: {len(messages)} messages")
    completion = client.chat.completions.create(...)
    logger.info("Groq response received")
except Exception as e:
    logger.error(f"Groq error: {e}", exc_info=True)
    raise
```

Then run:
```bash
python -m uvicorn main:app --log-level debug --reload
```

---

## Groq API Alternatives If Key Doesn't Work

If the Groq API key truly cannot be fixed, alternatives include:

1. **OpenAI API** (requires paid account)
   ```
   GROQ_PROVIDER=openai
   OPENAI_API_KEY=sk_...
   ```

2. **Ollama** (local, free)
   ```
   GROQ_PROVIDER=ollama
   OLLAMA_URL=http://localhost:11434
   ```

But for now, let's focus on getting the Groq key working.

---

## Still Not Working?

1. Run `python verify_setup.py` and share the output
2. Check backend console for the full error message
3. Verify your internet connection can reach `https://api.groq.com`
4. Try with a fresh API key from Groq console
5. Check if there's an account-level limit on your Groq account

---

**Last Updated**: September 27, 2026
