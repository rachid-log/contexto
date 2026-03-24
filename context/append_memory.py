#!/usr/bin/env python3
"""
append_memory.py — Appends a new memory to Hard Memory (ChromaDB).

Usage:
    python3 ./context/append_memory.py "your memory text here"
"""
import os
import sys

# Ensure we can import hard_memory from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hard_memory import add_memory


def main():
    # Get memory text from CLI args or interactive prompt
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter new memory: ")

    if not text.strip():
        print("Error: Memory cannot be empty.")
        sys.exit(1)

    memory_id = add_memory(text)
    print(f"Memory #{memory_id} saved to Hard Memory.")


if __name__ == "__main__":
    main()
