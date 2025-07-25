"""API routes for the Virtual Fitness Coach application."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List

from models import ChatMessage, ChatResponse, ChatHistoryResponse, ClearHistoryResponse
from database import get_database_manager
from ai_service import get_ai_service
from health_agent import HealthAgent
from config import USER_ID, DEFAULT_CHAT_HISTORY_LIMIT, MAX_CHAT_HISTORY_LIMIT
from utils import sanitize_message

# Create router
router = APIRouter()

# Initialize health agent
health_agent = HealthAgent(get_ai_service())


@router.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the chat interface."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat interface not found")


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Handle chat messages."""
    try:
        # Sanitize input
        sanitized_message = sanitize_message(message.message)
        if not sanitized_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        db_manager = await get_database_manager()
        
        # Save user message to MongoDB
        await db_manager.save_message(USER_ID, "user", sanitized_message)
        
        # Get recent chat history for context
        recent_messages = await db_manager.get_chat_history(USER_ID, DEFAULT_CHAT_HISTORY_LIMIT)
        
        # Generate response using health agent
        ai_response = await health_agent.generate_health_response(sanitized_message, recent_messages)
        
        # Save AI response to MongoDB
        await db_manager.save_message(USER_ID, "assistant", ai_response)
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history():
    """Get chat history from MongoDB."""
    try:
        db_manager = await get_database_manager()
        messages = await db_manager.get_chat_history(USER_ID, MAX_CHAT_HISTORY_LIMIT)
        
        # Convert MongoDB documents to the expected format
        history = [
            {
                "role": msg["role"], 
                "content": msg["content"], 
                "timestamp": msg["timestamp"]
            } 
            for msg in messages
        ]
        
        return ChatHistoryResponse(history=history)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")


@router.delete("/chat/history", response_model=ClearHistoryResponse)
async def clear_chat_history():
    """Clear chat history from MongoDB."""
    try:
        db_manager = await get_database_manager()
        deleted_count = await db_manager.clear_chat_history(USER_ID)
        
        return ClearHistoryResponse(
            message=f"Chat history cleared. Deleted {deleted_count} messages."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")
