"""Pydantic models for the Virtual Fitness Coach application."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Model for incoming chat messages."""
    message: str


class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str


class ChatHistoryItem(BaseModel):
    """Model for chat history items."""
    role: str
    content: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    """Model for chat history response."""
    history: List[ChatHistoryItem]


class ClearHistoryResponse(BaseModel):
    """Model for clear history response."""
    message: str
