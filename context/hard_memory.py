#!/usr/bin/env python3
"""
hard_memory.py — Core hard memory module.

All memory storage and retrieval is handled via ChromaDB (vector database).
This is the single source of truth for the memory system.
"""
import os
import chromadb

# Path to the persistent database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory", "chroma_db")
COLLECTION_NAME = "memories"


def init_db():
    """Initializes and returns the ChromaDB collection."""
    os.makedirs(DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def _next_id(collection):
    """Determines the next sequential integer ID from the collection."""
    if collection.count() == 0:
        return 1
    # Get all metadata to find the max numeric ID
    all_data = collection.get()
    max_id = 0
    for meta in all_data["metadatas"]:
        mem_id = meta.get("id", 0)
        if isinstance(mem_id, (int, float)) and mem_id > max_id:
            max_id = int(mem_id)
    return max_id + 1


def add_memory(text, date=None):
    """
    Embeds the text and stores it in chromaDB.

    Args:
        text: The memory text to store.
        date: Optional date string. Defaults to current time in HH:MM dd/mm/yyyy format.

    Returns:
        The integer ID assigned to the new memory.
    """
    if date is None:
        from datetime import datetime
        date = datetime.now().strftime("%H:%M %d/%m/%Y")

    collection = init_db()
    next_id = _next_id(collection)

    collection.add(
        documents=[text],
        metadatas=[{"id": next_id, "date": date}],
        ids=[str(next_id)]
    )
    return next_id


def get_recent(count=5):
    """
    Returns the N most recent memories, sorted by ID descending.

    Args:
        count: Number of recent memories to return.

    Returns:
        List of dicts with keys: id, date, memory.
    """
    collection = init_db()
    if collection.count() == 0:
        return []

    all_data = collection.get()
    memories = []
    for i in range(len(all_data["ids"])):
        memories.append({
            "id": all_data["metadatas"][i].get("id", 0),
            "date": all_data["metadatas"][i].get("date", ""),
            "memory": all_data["documents"][i],
        })

    # Sort by ID descending (most recent first), then take top N
    memories.sort(key=lambda m: m["id"], reverse=True)
    return memories[:count]


def search(query, top_k=5):
    """
    Searches for the top-k most semantically similar memories.

    Args:
        query: The search text.
        top_k: Number of results to return.

    Returns:
        List of dicts with keys: id, date, memory, distance.
    """
    collection = init_db()
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count())
    )

    formatted = []
    if results and results["ids"] and len(results["ids"]) > 0:
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["metadatas"][0][i]["id"],
                "date": results["metadatas"][0][i]["date"],
                "memory": results["documents"][0][i],
                "distance": results["distances"][0][i],
            })
    return formatted


def get_all():
    """Returns all memories stored in the collection."""
    collection = init_db()
    return collection.get()


def count():
    """Returns the total number of memories."""
    collection = init_db()
    return collection.count()


def delete(memory_id):
    """Deletes a memory by its numeric ID."""
    collection = init_db()
    collection.delete(ids=[str(memory_id)])
    return True


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(f"Searching for: {sys.argv[1]}")
        results = search(sys.argv[1])
        for r in results:
            print(f"  [{r['id']}] {r['date']} — {r['memory']} (dist: {r['distance']:.3f})")
    else:
        print(f"Total memories: {count()}")
