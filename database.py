"""Database operations for the Virtual Fitness Coach application."""

from datetime import datetime, UTC
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING
from config import MONGODB_URL, DATABASE_NAME


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.client = None
        self.database = None
        self.chat_collection = None
    
    async def connect(self):
        """Initialize database connection."""
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.database = self.client[DATABASE_NAME]
        self.chat_collection = self.database["chat_history"]
    
    async def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
    
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
        """Clear chat history for a user from MongoDB."""
        result = await self.chat_collection.delete_many({"user_id": user_id})
        return result.deleted_count


# Global database manager instance
db_manager = DatabaseManager()


async def get_database_manager() -> DatabaseManager:
    """Get the database manager instance."""
    return db_manager
