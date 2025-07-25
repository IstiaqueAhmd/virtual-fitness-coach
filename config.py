"""Configuration settings for the Virtual Fitness Coach application."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fitness_coach")

# Application Configuration
HOST = os.getenv("HOST", "127.0.0.2")
PORT = int(os.getenv("PORT", 8000))

# Hardcoded user ID for now
USER_ID = 1

# Validation
if not GEMINI_API_KEY:
    raise ValueError("API key for Gemini is missing. Please set the GEMINI_API_KEY in the .env file.")
