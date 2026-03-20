import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the keys
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GEMINI_API_KEY not found in .env file!")

# 2. Configure the Brain
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def critique_post(topic, generated_post, viral_examples):
    """
    Evaluates the generated LinkedIn post against viral standards.
    Acts as a 'Critic' agent in a multi-agent workflow.
    """
    
    examples_text = ""
    for i, ex in enumerate(viral_examples):
        examples_text += f"\n--- EXAMPLE {i+1} ---\n{ex.get('text', '')[:500]}...\n"

    prompt = f"""
    You are an elitist LinkedIn Content Strategist and Growth Hacker.
    Your job is to CRITIQUE a generated LinkedIn post and give actionable feedback for refinement.
    
    USER'S TOPIC: "{topic}"
    
    --- 📊 REFERENCE VIRAL POSTS ---
    We want to mimic the energy and spacing of these:
    {examples_text}
    
    --- 📝 GENERATED POST TO CRITIQUE ---
    {generated_post}
    
    --- INSTRUCTIONS ---
    Evaluate the generated post based on 4 criteria. Give a score /10 for each.
    
    1. **Hook (Scroll-Stopping)**: Is the first line high-impact? (Controversial, surprising, or question)
    2. **Formatting & Pace**: Are there short 1-2 sentence paragraphs? Large spacing? Punchy?
    3. **Call to Action (CTA)**: Does it drive comments or engagement effectively at the end?
    4. **Authenticity**: Does it feel corporate/AI-heavy or human/vulnerable?
    
    Provide your output STRICTLY in this format:
    
    --- 🏆 CRITIQUE REPORT ---
    🪝 Hook Score: X/10
    📝 Formatting Score: X/10
    📣 CTA Score: X/10
    🤝 Authenticity Score: X/10
    
    --- 💡 IMPROVEMENTS NEEDED ---
    - [List 2-3 specific, actionable changes to make the post better]
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Critic Agent Error: {str(e)}"
