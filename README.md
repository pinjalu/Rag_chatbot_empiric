# RAG Chatbot with Gemini API

A production-ready RAG (Retrieval-Augmented Generation) chatbot using Google's Gemini API. The chatbot loads documents from a folder, creates embeddings, and provides intelligent responses based on the knowledge base.

## Features

- ✅ **Fast Startup**: Caches embeddings to disk (build once, use many times)
- ✅ **Natural Responses**: Conversational, non-robotic answers
- ✅ **Smart Caching**: Automatically rebuilds when source files change
- ✅ **Modular Architecture**: Clean, maintainable code structure
- ✅ **Conversation Memory**: Maintains context across interactions

## Project Structure

```
.
├── main.py                 # Entry point
├── chatbot.py              # Main Chatbot class
├── config.py               # Configuration and constants
├── document_loader.py      # Document loading utilities
├── text_processor.py       # Text chunking and processing
├── vector_store.py         # Vector store operations
├── rag_engine.py           # RAG query engine
├── response_processor.py   # Response naturalization
├── requirements.txt        # Dependencies
├── Formated_data/         # Source documents folder
└── vector_store/          # Cached embeddings (auto-generated)
```

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API key:**
   - Create a `.env` file in the project root
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   Get your API key from: https://makersuite.google.com/app/apikey

## Usage

### Basic Usage

```bash
python main.py
```

Or use the backward-compatible file:

```bash
python gemini_rag_chatbot.py
```

### Programmatic Usage

```python
from chatbot import Chatbot
from pathlib import Path

# Initialize chatbot
chatbot = Chatbot()
chatbot.initialize(Path("Formated_data"))

# Ask questions
answer = chatbot.ask("What services do you offer?")
print(answer)

# Clear conversation history
chatbot.clear_history()
```

## Configuration

All configuration is in `config.py`:

- **Models**: Embedding and Gemini model names
- **Paths**: Data folder and vector store locations
- **Chunking**: Chunk size and overlap settings
- **RAG**: Top-K results, context relevance threshold
- **Generation**: Temperature, top-p, max tokens

## How It Works

1. **Document Loading**: Loads all `.txt` files from `Formated_data/`
2. **Text Chunking**: Splits documents into overlapping chunks
3. **Embeddings**: Creates vector embeddings using sentence-transformers
4. **Vector Store**: Uses FAISS for fast similarity search
5. **Caching**: Saves embeddings to disk for fast subsequent loads
6. **Retrieval**: Finds most relevant chunks for each question
7. **Generation**: Uses Gemini API to generate answers

## Performance

- **First Run**: 10-60 seconds (builds embeddings)
- **Subsequent Runs**: 2-5 seconds (loads from cache)
- **Auto-Rebuild**: Detects file changes and rebuilds automatically

## Commands

- Type your questions normally
- Type `exit` or `quit` to end the session
- Type `clear` to clear conversation history

## Module Overview

### `config.py`
Centralized configuration including API keys, model names, paths, and settings.

### `document_loader.py`
Handles loading text files and calculating file hashes for change detection.

### `text_processor.py`
Text chunking utilities for splitting documents into manageable pieces.

### `vector_store.py`
Manages FAISS vector store: building, saving, loading, and validation.

### `rag_engine.py`
Core RAG functionality: retrieval, context building, and response generation.

### `response_processor.py`
Post-processes responses to make them more natural and conversational.

### `chatbot.py`
Main Chatbot class that orchestrates all components.

### `main.py`
Entry point with interactive chat loop.

## Troubleshooting

- **"GEMINI_API_KEY not found"**: Create `.env` file with your API key
- **"No .txt files found"**: Ensure `Formated_data/` contains `.txt` files
- **Import errors**: Run `pip install -r requirements.txt`
- **Slow first response**: Normal - first run downloads embedding model

## License

MIT License

