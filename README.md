# Virtual Fitness Coach Chat

A modular FastAPI-based chatbot that provides personalized fitness advice using Google's Gemini AI, with chat history persistence in MongoDB.

## Project Structure

```
virtual-fitness-coach/
├── app.py              # Main FastAPI application entry point
├── config.py           # Configuration settings and environment variables
├── models.py           # Pydantic models for request/response validation
├── database.py         # MongoDB database operations
├── ai_service.py       # AI service for generating responses
├── routes.py           # API route definitions
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── start_chat.bat      # Windows batch file to start the application
├── .env               # Environment variables (create this file)
└── static/
    └── index.html      # Frontend chat interface
```

## Modules Overview

### `config.py`
- Manages all configuration settings
- Loads environment variables
- Validates required API keys

### `models.py`
- Defines Pydantic models for data validation
- Request/response schemas
- Type safety for API endpoints

### `database.py`
- MongoDB connection and operations
- Chat history persistence
- Database abstraction layer

### `ai_service.py`
- Google Gemini AI integration
- Response generation logic
- Context building for conversations

### `routes.py`
- API endpoint definitions
- Request handling logic
- Error management

### `utils.py`
- Common utility functions
- Data formatting helpers
- Reusable components

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your configuration:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=fitness_coach
   HOST=127.0.0.2
   PORT=8000
   ```

3. Start the application:
   ```bash
   python app.py
   ```
   Or use the provided batch file on Windows:
   ```bash
   start_chat.bat
   ```

## Features

- ✅ Modular architecture with separation of concerns
- ✅ MongoDB integration for chat history persistence
- ✅ Google Gemini AI for fitness coaching responses
- ✅ Real-time chat interface with message history
- ✅ Type safety with Pydantic models
- ✅ Proper error handling and logging
- ✅ Environment-based configuration
- ✅ Clean shutdown handling

## API Endpoints

- `GET /` - Serve the chat interface
- `POST /chat` - Send a message to the fitness coach
- `GET /chat/history` - Retrieve chat history
- `DELETE /chat/history` - Clear chat history

## Development

The modular structure makes it easy to:
- Add new features by extending specific modules
- Test individual components in isolation
- Maintain and update code with minimal impact
- Scale the application as needed
