"""API routes for the Virtual Fitness Coach application."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models import ChatMessage, ChatResponse, ChatHistoryResponse, ClearHistoryResponse
from database import db_manager
from ai_service import ai_service
from config import USER_ID

router = APIRouter()


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
        # Save user message to MongoDB
        await db_manager.save_message(USER_ID, "user", message.message)
        
        # Get recent chat history for context
        recent_messages = await db_manager.get_chat_history(USER_ID, 10)
        
        # Generate AI response
        ai_response = await ai_service.generate_response(message.message, recent_messages)
        
        # Save AI response to MongoDB
        await db_manager.save_message(USER_ID, "assistant", ai_response)
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.get("/chat/history")
async def get_chat_history():
    """Get chat history from MongoDB."""
    try:
        messages = await db_manager.get_chat_history(USER_ID, 50)  # Get more messages for history view
        # Convert MongoDB documents to the expected format
        history = [
            {"role": msg["role"], "content": msg["content"], "timestamp": msg["timestamp"]} 
            for msg in messages
        ]
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")


@router.delete("/chat/history")
async def clear_chat_history():
    """Clear chat history from MongoDB."""
    try:
        deleted_count = await db_manager.clear_chat_history(USER_ID)
        return {"message": f"Chat history cleared. Deleted {deleted_count} messages."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")
