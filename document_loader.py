"""
Document loading and file operations
"""

import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def load_documents_from_folder(folder_path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Load all text files from the specified folder.
    
    Args:
        folder_path: Path to the folder containing text files
        
    Returns:
        Tuple of (documents list, metadata list)
        
    Raises:
        FileNotFoundError: If folder doesn't exist or contains no .txt files
    """
    documents = []
    metadata = []
    
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder '{folder_path}' not found!")
    
    txt_files = list(folder_path.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in '{folder_path}' folder!")
    
    print(f"Found {len(txt_files)} text files. Loading...")
    
    for file_path in txt_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # Only add non-empty files
                    documents.append(content)
                    metadata.append({"source_file": file_path.name})
        except Exception as e:
            print(f"Error loading {file_path.name}: {e}")
            continue
    
    print(f"Successfully loaded {len(documents)} documents")
    return documents, metadata


def calculate_files_hash(folder_path: Path) -> Optional[str]:
    """
    Calculate MD5 hash of all source files to detect changes.
    
    Args:
        folder_path: Path to the folder containing text files
        
    Returns:
        MD5 hash string if files exist, None otherwise
    """
    if not folder_path.exists():
        return None
    
    txt_files = sorted(folder_path.glob("*.txt"))
    file_hashes = []
    
    for file_path in txt_files:
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                file_hashes.append(f"{file_path.name}:{file_hash}")
        except Exception:
            continue
    
    if not file_hashes:
        return None
    
    return hashlib.md5("|".join(file_hashes).encode()).hexdigest()

