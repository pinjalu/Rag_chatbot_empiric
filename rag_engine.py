"""
RAG (Retrieval-Augmented Generation) Engine
"""

import numpy as np
import google.generativeai as genai
from typing import List, Dict, Tuple

from config import (
    GEMINI_MODEL_NAME, TOP_K_RESULTS, CONTEXT_RELEVANCE_THRESHOLD,
    CONVERSATION_CONTEXT_WINDOW, TEMPERATURE, TOP_P, TOP_K, MAX_OUTPUT_TOKENS,
    HELPFUL_CONTACTS
)
from response_processor import make_response_natural


class RAGEngine:
    """Handles RAG query processing and response generation."""
    
    def __init__(self, embedding_model, gemini_model):
        """
        Initialize RAG Engine.
        
        Args:
            embedding_model: SentenceTransformer model for embeddings
            gemini_model: Gemini model for generation
        """
        self.embedding_model = embedding_model
        self.gemini_model = gemini_model
        self.conversation_history = []
    
    def _build_system_instruction(self) -> str:
        """Build system instruction for Gemini."""
        return """You are a friendly and helpful AI assistant for Empiric Infotech. 
Answer questions naturally and conversationally based on the provided context from the knowledge base.

CRITICAL RESPONSE FORMATTING RULES:
- ALWAYS format answers as bullet points (•) when listing items, features, or information
- Keep answers CONCISE and ENGAGING - avoid long boring paragraphs
- Use 2-5 bullet points maximum for most answers
- Add relevant emojis INLINE with text (not on separate lines) - 1-2 per response:
  * Use 🚀 for services/features (place right before the text, same line)
  * Use 💼 for business/company info (inline with text)
  * Use 👥 for team/people (inline with text)
  * Use ✨ for highlights/benefits (inline with text)
  * Use 📞 for contact info (inline with phone numbers)
  * Use 💡 for tips/suggestions (inline with text)
  * Use 😊 for friendly greetings
- NEVER put emojis on separate lines - always keep them with their text on the same line
- Make responses SHORT, POINT-WISE, and FUN to read - people should enjoy chatting!
- Break long information into digestible bullet points
- Start with friendly greeting when appropriate (like "Absolutely! 😊" or "Sure thing! ✨")
- Keep it conversational and engaging, not robotic or boring

IMPORTANT GUIDELINES FOR UNKNOWN ANSWERS:
- If the answer is not in the context, respond naturally and helpfully
- NEVER use phrases like:
  * "I'm sorry, but the provided context does not contain information..."
  * "The provided context does not contain..."
  * "I cannot find information about..."
- Instead, use natural, conversational phrases like:
  * "I don't have that specific detail, but I can help you find out... 💡"
  * "That's a great question! While I'm not certain about that, here's what I know..."
  * "Let me help you with that. For accurate info, you can..."
- Always provide helpful alternatives with contact info when needed
- Be warm, conversational, and genuinely helpful - never robotic or boring
- Keep responses SHORT, POINT-WISE, and ENGAGING"""
    
    def _build_conversation_context(self) -> str:
        """Build conversation context from history."""
        if not self.conversation_history:
            return ""
        
        context = "\n\nPrevious conversation:\n"
        for entry in self.conversation_history[-CONVERSATION_CONTEXT_WINDOW:]:
            context += f"User: {entry['question']}\n"
            context += f"Assistant: {entry['answer']}\n\n"
        
        return context
    
    def _retrieve_context(
        self, 
        question: str, 
        index, 
        all_chunks: List[str], 
        chunk_metadata: List[Dict[str, str]],
        top_k: int = TOP_K_RESULTS
    ) -> Tuple[str, float]:
        """
        Retrieve relevant context from vector store.
        
        Args:
            question: User's question
            index: FAISS index
            all_chunks: List of all text chunks
            chunk_metadata: List of chunk metadata
            top_k: Number of results to retrieve
            
        Returns:
            Tuple of (context string, average distance)
        """
        # Embed the question
        q_emb = self.embedding_model.encode([question], convert_to_numpy=True)
        
        # Retrieve top-k relevant chunks from FAISS
        distances, indices = index.search(q_emb, top_k)
        
        # Get the relevant chunks
        relevant_chunks = [all_chunks[i] for i in indices[0]]
        relevant_sources = [chunk_metadata[i]["source_file"] for i in indices[0]]
        
        # Combine chunks into context
        context = "\n\n---\n\n".join([
            f"[Source: {source}]\n{chunk}" 
            for chunk, source in zip(relevant_chunks, relevant_sources)
        ])
        
        # Calculate average distance
        avg_distance = np.mean(distances[0]) if len(distances[0]) > 0 else float('inf')
        
        return context, avg_distance
    
    def ask(
        self, 
        question: str, 
        index, 
        all_chunks: List[str], 
        chunk_metadata: List[Dict[str, str]]
    ) -> str:
        """
        Ask a question using RAG (Retrieval-Augmented Generation).
        
        Args:
            question: User's question
            index: FAISS index
            all_chunks: List of all text chunks
            chunk_metadata: List of chunk metadata
            
        Returns:
            Generated answer
        """
        # Retrieve context
        context, avg_distance = self._retrieve_context(
            question, index, all_chunks, chunk_metadata
        )
        
        # Build prompts
        system_instruction = self._build_system_instruction()
        conversation_context = self._build_conversation_context()
        
        # Add note about context relevance if needed
        context_relevance_note = ""
        if avg_distance > CONTEXT_RELEVANCE_THRESHOLD:
            context_relevance_note = (
                "\n\nNote: The retrieved context may not be highly relevant to this question. "
                "Provide a helpful response and suggest alternative ways to get the information."
            )
        
        # Create the full prompt
        full_prompt = f"""{system_instruction}

{conversation_context}

Context from knowledge base:
{context}
{context_relevance_note}

User Question: {question}

Please provide a natural, conversational, and helpful answer. If the information isn't in the context, respond naturally and suggest how they can get the information (like contacting HR at +91 6355 158315 or hr@empiricinfotech.com for job-related questions)."""
        
        try:
            # Generate response using Gemini
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    top_k=TOP_K,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                )
            )
            
            answer = response.text
            
            # Post-process to make responses more natural
            answer = make_response_natural(answer, question)
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            # Keep only last N exchanges to manage memory
            from config import CONVERSATION_HISTORY_LIMIT
            if len(self.conversation_history) > CONVERSATION_HISTORY_LIMIT:
                self.conversation_history.pop(0)
            
            return answer
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()

