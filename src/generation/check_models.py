import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found. Check your .env file.")
else:
    genai.configure(api_key=api_key)
    print("🔍 Scanning available models for your API key...")
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ FOUND: {m.name}")
                count += 1
        if count == 0:
            print("⚠️ No content generation models found. Check API key permissions.")
    except Exception as e:
        print(f"❌ Error listing models: {e}")