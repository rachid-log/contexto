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


import argparse

def main():
    parser = argparse.ArgumentParser(description="Appends a new memory to Hard Memory (ChromaDB).")
    parser.add_argument("-m", "--message", type=str, nargs="*", help="The memory text to store.")
    parser.add_argument("-p", "--project", type=str, help="Specifically set the project scope name.")
    parser.add_argument("-g", "--global", dest="is_global", action="store_true", help="Store this memory globally rather than scoped to a project.")
    
    # Parse known args so we can still accept un-flagged text seamlessly
    args, unknown = parser.parse_known_args()

    # Determine message text
    text_parts = []
    if args.message:
        text_parts.extend(args.message)
    if unknown:
        text_parts.extend(unknown)
        
    if text_parts:
        text = " ".join(text_parts)
    else:
        text = input("Enter new memory: ")

    if not text.strip():
        print("Error: Memory cannot be empty.")
        sys.exit(1)
        
    # Determine project scope
    project = "global"
    if args.is_global:
        project = "global"
    elif args.project:
        project = args.project
    else:
        project = os.path.basename(os.getcwd())

    memory_id = add_memory(text, project=project)
    print(f"Memory #{memory_id} saved to Hard Memory (Scope: {project}).")


if __name__ == "__main__":
    main()
