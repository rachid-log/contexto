#!/usr/bin/env bash

echo "RACHID LOG"

set -e

# Define variables
REPO_URL="https://github.com/rachid-log/contexto.git"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.contexto}"

echo "=========================================="
echo " 🚀 Installing Contexto Memory System "
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git could not be found. Please install git and try again."
    exit 1
fi

# Clone or pull the repository
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "📂 Contexto directory already exists at $INSTALL_DIR"
    echo "🔄 Pulling latest changes..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📥 Cloning Contexto repository into $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 could not be found. Please install python3."
    exit 1
fi

python3 -m venv .venv

# Install dependencies
echo "📦 Installing requirements (ChromaDB, etc.)..."
source .venv/bin/activate
pip install --upgrade pip --quiet
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install chromadb>=0.4.0
fi

# Final setup messages
echo ""
echo "=========================================="
echo " ✅ Installation Complete! "
echo "=========================================="
echo ""
echo "Contexto has been installed in: $INSTALL_DIR"
echo ""
echo "To enable Hard Memory in any given project, copy the GEMINI.md instructions:"
echo "   mkdir -p .agent"
echo "   cp $INSTALL_DIR/.agent/GEMINI.md .agent/GEMINI.md"
echo ""
echo "The agent will use the global scripts located at $INSTALL_DIR."
echo "You can manually test it from any folder using:"
echo "   source $INSTALL_DIR/.venv/bin/activate && python3 $INSTALL_DIR/context/append_memory.py -m \"Hello Memory!\""
echo "   source $INSTALL_DIR/.venv/bin/activate && python3 $INSTALL_DIR/context/fetch_memories.py 5"
echo ""
echo "Happy hacking! 🧠"
