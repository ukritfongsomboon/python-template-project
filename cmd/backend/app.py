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
from pydantic import BaseModel, Field
from typing import List, Optional
from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from core.services.user_srv import UserService
from core.handlers.user_res import userHandler


# Response Models
class UserSchema(BaseModel):
    """User data model"""
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User full name")
    username: str = Field(..., description="User login username")
    email: str = Field(..., description="User email address")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Leanne Graham",
                "username": "Bret",
                "email": "Sincere@april.biz"
            }
        }


class PaginationInfo(BaseModel):
    """Pagination information"""
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items returned")
    total: int = Field(..., description="Total number of items")
    returned: int = Field(..., description="Number of items returned in this response")


class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    status: bool = Field(..., description="Response status (success/failure)")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message or error description")
    data: List[UserSchema] = Field(..., description="Response data")

    class Config:
        json_schema_extra = {
            "example": {
                "status": True,
                "code": 200,
                "message": "Users retrieved successfully",
                "data": [
                    {
                        "id": 1,
                        "name": "Leanne Graham",
                        "username": "Bret",
                        "email": "Sincere@april.biz"
                    }
                ]
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated API response"""
    status: bool = Field(..., description="Response status")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    data: List[UserSchema] = Field(..., description="User data array")
    pagination: PaginationInfo = Field(..., description="Pagination information")

    class Config:
        json_schema_extra = {
            "example": {
                "status": True,
                "code": 200,
                "message": "Users retrieved successfully with pagination",
                "data": [
                    {
                        "id": 1,
                        "name": "Leanne Graham",
                        "username": "Bret",
                        "email": "Sincere@april.biz"
                    }
                ],
                "pagination": {
                    "skip": 0,
                    "limit": 10,
                    "total": 100,
                    "returned": 10
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")


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
            "content": {
                "application/json": {
                    "example": {
                        "status": True,
                        "code": 200,
                        "message": "Users retrieved successfully",
                        "data": [
                            {
                                "id": 1,
                                "name": "Leanne Graham",
                                "username": "Bret",
                                "email": "Sincere@april.biz"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal server error while fetching users"
        }
    }
)
async def get_users():
    """
    Retrieve all users from the JSONPlaceholder API.

    This endpoint fetches a complete list of all available users and returns them
    in a standardized format with status and metadata information.

    **Features:**
    - Returns all users from JSONPlaceholder API
    - Consistent response format with status codes
    - Error handling and informative messages

    **Response Format:**
    - status: Boolean indicating success/failure
    - code: HTTP status code
    - message: Descriptive message
    - data: Array of user objects
    """
    return await userHand.list_users_handler()


@app.get(
    "/api/v1/users/filtered",
    response_model=PaginatedResponse,
    summary="Get Users with Pagination",
    tags=["Users"],
    responses={
        200: {
            "description": "Successfully retrieved paginated users",
            "content": {
                "application/json": {
                    "example": {
                        "status": True,
                        "code": 200,
                        "message": "Users retrieved successfully with pagination",
                        "data": [
                            {
                                "id": 1,
                                "name": "Leanne Graham",
                                "username": "Bret",
                                "email": "Sincere@april.biz"
                            }
                        ],
                        "pagination": {
                            "skip": 0,
                            "limit": 10,
                            "total": 100,
                            "returned": 1
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error while fetching users"
        }
    }
)
async def get_users_filtered(skip: int = 0, limit: int = 10):
    """
    Retrieve users with pagination support.

    This endpoint provides paginated access to the user list, allowing you to
    control how many results are returned and which records to skip.

    **Parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 10, max: 100)

    **Use Cases:**
    - Implement infinite scrolling in frontend applications
    - Reduce memory usage by loading data in chunks
    - Navigate through large datasets efficiently

    **Example Usage:**
    - Get first 10 users: `/api/v1/users/filtered?skip=0&limit=10`
    - Get next 10 users: `/api/v1/users/filtered?skip=10&limit=10`
    """
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
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "message": "API is running"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Check the health and availability of the API.

    This endpoint should be called periodically to ensure the API is running
    and responding to requests. Use this for monitoring and load balancer checks.

    **Response:**
    - status: Always returns "healthy" if endpoint is reachable
    - message: Descriptive message about API status
    """
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
