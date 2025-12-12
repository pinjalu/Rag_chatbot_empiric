"""
Flask web application for RAG Chatbot
"""

from flask import Flask, render_template, request, jsonify, session
from chatbot import Chatbot
from config import DATA_FOLDER
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize chatbot (will be loaded on first request)
chatbot = None


def get_chatbot():
    """Get or initialize chatbot instance."""
    global chatbot
    if chatbot is None:
        chatbot = Chatbot()
        chatbot.initialize(DATA_FOLDER)
    return chatbot


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.json
        question = data.get('message', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Please provide a message'
            }), 400
        
        # Handle special commands
        if question.lower() in ['exit', 'quit']:
            return jsonify({
                'success': True,
                'response': 'Goodbye! 👋',
                'clear_history': True
            })
        
        if question.lower() == 'clear':
            get_chatbot().clear_history()
            return jsonify({
                'success': True,
                'response': 'Conversation history cleared.',
                'clear_history': True
            })
        
        # Get chatbot and ask question
        bot = get_chatbot()
        response = bot.ask(question)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    try:
        get_chatbot().clear_history()
        return jsonify({
            'success': True,
            'message': 'History cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        bot = get_chatbot()
        return jsonify({
            'success': True,
            'status': 'ready',
            'initialized': bot.index is not None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Initialize chatbot on startup
    print("Initializing chatbot...")
    get_chatbot()
    print("Chatbot ready!")
    
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run Flask app
    app.run(debug=False, host='0.0.0.0', port=port)

