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
import uvicorn
from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from core.services.user_srv import UserService
from core.handlers.user_res import userHandler
from core.models.api_response import (
    ApiResponse,
    PaginatedResponse,
    HealthResponse,
)


# Repositories
jsonplacehodelRepo = JsonplaceHolderRepository(api_url)

# Services
userSrv = UserService(jsonplacehodelRepo)

# Handlers
userHand = userHandler(userSrv)


app = FastAPI(
    title="User API",
    description="Professional API for managing and retrieving user information from JSONPlaceholder API. Built with FastAPI and Hexagonal Architecture.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
)


# FastAPI endpoints
@app.get(
    "/api/v1/users",
    response_model=ApiResponse,
    summary="Get All Users",
    tags=["Users"],
    responses={
        200: {
            "description": "Successfully retrieved all users",
        },
        500: {
            "description": "Internal server error while fetching users"
        }
    }
)
async def get_users():
    """Get all users from the JSONPlaceholder API."""
    return await userHand.list_users_handler()


@app.get(
    "/api/v1/users/filtered",
    response_model=PaginatedResponse,
    summary="Get Users with Pagination",
    tags=["Users"],
    responses={
        200: {
            "description": "Successfully retrieved paginated users",
        },
        500: {
            "description": "Internal server error while fetching users"
        }
    }
)
async def get_users_filtered(skip: int = 0, limit: int = 10):
    """Get users with pagination support."""
    return await userHand.list_users_with_filter_handler(skip=skip, limit=limit)


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["System"],
    responses={
        200: {
            "description": "API is healthy and operational",
        }
    }
)
async def health_check():
    """Check the health and availability of the API."""
    return {"status": "healthy", "message": "API is running"}


# Application startup
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if debug_mode else "warning",
    )
