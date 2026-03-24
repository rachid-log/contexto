# Persistent Contextual Memory (Hard Memory)

You have a built-in "Hard Memory" system backed by a vector database. You **MUST** use this exact format to continually store and review progress to ensure context continues across different sessions.

### Memory Scopes (Important!)
Memories are scoped to Projects to prevent context bleed. By default, running these scripts stores/fetches memories scoped to the **current working directory's basename**. 
* **Project Scope (Default)**: Best for project-specific tasks and logs.
* **Global Scope (`--global` or `-g`)**: Best for saving/searching universal knowledge not tied to a specific project.
* **All Scopes (`--all` or `-a`)**: Best for searching across everything simultaneously (only available for fetching).

### 1. Retrieve Past Context Before Acting
Before executing tasks, always check your memory to understand what happened previously.

**A. Recency Fetch (What just happened?)**
Use this to see the most recent log of actions for the current project.
*   Command: `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py <COUNT>`
*   Example: `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py 5`
*   Example (All Scopes): `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py 5 --all`

**B. Semantic Recall (What do we know about this topic?)**
Use this when you need context about a specific feature, tool, or goal to avoid starting from scratch.
*   Command: `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py --search "<YOUR_QUERY>"`
*   Example (Project Scope): `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py --search "OAuth2 token implementation"`
*   Example (Global Search): `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/fetch_memories.py --search "general server setup" --all`

### 2. Append Memory After Executing Actions
After you have completed a meaningful chunk of work, encountered a critical error, or made a major decision, you **MUST** record it as a one-sentence memory.

*   Command: `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/append_memory.py -m "<YOUR_MEMORY_TEXT>"`
*   Example (Current Project): `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/append_memory.py -m "Refactored the core authentication flow."`
*   Example (Global Knowledge): `source ~/.contexto/.venv/bin/activate && python3 ~/.contexto/context/append_memory.py -m "Always use .env for secrets globally." --global`

> **Note:** Keep your appended memories highly descriptive but concise. Always include technical details (e.g., file names, library versions, decisions made) so that your future self can easily understand the context using semantic searches.