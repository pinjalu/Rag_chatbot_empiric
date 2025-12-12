"""
Main Chatbot class that orchestrates all components
"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

from config import (
    GEMINI_API_KEY, EMBEDDING_MODEL_NAME, GEMINI_MODEL_NAME, DATA_FOLDER
)
from document_loader import load_documents_from_folder
from vector_store import VectorStore
from rag_engine import RAGEngine


class Chatbot:
    """Main chatbot class that orchestrates document loading, vector store, and RAG."""
    
    def __init__(self):
        """Initialize the chatbot with models and components."""
        # Configure Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize models
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Embedding model loaded!")
        
        self.gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        
        # Initialize components
        self.vector_store = VectorStore(self.embedding_model)
        self.rag_engine = RAGEngine(self.embedding_model, self.gemini_model)
        
        # Vector store data (will be loaded/created)
        self.index = None
        self.all_chunks = None
        self.chunk_metadata = None
    
    def initialize(self, data_folder: Path = DATA_FOLDER):
        """
        Initialize the chatbot by loading documents and setting up vector store.
        
        Args:
            data_folder: Path to folder containing text files
        """
        # Load documents
        documents, metadata = load_documents_from_folder(data_folder)
        
        # Get or build vector store
        self.index, self.all_chunks, self.chunk_metadata = self.vector_store.get_or_build(
            documents, metadata, data_folder
        )
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the chatbot.
        
        Args:
            question: User's question
            
        Returns:
            Generated answer
        """
        if self.index is None:
            return "Error: Chatbot not initialized. Please call initialize() first."
        
        return self.rag_engine.ask(
            question, 
            self.index, 
            self.all_chunks, 
            self.chunk_metadata
        )
    
    def clear_history(self):
        """Clear conversation history."""
        self.rag_engine.clear_history()

