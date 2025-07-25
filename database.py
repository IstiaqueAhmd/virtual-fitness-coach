"""Database operations for chat history management."""

from datetime import datetime, UTC
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING
from config import MONGODB_URL, DATABASE_NAME


class DatabaseManager:
    """Handles all database operations for the fitness coach chat."""
    
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.database = self.client[DATABASE_NAME]
        self.chat_collection = self.database["chat_history"]
    
    async def save_message(self, user_id: int, role: str, content: str) -> None:
        """Save a message to MongoDB."""
        message_doc = {
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now(UTC)
        }
        await self.chat_collection.insert_one(message_doc)
    
    async def get_chat_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get recent chat history from MongoDB."""
        cursor = self.chat_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", DESCENDING).limit(limit)
        
        messages = await cursor.to_list(length=limit)
        # Reverse to get chronological order
        messages.reverse()
        return messages
    
    async def clear_chat_history(self, user_id: int) -> int:
        """Clear chat history from MongoDB and return count of deleted messages."""
        result = await self.chat_collection.delete_many({"user_id": user_id})
        return result.deleted_count
    
    async def close_connection(self):
        """Close the database connection."""
        self.client.close()


# Global database manager instance
db_manager = DatabaseManager()
