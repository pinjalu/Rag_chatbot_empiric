# Flask Web Application - RAG Chatbot

## Overview

This is a Flask-based web application for the RAG Chatbot. It provides a beautiful, modern web interface for interacting with the chatbot.

## Features

- ✅ **Modern Web UI**: Beautiful, responsive design
- ✅ **Real-time Chat**: Interactive chat interface
- ✅ **RESTful API**: Clean API endpoints
- ✅ **Session Management**: Maintains conversation history
- ✅ **Error Handling**: Graceful error handling
- ✅ **Mobile Responsive**: Works on all devices

## Installation

1. **Install Flask** (if not already installed):
```bash
pip install flask
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

2. **Set up API key** (if not already done):
   - Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start on: `http://localhost:5000`

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### `GET /`
Renders the main chat interface.

### `POST /api/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What services do you offer?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "We offer various services including..."
}
```

### `POST /api/clear`
Clear conversation history.

**Response:**
```json
{
  "success": true,
  "message": "History cleared"
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "success": true,
  "status": "ready",
  "initialized": true
}
```

## Usage

1. Start the Flask app: `python app.py`
2. Open your browser: `http://localhost:5000`
3. Start chatting!

## Features

- **Real-time Chat**: Send messages and get instant responses
- **Clear History**: Clear conversation history with one click
- **Loading Indicators**: Visual feedback while processing
- **Error Handling**: Graceful error messages
- **Responsive Design**: Works on desktop and mobile

## Customization

### Change Port

Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

### Change UI Colors

Edit `templates/index.html` CSS section to customize colors, fonts, etc.

## Troubleshooting

- **Port already in use**: Change the port in `app.py`
- **Import errors**: Make sure all dependencies are installed
- **Chatbot not responding**: Check that `.env` file has correct API key

## Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up a reverse proxy (Nginx)
3. Use environment variables for configuration
4. Enable HTTPS
5. Set `debug=False` in production

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

