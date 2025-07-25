# Virtual Fitness Coach

A modular virtual fitness coach application with AI-powered chat functionality.

## Project Structure

```
virtual-fitness-coach/
├── app.py              # Main application entry point
├── config.py           # Configuration and environment variables
├── models.py           # Pydantic models for API requests/responses
├── database.py         # MongoDB operations and database management
├── ai_service.py       # AI/Gemini integration service
├── health_agent.py     # Specialized health and fitness logic
├── routes.py           # API route handlers
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── start_chat.bat      # Windows batch file to start the application
└── static/
    └── index.html      # Frontend chat interface
```

## Modules Overview

### `config.py`
- Environment variable loading
- Configuration constants
- API key validation

### `models.py`
- Pydantic models for request/response validation
- Data structure definitions
- Type safety enforcement

### `database.py`
- MongoDB connection management
- Database operations (save, retrieve, delete messages)
- Async database operations with proper connection handling

### `ai_service.py`
- Gemini AI integration
- Prompt engineering
- Response generation

### `health_agent.py`
- Specialized fitness and health logic
- Message intent analysis
- Context-aware response generation

### `routes.py`
- FastAPI route definitions
- Request handling and validation
- Error handling and response formatting

### `utils.py`
- Helper functions
- Input sanitization
- Response formatting utilities

### `app.py`
- Main application setup
- Middleware configuration
- Application lifecycle management

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **AI-Powered Chat**: Integration with Google's Gemini AI for intelligent responses
- **Persistent Chat History**: MongoDB storage for conversation continuity
- **Health-Focused Responses**: Specialized agent for fitness and health advice
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling throughout the application
- **Async Operations**: Fully asynchronous for better performance

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fitness_coach
```

3. Start the application:
```bash
python app.py
```

Or use the batch file on Windows:
```bash
start_chat.bat
```

## API Endpoints

- `GET /` - Serve the chat interface
- `POST /chat` - Send a message and get AI response
- `GET /chat/history` - Retrieve chat history
- `DELETE /chat/history` - Clear chat history

## Benefits of Modular Structure

1. **Maintainability**: Each module has a single responsibility
2. **Testability**: Individual modules can be tested in isolation
3. **Scalability**: Easy to add new features or modify existing ones
4. **Reusability**: Modules can be reused across different parts of the application
5. **Code Organization**: Clear structure makes the codebase easier to navigate
6. **Separation of Concerns**: Business logic, data access, and API handling are separated
