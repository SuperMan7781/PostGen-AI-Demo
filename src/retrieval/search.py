from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuration (Must match ingest.py)
COLLECTION_NAME = "linkedin_posts"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

class VectorSearch:
    def __init__(self):
        # Connect to Database
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        # Load the same Brain (Model) used for ingestion
        # (This loads faster the second time because it's already downloaded)
        print("🧠 Loading Search Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def search(self, query_text, limit=3):
        """
        Finds the top 'limit' posts that are semantically similar to the query.
        """
        # 1. Convert user query to vector
        query_vector = self.model.encode(query_text).tolist()

        # 2. Search Qdrant
        search_result = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit
        )

        # 3. Format results
        results = []
        for hit in search_result:
            results.append({
                "score": hit.score,  # How similar is it? (0 to 1)
                "author": hit.payload.get("author"),
                "reactions": hit.payload.get("reactions"),
                "text": hit.payload.get("text")
            })
            
        return results

# Quick Test (Only runs if you run this file directly)
if __name__ == "__main__":
    searcher = VectorSearch()
    # Test query
    topic = "remote work productivity hacks"
    print(f"\n🔎 Searching for patterns about: '{topic}'...")
    
    hits = searcher.search(topic)
    
    for i, hit in enumerate(hits):
        print(f"\n--- Result {i+1} (Score: {hit['score']:.2f}) ---")
        print(f"👍 Reactions: {hit['reactions']}")
        print(f"📝 Content: {hit['text'][:150]}...") # Show first 150 chars