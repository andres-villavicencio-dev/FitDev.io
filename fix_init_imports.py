#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix import statements in FitDev.io __init__.py files
"""

import os
import re
from pathlib import Path

def update_init_imports(file_path):
    """Update import statements in __init__ files.
    
    Args:
        file_path: Path to the file to update
    """
    print(f"Processing {file_path}")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace relative imports with absolute imports
    content = re.sub(r'from agents\.', r'from fitdev.agents.', content)
    content = re.sub(r'from critics\.', r'from fitdev.critics.', content)
    
    # Write updated content
    with open(file_path, 'w') as f:
        f.write(content)

def process_init_files(directory):
    """Process all __init__.py files in a directory recursively.
    
    Args:
        directory: Path to the directory to process
    """
    for root, _, files in os.walk(directory):
        if '__init__.py' in files:
            update_init_imports(os.path.join(root, '__init__.py'))

if __name__ == "__main__":
    # Process agent and critic directories
    base_dir = Path(__file__).resolve().parent
    process_init_files(os.path.join(base_dir, 'fitdev', 'agents'))
    process_init_files(os.path.join(base_dir, 'fitdev', 'critics'))
    print("Import statements in __init__.py files updated successfully")