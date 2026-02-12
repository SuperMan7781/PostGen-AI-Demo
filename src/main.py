import sys
import os

# 1. Setup paths so Python can find your other files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retrieval.search import VectorSearch
from generation.generation import generate_viral_post

def main():
    print("\n" + "="*60)
    print("   🚀 PostGen AI - The Viral LinkedIn Creator")
    print("="*60)

    # 2. Get User Input
    topic = input("\n✍️  What topic do you want to write about? (e.g., 'Remote Work'): ").strip()
    
    if not topic:
        print("❌ Error: You must enter a topic!")
        return

    # 3. Search for Viral Inspiration (The "RAG" Step)
    print(f"\n🔎 Searching database for high-performing posts about '{topic}'...")
    
    try:
        searcher = VectorSearch()
        viral_examples = searcher.search(topic, limit=3)
    except Exception as e:
        print(f"⚠️ Search Warning: Could not retrieve examples ({e}). Writing from scratch.")
        viral_examples = []

    # Show the user what we found
    if not viral_examples:
        print("   -> No exact matches found. The AI will be creative!")
    else:
        print(f"✅ Found {len(viral_examples)} viral examples to learn from:")
        for i, ex in enumerate(viral_examples):
            # Show a snippet and the match score
            score = ex.get('score', 0)
            print(f"   [{i+1}] Match: {score:.2f} | 👍 {ex['reactions']} Reactions")

    # 4. Generate the Post (The "Generation" Step)
    print("\n🧠 AI is analyzing patterns and writing your post...")
    final_post = generate_viral_post(topic, viral_examples)

    # 5. Display Result
    print("\n" + "="*60)
    print("✨ YOUR VIRAL POST IS READY ✨")
    print("="*60 + "\n")
    print(final_post)
    print("\n" + "="*60)
    print("💡 Tip: Copy/Paste this directly to LinkedIn!")

if __name__ == "__main__":
    main()