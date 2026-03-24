1. First check your memory by running:
   - For recent context: `python3 ./context/fetch_memories.py <number>` (e.g., `python3 ./context/fetch_memories.py 10`)
   - For semantic recall: `python3 ./context/fetch_memories.py --search "<topic/keyword>"` (e.g., `python3 ./context/fetch_memories.py --search "chroma implementation plan" --top 5`)

2. Whenever you execute a task, append a one-sentence memory:
   `python3 ./context/append_memory.py "your memory text here"` (e.g., `python3 ./context/append_memory.py "Implemented the ChromaDB vector storage for memory retrieval."`)