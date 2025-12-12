"""
Text processing and chunking utilities
"""

from typing import List, Tuple, Dict


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Number of words per chunk
        overlap: Number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
        if start >= len(words):
            break
    
    return chunks


def process_documents_for_chunking(
    documents: List[str], 
    metadata: List[Dict[str, str]],
    chunk_size: int = 200,
    overlap: int = 50
) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Process documents into chunks with metadata.
    
    Args:
        documents: List of document texts
        metadata: List of metadata dictionaries
        chunk_size: Number of words per chunk
        overlap: Number of words to overlap between chunks
        
    Returns:
        Tuple of (all_chunks, chunk_metadata)
    """
    all_chunks = []
    chunk_metadata = []
    
    for doc, meta in zip(documents, metadata):
        chunks = chunk_text(doc, chunk_size, overlap)
        all_chunks.extend(chunks)
        # Associate each chunk with its source file
        chunk_metadata.extend([meta] * len(chunks))
    
    return all_chunks, chunk_metadata

