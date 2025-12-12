"""
Configuration settings for the RAG Chatbot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your .env file or environment variables")

# Model Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# Path Configuration
DATA_FOLDER = Path("Formated_data")
VECTOR_STORE_DIR = Path("vector_store")
VECTOR_STORE_DIR.mkdir(exist_ok=True)

# Vector Store File Paths
INDEX_PATH = VECTOR_STORE_DIR / "faiss_index.bin"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.pkl"
METADATA_PATH = VECTOR_STORE_DIR / "metadata.pkl"
FILES_HASH_PATH = VECTOR_STORE_DIR / "files_hash.txt"

# Text Processing Configuration
CHUNK_SIZE = 200  # Number of words per chunk
CHUNK_OVERLAP = 50  # Number of words to overlap between chunks

# RAG Configuration
TOP_K_RESULTS = 5  # Number of relevant chunks to retrieve
CONTEXT_RELEVANCE_THRESHOLD = 1.5  # Distance threshold for low relevance
CONVERSATION_HISTORY_LIMIT = 10  # Maximum conversation history entries
CONVERSATION_CONTEXT_WINDOW = 3  # Number of previous exchanges to include

# Gemini Generation Configuration
TEMPERATURE = 0.7
TOP_P = 0.95
TOP_K = 40
MAX_OUTPUT_TOKENS = 2048

# Contact Information
HELPFUL_CONTACTS = {
    "hr": {
        "phone": "+91 6355 158315",
        "email": "hr@empiricinfotech.com",
        "whatsapp": "https://wa.me/6355158315",
        "description": "For job applications, employment verification, and career inquiries"
    },
    "business": {
        "phone": "+91 7862 920292",
        "email": "inquire@empiricinfotech.com",
        "description": "For business queries and service inquiries"
    },
    "career_page": "https://empiricinfotech.com/career",
    "contact_form": "https://empiricinfotech.com/contact-us#career_form"
}

