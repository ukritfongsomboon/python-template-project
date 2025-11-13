import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Get environment variables
api_url = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
debug_mode = os.getenv("DEBUG", "False").lower() == "true"


# Application setup
from fastapi import FastAPI
from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from core.services.user_srv import UserService
from core.handlers.user_res import userHandler


# Repositories
jsonplacehodelRepo = JsonplaceHolderRepository(api_url)

# Services
userSrv = UserService(jsonplacehodelRepo)

# Handlers
userHand = userHandler(userSrv)


app = FastAPI(title="User API", version="1.0.0")


# FastAPI endpoints
@app.get("/api/users")
async def get_users():
    """Get all users endpoint

    Returns:
        JSONResponse: List of all users with status and metadata
    """
    return userHand.list_users_handler()


@app.get("/api/users/filtered")
async def get_users_filtered(skip: int = 0, limit: int = 10):
    """Get users with pagination and filtering

    Args:
        skip: Number of users to skip (default: 0)
        limit: Maximum number of users to return (default: 10, max: 100)

    Returns:
        JSONResponse: Paginated list of users with pagination info
    """
    return userHand.list_users_with_filter_handler(skip=skip, limit=limit)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint

    Returns:
        dict: Status of the application
    """
    return {"status": "healthy", "message": "API is running"}
