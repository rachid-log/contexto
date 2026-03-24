# Contexto 🧠

Contexto is a powerful, persistent local memory system (Hard Memory) powered by ChromaDB. It helps AI agents and developers maintain context seamlessly by storing and retrieving structured memories for ongoing software development tasks and projects.

## Setup & Installation 🚀

You can set up Contexto on your machine with a single one-liner command. Just open your terminal and run:

```bash
curl -sSL https://raw.githubusercontent.com/rachid-log/contexto/main/install.sh | bash
```

### What does the installation script do?
- **Clones** the repository into `~/contexto` (or pulls the latest changes if already cloned).
- **Sets up a Python virtual environment** (`.venv`).
- **Installs the necessary dependencies**, such as `chromadb`.

## Usage Overview 🛠️

Once it's installed, you can interact directly with the context memory system using the following scripts. 

Ensure you've navigated to the root directory and activated the virtual environment before trying any commands:

```bash
cd ~/contexto
source .venv/bin/activate
```

### 1. Saving a New Memory

After making major changes or solving a problem, permanently store what happened using the `append_memory.py` script:

```bash
python3 ./context/append_memory.py "Refactored the core authentication flow, replacing sessions with JWT tokens."
```

### 2. Fetching Recent Context (Sequential Recall)

Before beginning a new task, fetch the latest context to understand exactly what was done previously. This retrieves chronological logs.

```bash
# Fetches the last 5 executed task logs
python3 ./context/fetch_memories.py 5
```

### 3. Semantic Search Mode (Topic Recall)

You can also leverage ChromaDB's built-in intelligent vectorization to semantically search your historical memory space.

```bash
# Retrieve past memories related to a specific topic
python3 ./context/fetch_memories.py --search "OAuth2 token implementation"
```

## System Requirements
- `python` 3.x
- `git`
- `curl`
