"""
Virtual Fitness Coach Chat Application

A FastAPI-based chatbot that provides personalized fitness advice using Google's Gemini AI.
Chat history is persisted in MongoDB with a modular architecture.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import router
from database import db_manager
from config import HOST, PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    yield
    # Shutdown
    await db_manager.close_connection()


# Create FastAPI application with lifespan management
app = FastAPI(
    title="Virtual Fitness Coach Chat",
    description="A personalized AI fitness coach with chat history persistence",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)