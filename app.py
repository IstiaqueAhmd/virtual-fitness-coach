import os
from typing import List, Dict
from datetime import datetime, UTC
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fitness_coach")

if not GEMINI_API_KEY:
    raise ValueError("API key for Gemini is missing. Please set the GEMINI_API_KEY in the .env file.")

app = FastAPI(title="Virtual Fitness Coach Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# MongoDB setup
mongo_client = AsyncIOMotorClient(MONGODB_URL)
database = mongo_client[DATABASE_NAME]
chat_collection = database["chat_history"]

client = genai.Client()

# Hardcoded user ID for now
USER_ID = 1

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Helper functions for MongoDB operations
async def save_message_to_db(user_id: int, role: str, content: str):
    """Save a message to MongoDB"""
    message_doc = {
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now(UTC)
    }
    await chat_collection.insert_one(message_doc)

async def get_chat_history_from_db(user_id: int, limit: int = 10):
    """Get recent chat history from MongoDB"""
    cursor = chat_collection.find(
        {"user_id": user_id}
    ).sort("timestamp", DESCENDING).limit(limit)
    
    messages = await cursor.to_list(length=limit)
    # Reverse to get chronological order
    messages.reverse()
    return messages

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the chat interface"""
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Handle chat messages"""
    try:
        # Save user message to MongoDB
        await save_message_to_db(USER_ID, "user", message.message)
        
        # Get recent chat history for context
        recent_messages = await get_chat_history_from_db(USER_ID, 10)
        
        # Create context from chat history for better conversation flow
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
        
        # Generate response with fitness coach context
        prompt = f"""You are a helpful virtual fitness coach. Provide encouraging, informative, and personalized fitness advice.
        
Previous conversation:
{context}

Please respond to the user's latest message in a friendly and supportive manner."""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        
        ai_response = response.text
        
        # Save AI response to MongoDB
        await save_message_to_db(USER_ID, "assistant", ai_response)
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/chat/history")
async def get_chat_history():
    """Get chat history from MongoDB"""
    try:
        messages = await get_chat_history_from_db(USER_ID, 50)  # Get more messages for history view
        # Convert MongoDB documents to the expected format
        history = [{"role": msg["role"], "content": msg["content"], "timestamp": msg["timestamp"]} for msg in messages]
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

@app.delete("/chat/history")
async def clear_chat_history():
    """Clear chat history from MongoDB"""
    try:
        result = await chat_collection.delete_many({"user_id": USER_ID})
        return {"message": f"Chat history cleared. Deleted {result.deleted_count} messages."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)