#!/usr/bin/env python3
"""
fetch_memories.py — Retrieves past memories from Hard Memory (ChromaDB).

Usage:
    # Recency (default):
    python3 ./context/fetch_memories.py 5
    
    # Semantic Search:
    python3 ./context/fetch_memories.py --search "your query" --top 5
"""
import os
import sys
import argparse

# Ensure we can import hard_memory from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hard_memory import search as semantic_search, get_recent, count as db_count


def main():
    parser = argparse.ArgumentParser(description="Fetch memories from Hard Memory.")
    parser.add_argument("count", type=int, nargs="?", help="Number of recent memories to fetch (default: 10 if no search)")
    parser.add_argument("--search", "-s", type=str, help="Search for memories semantically")
    parser.add_argument("--top", "-t", type=int, default=5, help="Top K results for semantic search (default: 5)")
    
    args = parser.parse_args()
    
    total = db_count()
    if total == 0:
        print("Hard Memory is completely empty.")
        return

    if args.search:
        # SEMANTIC SEARCH
        print(f"## Semantic Search Results for: '{args.search}'\n")
        results = semantic_search(args.search, args.top)
        
        if not results:
            print("No matching memories found.")
            return
            
        print("| ID | Date | Memory | Relevance |")
        print("|---:|------|--------|-----------|")
        for res in results:
            # Distance is returned; smaller is better.
            relevance = max(0, 1 - res['distance'])
            print(f"| {res['id']} | {res['date']} | {res['memory']} | {relevance:.2f} |")
    else:
        # RECENCY FETCH
        count = args.count
        if count is None:
            if sys.stdin.isatty():
                try:
                    count_str = input("How many memories to fetch? ")
                    count = int(count_str) if count_str.strip() else 10
                except (ValueError, EOFError):
                    count = 10
            else:
                count = 10
        
        if count <= 0:
            print("Error: number must be greater than 0.")
            return

        fetched = get_recent(count)
        
        if not fetched:
            print("No memories found.")
            return
            
        print(f"## Recent Memories ({len(fetched)} of {total})\n")
        print("| ID | Date | Memory |")
        print("|---:|------|--------|")
        for mem in fetched:
            print(f"| {mem['id']} | {mem['date']} | {mem['memory']} |")


if __name__ == "__main__":
    main()
