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


def add_memory(text, date=None, project="global"):
    """
    Embeds the text and stores it in chromaDB.

    Args:
        text: The memory text to store.
        date: Optional date string. Defaults to current time in HH:MM dd/mm/yyyy format.
        project: Optional project scope identifier. Defaults to "global".

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
        metadatas=[{"id": next_id, "date": date, "project": project}],
        ids=[str(next_id)]
    )
    return next_id


def get_recent(count=5, project=None):
    """
    Returns the N most recent memories, sorted by ID descending.

    Args:
        count: Number of recent memories to return.
        project: Optional project string to filter by.

    Returns:
        List of dicts with keys: id, date, project, memory.
    """
    collection = init_db()
    if collection.count() == 0:
        return []

    where_clause = {"project": project} if project and project != "all" else None
    
    if where_clause:
        all_data = collection.get(where=where_clause)
    else:
        all_data = collection.get()

    if not all_data.get("ids"):
        return []

    memories = []
    for i in range(len(all_data["ids"])):
        memories.append({
            "id": all_data["metadatas"][i].get("id", 0),
            "date": all_data["metadatas"][i].get("date", ""),
            "project": all_data["metadatas"][i].get("project", "global"),
            "memory": all_data["documents"][i],
        })

    # Sort by ID descending (most recent first), then take top N
    memories.sort(key=lambda m: m["id"], reverse=True)
    return memories[:count]


def search(query, top_k=5, project=None):
    """
    Searches for the top-k most semantically similar memories.

    Args:
        query: The search text.
        top_k: Number of results to return.
        project: Optional project string to filter by.

    Returns:
        List of dicts with keys: id, date, project, memory, distance.
    """
    collection = init_db()
    if collection.count() == 0:
        return []

    where_clause = {"project": project} if project and project != "all" else None
    
    kwargs = {
        "query_texts": [query],
        "n_results": min(top_k, collection.count())
    }
    
    if where_clause:
        kwargs["where"] = where_clause

    results = collection.query(**kwargs)

    formatted = []
    if results and results["ids"] and len(results["ids"]) > 0:
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["metadatas"][0][i]["id"],
                "date": results["metadatas"][0][i]["date"],
                "project": results["metadatas"][0][i].get("project", "global"),
                "memory": results["documents"][0][i],
                "distance": results["distances"][0][i],
            })
    return formatted


def get_all(project=None):
    """Returns all memories stored in the collection."""
    collection = init_db()
    where_clause = {"project": project} if project and project != "all" else None
    if where_clause:
        return collection.get(where=where_clause)
    return collection.get()


def count(project=None):
    """Returns the total number of memories."""
    collection = init_db()
    where_clause = {"project": project} if project and project != "all" else None
    if where_clause:
        return len(collection.get(where=where_clause).get("ids", []))
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
