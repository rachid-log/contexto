# Hard Memory — Implementation Plan

> **Goal:** Graduate the current flat-file memory system (`memories.json`) into a persistent, semantically searchable vector database — enabling the AI agent to _recall_ past context by meaning, not just recency.

---

## 1. Current State

```
contexto/
├── context/
│   ├── append_memory.py      # Appends a new memory to memories.json
│   ├── fetch_memories.py     # Fetches N most recent memories
│   └── memory/
│       └── memories.json     # Flat JSON array of {id, date, memory}
└── .agent/
    └── GEMINI.md             # System instructions (fetch + append rules)
```

**How it works today:**
- `append_memory.py` — writes a new `{id, date, memory}` entry to `memories.json`.
- `fetch_memories.py` — reads the last N entries from `memories.json` and prints them as a markdown table.
- Retrieval is **recency-based only** — there is no semantic search.

**Limitations:**
| Problem | Impact |
|---------|--------|
| No semantic search | Agent can't find relevant memories by _meaning_, only by recency |
| Linear scan | O(n) lookup — gets slower as memories grow |
| No embeddings | Memory text is stored as raw strings with no vector representation |
| Single file | Risk of data loss; no backup/sync strategy |

---

## 2. What Is "Hard Memory"?

Hard Memory is the **persistent vector layer** that sits alongside (or replaces) the current JSON file. It:

1. **Embeds** each memory string into a high-dimensional vector (using an embedding model).
2. **Stores** the vector + metadata (id, date, raw text) in a vector database.
3. **Retrieves** memories via **semantic similarity search** — "find the 5 memories most relevant to this query."

### Soft Memory vs Hard Memory

| | Soft Memory (current) | Hard Memory (proposed) |
|---|---|---|
| **Storage** | `memories.json` (flat file) | Vector DB (ChromaDB / local SQLite+vectors) |
| **Retrieval** | Last N entries | Top-K by cosine similarity to query |
| **Embeddings** | None | Sentence-level embeddings |
| **Scalability** | Hundreds of entries | Tens of thousands+ |
| **Persistence** | File on disk | DB on disk (portable) |

---

## 3. Proposed Architecture

```
contexto/
├── context/
│   ├── append_memory.py        # UPDATED — also pushes to vector DB
│   ├── fetch_memories.py       # UPDATED — supports semantic search mode
│   ├── hard_memory.py          # NEW — core hard memory module
│   ├── sync_to_hard_memory.py  # NEW — one-time migration script
│   └── memory/
│       ├── memories.json       # KEPT — remains as the simple append log
│       └── chroma_db/          # NEW — ChromaDB persistent storage
└── .agent/
    └── GEMINI.md               # UPDATED — new commands for semantic recall
```

### Component Breakdown

#### 3.1 `hard_memory.py` — Core Module

The central module that wraps all vector DB operations.

```python
# Responsibilities:
# - Initialize / connect to ChromaDB
# - Embed + store a memory
# - Query memories by semantic similarity
# - List / delete memories
```

**Key functions:**

| Function | Description |
|----------|-------------|
| `init_db()` | Creates or connects to the local ChromaDB instance |
| `add_memory(id, date, text)` | Embeds the text and upserts into the collection |
| `search(query, top_k=5)` | Returns the top-K most semantically similar memories |
| `get_all()` | Returns all stored memories (for debugging / export) |
| `delete(id)` | Removes a memory by ID |

#### 3.2 `sync_to_hard_memory.py` — Migration Script

One-time (or repeatable) script to bulk-load all entries from `memories.json` into ChromaDB.

```
Usage: python3 ./context/sync_to_hard_memory.py
```

**Steps:**
1. Read all entries from `memories.json`
2. For each entry, call `hard_memory.add_memory(id, date, text)`
3. Report how many were synced (skipping duplicates by ID)

#### 3.3 Updated `append_memory.py`

After appending to `memories.json` (existing behavior), also push the new memory into the vector DB:

```python
# ... existing append logic ...
from hard_memory import add_memory
add_memory(next_id, current_date, user_input)
```

#### 3.4 Updated `fetch_memories.py`

Add a new `--search` / `-s` flag for semantic retrieval:

```
# Existing behavior (recency):
python3 ./context/fetch_memories.py 5

# NEW — semantic search:
python3 ./context/fetch_memories.py --search "JWT token refactoring" --top 5
```

---

## 4. Technology Choice: ChromaDB

**Why ChromaDB?**

| Criteria | ChromaDB | FAISS | Pinecone |
|----------|----------|-------|----------|
| Local / no API key | ✅ | ✅ | ❌ (cloud) |
| Persistent storage | ✅ (SQLite) | ❌ (in-memory) | ✅ |
| Built-in embeddings | ✅ (default model) | ❌ | ❌ |
| Python-native | ✅ | ✅ | ✅ |
| Zero config | ✅ | ⚠️ | ❌ |
| Metadata filtering | ✅ | ❌ | ✅ |

ChromaDB is ideal because:
- **Runs 100% locally** — no API keys, no cloud dependency.
- **Built-in embedding model** — uses `all-MiniLM-L6-v2` by default (via sentence-transformers), so we don't need to manage embeddings ourselves.
- **Persistent** — stores data in a local SQLite file, survives restarts.
- **Lightweight** — single `pip install chromadb`.

