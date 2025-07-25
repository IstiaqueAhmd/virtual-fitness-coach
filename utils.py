"""Utility functions for the Virtual Fitness Coach application."""

from datetime import datetime, UTC
from typing import Dict, Any


def format_timestamp(timestamp: datetime) -> str:
    """Format a timestamp for display."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def sanitize_message(message: str) -> str:
    """Sanitize user input message."""
    return message.strip()[:1000]


def create_response_dict(success: bool, message: str, data: Any = None) -> Dict:
    """Create a standardized response dictionary."""
    response = {
        "success": success,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def get_current_utc_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(UTC)
