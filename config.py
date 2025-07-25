"""Configuration settings for the Virtual Fitness Coach application."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys and External Services
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fitness_coach")

# Application Configuration
USER_ID = 1  # Hardcoded user ID for now
DEFAULT_CHAT_HISTORY_LIMIT = 10
MAX_CHAT_HISTORY_LIMIT = 50

# Server Configuration
HOST = "127.0.0.2"
PORT = 8000

# Validate required configuration
if not GEMINI_API_KEY:
    raise ValueError("API key for Gemini is missing. Please set the GEMINI_API_KEY in the .env file.")
