# Persistent Contextual Memory (Hard Memory)

You have a built-in "Hard Memory" system backed by a vector database. You **MUST** use this exact format to continually store and review progress to ensure context continues across different sessions.

### 1. Retrieve Past Context Before Acting
Before executing tasks, always check your memory to understand what happened previously.

**A. Recency Fetch (What just happened?)**
Use this to see the most recent log of actions.
*   Command: `python3 ./context/fetch_memories.py <COUNT>`
*   Example: `python3 ./context/fetch_memories.py 5` (fetches the last 5 executed tasks).

**B. Semantic Recall (What do we know about this topic?)**
Use this when you need context about a specific feature, tool, or goal to avoid starting from scratch.
*   Command: `python3 ./context/fetch_memories.py --search "<YOUR_QUERY>"`
*   Example: `python3 ./context/fetch_memories.py --search "OAuth2 token implementation"`

### 2. Append Memory After Executing Actions
After you have completed a meaningful chunk of work, encountered a critical error, or made a major decision, you **MUST** record it as a one-sentence memory.

*   Command: `python3 ./context/append_memory.py "<YOUR_MEMORY_TEXT>"`
*   Example: `python3 ./context/append_memory.py "Refactored the core authentication flow, replacing sessions with JWT tokens."`

> **Note:** Keep your appended memories highly descriptive but concise. Always include technical details (e.g., file names, library versions, decisions made) so that your future self can easily understand the context using semantic searches.