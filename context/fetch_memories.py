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
    parser.add_argument("-p", "--project", type=str, help="Filter by specific project scope.")
    parser.add_argument("-g", "--global", dest="is_global", action="store_true", help="Filter by global scope only.")
    parser.add_argument("-a", "--all", dest="is_all", action="store_true", help="Fetch memories from all scopes (bypass filtering).")
    
    args = parser.parse_args()
    
    project_filter = None
    if args.is_all:
        project_filter = "all"
    elif args.is_global:
        project_filter = "global"
    elif args.project:
        project_filter = args.project
    else:
        project_filter = os.path.basename(os.getcwd())

    total = db_count(project_filter)
    if total == 0:
        print("Hard Memory is completely empty.")
        return

    if args.search:
        # SEMANTIC SEARCH
        print(f"## Semantic Search Results for: '{args.search}' (Scope: {project_filter})\n")
        results = semantic_search(args.search, args.top, project=project_filter)
        
        if not results:
            print("No matching memories found.")
            return
            
        print("| ID | Date | Project | Memory | Relevance |")
        print("|---:|------|---------|--------|-----------|")
        for res in results:
            # Distance is returned; smaller is better.
            relevance = max(0, 1 - res['distance'])
            print(f"| {res['id']} | {res['date']} | {res['project']} | {res['memory']} | {relevance:.2f} |")
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

        fetched = get_recent(count, project=project_filter)
        
        if not fetched:
            print("No memories found.")
            return
            
        print(f"## Recent Memories ({len(fetched)} of {total} in Scope: {project_filter})\n")
        print("| ID | Date | Project | Memory |")
        print("|---:|------|---------|--------|")
        for mem in fetched:
            print(f"| {mem['id']} | {mem['date']} | {mem['project']} | {mem['memory']} |")


if __name__ == "__main__":
    main()
