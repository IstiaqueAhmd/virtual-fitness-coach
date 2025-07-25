"""Main application module for the Virtual Fitness Coach."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import get_database_manager
from routes import router
from config import HOST, PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    db_manager = await get_database_manager()
    await db_manager.connect()
    
    yield
    
    # Shutdown
    await db_manager.close()


# Create FastAPI application with lifespan management
app = FastAPI(
    title="Virtual Fitness Coach Chat",
    description="A modular virtual fitness coach application with AI-powered chat",
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

# Include routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)