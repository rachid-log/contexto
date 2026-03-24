#!/usr/bin/env python3
import json
import os
import sys
import argparse

# Ensure the parent directory is in the path so we can import hard_memory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from hard_memory import search as semantic_search

def main():
    # Set the base directory relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    memories_file = os.path.join(base_dir, 'memory', 'memories.json')

    # Load memories for background info (count)
    if os.path.exists(memories_file):
        try:
            with open(memories_file, 'r') as f:
                memories = json.load(f)
        except (json.JSONDecodeError, ValueError):
            memories = []
    else:
        memories = []

    parser = argparse.ArgumentParser(description="Fetch memories from soft or hard memory.")
    parser.add_argument("count", type=int, nargs="?", help="Number of recent memories to fetch (default if no search)")
    parser.add_argument("--search", "-s", type=str, help="Search for memories semantically")
    parser.add_argument("--top", "-t", type=int, default=5, help="Top K results for semantic search (default: 5)")
    
    args = parser.parse_args()
    
    if args.search:
        # SEMANTIC SEARCH (Hard Memory)
        print(f"## Semantic Search Results for: '{args.search}'\n")
        results = semantic_search(args.search, args.top)
        
        if not results:
            print("No matching memories found.")
            return
            
        print("| ID | Date | Memory | Relevance |")
        print("|---:|------|--------|-----------|")
        for res in results:
            # Distance is returned; smaller is better. Chroma default L2 distance on normalized vectors.
            # We display (1 - distance) as a simple relevance score.
            relevance = max(0, 1 - res['distance'])
            print(f"| {res['id']} | {res['date']} | {res['memory']} | {relevance:.2f} |")
    else:
        # RECENCY FETCH (Soft Memory)
        count = args.count
        if count is None:
             if sys.stdin.isatty():
                 try:
                    count_str = input("How many memories to fetch? ")
                    count = int(count_str) if count_str.strip() else 10
                 except (ValueError, EOFError):
                    count = 10
             else:
                 count = 10 # Default when non-interactive
        
        if count <= 0:
            print("Error: number must be greater than 0.")
            return

        if not memories:
            print("No memories found.")
            return
            
        fetched = memories[-count:]
        print(f"## Recent Memories ({len(fetched)} of {len(memories)})\n")
        print("| ID | Date | Memory |")
        print("|---:|------|--------|")
        for mem in fetched:
            print(f"| {mem['id']} | {mem['date']} | {mem['memory']} |")

if __name__ == "__main__":
    main()
