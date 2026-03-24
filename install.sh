#!/usr/bin/env bash

set -e

# Define variables
REPO_URL="https://github.com/rachid-log/contexto.git"
INSTALL_DIR="${INSTALL_DIR:-$HOME/contexto}"

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
echo "To get started, simply run the following commands:"
echo ""
echo "1. Go to the project directory:"
echo "   cd $INSTALL_DIR"
echo ""
echo "2. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "3. Save a memory:"
echo "   python3 ./context/append_memory.py \"Installed Contexto memory system on my machine.\""
echo ""
echo "4. Fetch recent memories:"
echo "   python3 ./context/fetch_memories.py 5"
echo ""
echo "Happy hacking! 🧠"
