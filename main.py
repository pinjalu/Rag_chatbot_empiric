"""
Main entry point for the RAG Chatbot
"""

import time
from chatbot import Chatbot
from config import DATA_FOLDER


def main():
    """Main function to run the chatbot."""
    print("=" * 60)
    print("RAG Chatbot with Gemini API")
    print("=" * 60)
    
    try:
        # Initialize chatbot
        chatbot = Chatbot()
        chatbot.initialize(DATA_FOLDER)
        
        print("\n" + "=" * 60)
        print("Chatbot is ready! Type your questions below.")
        print("Commands: 'exit' or 'quit' to end, 'clear' to clear history")
        print("=" * 60 + "\n")
        
        # Chat loop
        while True:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit']:
                print("\nGoodbye! 👋")
                break
            
            if question.lower() == 'clear':
                chatbot.clear_history()
                print("Conversation history cleared.\n")
                continue
            
            print("\nThinking...")
            start_time = time.time()
            answer = chatbot.ask(question)
            elapsed_time = time.time() - start_time
            
            print(f"\nAssistant: {answer}")
            print(f"\n[Response time: {elapsed_time:.2f}s]\n")
            print("-" * 60 + "\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

