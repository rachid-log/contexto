import os
import json
import sys

# Ensure the parent directory is in the path so we can import hard_memory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from hard_memory import add_memory

# Path to the memories.json
MEMORIES_PATH = os.path.join(current_dir, "memory", "memories.json")

def sync():
    if not os.path.exists(MEMORIES_PATH):
        print(f"No existing memories file found at {MEMORIES_PATH}")
        return

    with open(MEMORIES_PATH, "r") as f:
        try:
            memories = json.load(f)
        except json.JSONDecodeError:
            print("Failed to decode memories.json. File may be empty or malformed.")
            return

    print(f"Syncing {len(memories)} memories...")
    
    count = 0
    for entry in memories:
        try:
            # We use the existing ID and Date
            add_memory(entry['id'], entry['date'], entry['memory'])
            count += 1
        except Exception as e:
            print(f"Failed to sync memory ID {entry.get('id', 'unknown')}: {e}")

    print(f"Successfully synced {count} memories to ChromaDB.")

if __name__ == "__main__":
    sync()
