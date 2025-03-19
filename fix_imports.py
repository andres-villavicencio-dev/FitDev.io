#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix import statements in FitDev.io files
"""

import os
import re
from pathlib import Path

def update_file_imports(file_path):
    """Update import statements in a file.
    
    Args:
        file_path: Path to the file to update
    """
    print(f"Processing {file_path}")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace model imports
    content = re.sub(r'from models\.', r'from fitdev.models.', content)
    content = re.sub(r'from config\.', r'from fitdev.config.', content)
    
    # Write updated content
    with open(file_path, 'w') as f:
        f.write(content)

def process_directory(directory):
    """Process all Python files in a directory recursively.
    
    Args:
        directory: Path to the directory to process
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                update_file_imports(os.path.join(root, file))

if __name__ == "__main__":
    # Process agent and critic directories
    base_dir = Path(__file__).resolve().parent
    process_directory(os.path.join(base_dir, 'fitdev', 'agents'))
    process_directory(os.path.join(base_dir, 'fitdev', 'critics'))
    print("Import statements updated successfully")