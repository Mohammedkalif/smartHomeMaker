#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
print(f"API Key present: {bool(api_key)}")
if api_key:
    print(f"API Key preview: {api_key[:30]}...")

# Test Groq connection
try:
    from groq import Groq
    print("✅ Groq library imported successfully")
    
    client = Groq(api_key=api_key)
    print("✅ Groq client instantiated")
    
    # Test with minimal request
    result = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print("✅ Groq API working! Response received")
    print(f"Test response: {result.choices[0].message.content}")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ API Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    sys.exit(1)
