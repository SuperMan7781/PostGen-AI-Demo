import pandas as pd
import ast
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import os

# --- CONFIGURATION ---
DATA_PATH = "data/viral_posts.csv"
COLLECTION_NAME = "linkedin_posts"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
MIN_REACTIONS = 10 

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.replace("...see more", "").replace("…see more", "")
    return text.strip()

def ingest_data():
    print("🚀 Starting Ingestion Pipeline...")

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"DTO: Loaded {len(df)} raw rows.")
    except FileNotFoundError:
        print("❌ Error: viral_posts.csv not found in data/ folder.")
        return

    # 2. Data Cleaning & Filtering
    if 'reactions' in df.columns:
        df['reactions'] = pd.to_numeric(df['reactions'], errors='coerce').fillna(0)
        df = df[df['reactions'] >= MIN_REACTIONS]
    
    df['content'] = df['content'].apply(clean_text)
    df = df[df['content'].str.len() > 20]

    if df.empty:
        print("⚠️ Warning: No data left after filtering!")
        return

    # 3. Initialize Vector Database
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑️ Deleted existing collection: {COLLECTION_NAME}")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    print(f"✅ Created collection: {COLLECTION_NAME}")

    # 4. Generate Embeddings
    print("🧠 Generating Embeddings...")
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    documents = df['content'].tolist()
    # This will be FAST this time because of caching
    embeddings = encoder.encode(documents, show_progress_bar=True)

    # 5. Upload to Qdrant (WITH CHUNKING)
    print("cw Uploading vectors to Qdrant (in batches)...")
    
    batch_points = []
    names = df['name'].fillna('Unknown').tolist()
    reactions = df['reactions'].tolist()
    
    for idx, (text, name, react, emb) in enumerate(zip(documents, names, reactions, embeddings)):
        batch_points.append(models.PointStruct(
            id=idx,
            vector=emb.tolist(),
            payload={
                "author": str(name),
                "reactions": int(react),
                "text": text
            }
        ))

    # --- THE FIX IS HERE ---
    CHUNK_SIZE = 100  # Upload 100 posts at a time safely
    for i in range(0, len(batch_points), CHUNK_SIZE):
        chunk = batch_points[i : i + CHUNK_SIZE]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=chunk
        )
        print(f"   ⬆️ Uploaded batch {i} to {i + len(chunk)}...")

    print(f"🎉 Success! Ingested {len(batch_points)} posts into '{COLLECTION_NAME}'")

if __name__ == "__main__":
    ingest_data()