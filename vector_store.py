"""
Vector store operations: building, saving, and loading
"""

import faiss
import pickle
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List, Dict
from sentence_transformers import SentenceTransformer

from config import (
    INDEX_PATH, CHUNKS_PATH, METADATA_PATH, FILES_HASH_PATH,
    VECTOR_STORE_DIR, CHUNK_SIZE, CHUNK_OVERLAP
)
from document_loader import calculate_files_hash
from text_processor import process_documents_for_chunking


class VectorStore:
    """Manages vector store operations including building, saving, and loading."""
    
    def __init__(self, embedding_model: SentenceTransformer):
        """
        Initialize VectorStore with embedding model.
        
        Args:
            embedding_model: SentenceTransformer model for creating embeddings
        """
        self.embedding_model = embedding_model
    
    def build(
        self, 
        documents: List[str], 
        metadata: List[Dict[str, str]]
    ) -> Tuple[faiss.Index, List[str], List[Dict[str, str]]]:
        """
        Create embeddings and build FAISS index.
        
        Args:
            documents: List of document texts
            metadata: List of metadata dictionaries
            
        Returns:
            Tuple of (FAISS index, chunks, chunk_metadata)
        """
        print("\nChunking documents...")
        all_chunks, chunk_metadata = process_documents_for_chunking(
            documents, metadata, CHUNK_SIZE, CHUNK_OVERLAP
        )
        
        print(f"Total chunks created: {len(all_chunks)}")
        
        print("Creating embeddings (this may take a while)...")
        embeddings = self.embedding_model.encode(
            all_chunks, 
            convert_to_numpy=True, 
            show_progress_bar=True
        )
        print(f"Embeddings shape: {embeddings.shape}")
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        print("Vector store built successfully!")
        return index, all_chunks, chunk_metadata
    
    def save(
        self, 
        index: faiss.Index, 
        chunks: List[str], 
        metadata: List[Dict[str, str]], 
        files_hash: str
    ) -> bool:
        """
        Save FAISS index, chunks, and metadata to disk.
        
        Args:
            index: FAISS index
            chunks: List of text chunks
            metadata: List of chunk metadata
            files_hash: Hash of source files
            
        Returns:
            True if successful, False otherwise
        """
        print("\n💾 Saving vector store to disk...")
        
        try:
            # Save FAISS index
            faiss.write_index(index, str(INDEX_PATH))
            
            # Save chunks and metadata using pickle
            with open(CHUNKS_PATH, "wb") as f:
                pickle.dump(chunks, f)
            
            with open(METADATA_PATH, "wb") as f:
                pickle.dump(metadata, f)
            
            # Save files hash
            with open(FILES_HASH_PATH, "w") as f:
                f.write(files_hash)
            
            print(f"✅ Vector store saved to {VECTOR_STORE_DIR}/")
            return True
        except Exception as e:
            print(f"⚠️  Warning: Could not save vector store: {e}")
            return False
    
    def load(self) -> Optional[Tuple[faiss.Index, List[str], List[Dict[str, str]]]]:
        """
        Load FAISS index, chunks, and metadata from disk.
        
        Returns:
            Tuple of (index, chunks, metadata) if successful, None otherwise
        """
        print("\n📂 Loading vector store from disk...")
        
        try:
            # Load FAISS index
            index = faiss.read_index(str(INDEX_PATH))
            
            # Load chunks and metadata
            with open(CHUNKS_PATH, "rb") as f:
                chunks = pickle.load(f)
            
            with open(METADATA_PATH, "rb") as f:
                metadata = pickle.load(f)
            
            print(f"✅ Vector store loaded! ({len(chunks)} chunks)")
            return index, chunks, metadata
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            return None
    
    def exists(self, folder_path: Path) -> bool:
        """
        Check if saved vector store exists and is up-to-date.
        
        Args:
            folder_path: Path to source data folder
            
        Returns:
            True if vector store exists and is valid, False otherwise
        """
        if not all([
            INDEX_PATH.exists(), 
            CHUNKS_PATH.exists(), 
            METADATA_PATH.exists(), 
            FILES_HASH_PATH.exists()
        ]):
            return False
        
        # Check if source files changed
        current_hash = calculate_files_hash(folder_path)
        if current_hash is None:
            return False
        
        try:
            with open(FILES_HASH_PATH, "r") as f:
                saved_hash = f.read().strip()
            return current_hash == saved_hash
        except Exception:
            return False
    
    def get_or_build(
        self, 
        documents: List[str], 
        metadata: List[Dict[str, str]],
        folder_path: Path
    ) -> Tuple[faiss.Index, List[str], List[Dict[str, str]]]:
        """
        Get vector store - load from disk if exists and up-to-date,
        otherwise build and save it.
        
        Args:
            documents: List of document texts
            metadata: List of metadata dictionaries
            folder_path: Path to source data folder
            
        Returns:
            Tuple of (index, chunks, chunk_metadata)
        """
        # Check if we can load from disk
        if self.exists(folder_path):
            result = self.load()
            if result is not None:
                return result
        
        # Need to build vector store
        print("\n🔨 Building new vector store (this may take a while)...")
        index, chunks, chunk_metadata = self.build(documents, metadata)
        
        # Save to disk for next time
        files_hash = calculate_files_hash(folder_path)
        if files_hash:
            self.save(index, chunks, chunk_metadata, files_hash)
        
        return index, chunks, chunk_metadata

