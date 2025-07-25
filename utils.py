"""Utility functions for the Virtual Fitness Coach application."""

from datetime import datetime
from typing import Any, Dict


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_message(message: str) -> str:
    """Sanitize user input message."""
    # Remove excessive whitespace and limit length
    return message.strip()[:1000]  # Limit to 1000 characters


def create_error_response(error_message: str) -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        "error": True,
        "message": error_message,
        "timestamp": datetime.now().isoformat()
    }


def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create a standardized success response."""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
