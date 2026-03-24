import os
import chromadb
from datetime import datetime

# Path to the persistent database
DB_PATH = os.path.join(os.path.dirname(__file__), "memory", "chroma_db")

def init_db():
    """Initializes and returns the ChromaDB collection."""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Initialize the persistent client
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Get or create the collection
    collection = client.get_or_create_collection(name="memories")
    return collection

def add_memory(memory_id, date, text):
    """Embeds the text and adds it to the persistent collection."""
    collection = init_db()
    
    # Add to collection (Chroma IDs must be strings)
    collection.add(
        documents=[text],
        metadatas=[{"id": int(memory_id), "date": date}],
        ids=[str(memory_id)]
    )
    return True

def search(query, top_k=5):
    """Searches for the top-k most semantically similar memories."""
    collection = init_db()
    
    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()) if collection.count() > 0 else 0
    )
    
    # Format results
    formatted = []
    if results and results['ids'] and len(results['ids']) > 0:
        for i in range(len(results['ids'][0])):
            formatted.append({
                "id": results['metadatas'][0][i]['id'],
                "date": results['metadatas'][0][i]['date'],
                "memory": results['documents'][0][i],
                "distance": results['distances'][0][i]
            })
    return formatted

def get_all():
    """Returns all memories stored in the collection."""
    collection = init_db()
    return collection.get()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(f"Searching for: {sys.argv[1]}")
        print(search(sys.argv[1]))
    else:
        print(f"Collection count: {init_db().count()}")