### Alternative: Use an External Embedding API

If you want higher-quality embeddings (e.g., OpenAI `text-embedding-3-small`), ChromaDB supports custom embedding functions. This can be added later as an enhancement.

---

## 5. Implementation Steps

### Phase 1: Foundation (Core Module + Migration)

| Step | Task | File(s) | Effort |
|---:|------|---------|--------|
| 1 | Install ChromaDB | `requirements.txt` | 5 min |
| 2 | Create `hard_memory.py` with `init_db`, `add_memory`, `search` | `context/hard_memory.py` | 30 min |
| 3 | Create `sync_to_hard_memory.py` to migrate existing memories | `context/sync_to_hard_memory.py` | 15 min |
| 4 | Test: sync + search manually | — | 10 min |

### Phase 2: Integration (Update Existing Scripts)

| Step | Task | File(s) | Effort |
|---:|------|---------|--------|
| 5 | Update `append_memory.py` to also write to vector DB | `context/append_memory.py` | 10 min |
| 6 | Update `fetch_memories.py` with `--search` flag | `context/fetch_memories.py` | 15 min |
| 7 | Update `.agent/GEMINI.md` with new recall commands | `.agent/GEMINI.md` | 5 min |

### Phase 3: Polish & Extend

| Step | Task | File(s) | Effort |
|---:|------|---------|--------|
| 8 | Add `--search` usage to system instructions | `.agent/GEMINI.md` | 5 min |
| 9 | Add error handling for missing ChromaDB | `hard_memory.py` | 10 min |
| 10 | Optional: swap to OpenAI embeddings for better quality | `hard_memory.py` | 15 min |
| 11 | Optional: add `forget_memory.py` (delete by ID) | `context/forget_memory.py` | 10 min |

---

## 6. Updated Agent Instructions (Preview)

After implementation, the `.agent/GEMINI.md` rules would be updated to:

```markdown
1. First check your memory by running:
   - Recent: `python3 ./context/fetch_memories.py <number>`
   - Semantic: `python3 ./context/fetch_memories.py --search "<query>" --top 5`

2. Whenever you execute a task, append a memory:
   `python3 ./context/append_memory.py "your memory text here"`
```

This gives the agent **two retrieval modes**:
- **Recency** — "what did I do recently?" (existing)
- **Relevance** — "what do I know about X?" (new)

---

## 7. Data Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Agent Workflow                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐    append_memory.py               │
│  │  New Memory   │──────────┬──────────────────┐    │
│  └──────────────┘           │                  │    │
│                             ▼                  ▼    │
│                    ┌──────────────┐   ┌────────────┐│
│                    │memories.json │   │  ChromaDB  ││
│                    │ (soft memory)│   │(hard memory)││
│                    └──────┬───────┘   └─────┬──────┘│
│                           │                 │       │
│                  fetch N  │     search by   │       │
│                  recent   │     similarity  │       │
│                           ▼                 ▼       │
│                    ┌────────────────────────────┐   │
│                    │     fetch_memories.py      │   │
│                    │  --search "query" --top K  │   │
│                    └────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 8. Example Usage

### Syncing existing memories
```bash
# One-time migration
python3 ./context/sync_to_hard_memory.py
# Output: Synced 42 memories to ChromaDB.
```

### Appending a new memory (auto-syncs to both)
```bash
python3 ./context/append_memory.py "Implemented OAuth2 for the API gateway"
# Output: Memory appended with ID 43 (soft + hard memory).
```

### Searching by meaning
```bash
python3 ./context/fetch_memories.py --search "authentication" --top 3
# Output:
# ## Semantic Search Results (top 3)
# | ID | Date | Memory | Similarity |
# |---:|------|--------|------------|
# | 43 | 15:40 24/03/2026 | Implemented OAuth2 for the API gateway | 0.91 |
# | 12 | 10:22 22/03/2026 | Added JWT token refresh logic | 0.85 |
# | 7  | 09:15 21/03/2026 | Set up login endpoint with bcrypt hashing | 0.78 |
```

---

## 9. Dependencies

```
# requirements.txt (new or updated)
chromadb>=0.4.0
```

> **Note:** ChromaDB bundles `sentence-transformers` and `all-MiniLM-L6-v2` for local embeddings. First run will download the model (~80MB). No API key needed.

---

## 10. Open Questions

| # | Question | Options |
|---|----------|---------|
| 1 | Should `memories.json` remain as the source of truth, or should ChromaDB be the primary store? | Keep both (recommended for now) |
| 2 | Should we use a cloud embedding model (OpenAI) for higher quality? | Start local, upgrade later if needed |
| 3 | Should old memories be auto-pruned from soft memory after syncing? | No — keep the full log |
| 4 | Do we need a `forget` / `delete` command? | Nice to have, not critical |
| 5 | Should the agent auto-search hard memory on every conversation start? | Yes, if a relevant query can be inferred |

---

## Summary

This plan transforms the current **append-only, recency-based** memory system into a **dual-layer architecture** where:
- **Soft memory** (`memories.json`) remains the simple, human-readable log.
- **Hard memory** (ChromaDB) enables **semantic recall** — finding relevant past context by meaning.

The implementation is **incremental** — each phase builds on the last, and the existing system continues to work throughout.
