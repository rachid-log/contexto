#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

def main():
    # Set the base directory to the root of the project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # The memories are stored in the context/ folder
    memories_file = os.path.join(base_dir, 'memory', 'memories.json')
    
    # Read existing memories
    if os.path.exists(memories_file):
        try:
            with open(memories_file, 'r') as f:
                memories = json.load(f)
        except json.JSONDecodeError:
            print(f"File {memories_file} is empty or invalid JSON. Initializing as empty list.")
            memories = []
    else:
        # If the file or directory doesn't exist, create it
        if not os.path.exists(os.path.dirname(memories_file)):
            os.makedirs(os.path.dirname(memories_file))
        memories = []
        
    # Calculate next id
    next_id = 1
    if memories:
        ids = [m.get('id', 0) for m in memories]
        if ids:
            next_id = max(ids) + 1
        
    # Check for CLI argument, otherwise prompt for input
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Enter new memory: ")
        
    if not user_input.strip():
        print("Memory cannot be empty.")
        return
        
    # Get current date in custom format hh:mm dd/mm/yyyy
    current_date = datetime.now().strftime("%H:%M %d/%m/%Y")
    
    # Create new memory object
    new_memory = {
        "id": next_id,
        "date": current_date,
        "memory": user_input
    }
    
    memories.append(new_memory)
    
    # Write back to memories.json
    with open(memories_file, 'w') as f:
        json.dump(memories, f, indent=2)
        
    print(f"Memory appended successfully with ID {next_id} in {memories_file}.")

if __name__ == "__main__":
    main()
