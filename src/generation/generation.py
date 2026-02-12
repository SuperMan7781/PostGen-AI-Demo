import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the keys from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GEMINI_API_KEY not found in .env file!")

# 2. Configure the Brain
genai.configure(api_key=api_key)

# We use the NEWEST model available to you
# 'gemini-2.5-flash' is faster and smarter than Pro 1.0
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_viral_post(topic, viral_examples):
    """
    Creates a LinkedIn post using the 'Few-Shot' technique.
    It looks at real viral examples before writing.
    """
    
    # Format the examples into a string
    examples_text = ""
    for i, ex in enumerate(viral_examples):
        examples_text += f"\n--- EXAMPLE {i+1} (Reactions: {ex.get('reactions', 0)}) ---\n{ex.get('text', '')[:600]}...\n"

    # This is the "Prompt Engineering" part
    prompt = f"""
    You are a viral content expert for LinkedIn. 
    You write in a punchy, authentic, and engaging style (short sentences, generous spacing).
    
    Here is the USER'S TOPIC: "{topic}"
    
    Here are 3 REAL VIRAL EXAMPLES of high-performing posts. Analyze their structure, hooks, and tone:
    {examples_text}
    
    --- INSTRUCTIONS ---
    1. Write a NEW post about "{topic}".
    2. DO NOT copy the examples directly. Instead, mimic their *formatting* and *energy*.
    3. Start with a "Scroll-Stopping Hook" (a controversial statement or a surprising fact).
    4. Use short paragraphs (1-2 sentences max).
    5. End with a clear Call to Action (CTA) or a question to drive comments.
    
    WRITE THE POST NOW:
    """
    
    # 3. Call the API
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# Quick Test (Only runs if you run this specific file)
if __name__ == "__main__":
    # Fake data just to test the connection
    dummy_examples = [
        {"text": "I quit my job today to start a bakery...", "reactions": 5000},
        {"text": "Remote work is not the future, it is the present...", "reactions": 1200},
        {"text": "Hiring is broken. Here is how I fixed it...", "reactions": 3000}
    ]
    
    print("🧠 Testing Gemini 2.5 Flash Connection...")
    result = generate_viral_post("Salary Negotiation", dummy_examples)
    print("\n" + "="*40)
    print(result)
    print("="*40)