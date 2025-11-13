"""API Response Models for Swagger/OpenAPI Documentation"""

from pydantic import BaseModel, Field
from typing import List


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


class CommentSchema(BaseModel):
    """Comment data model from JSONPlaceholder API"""
    postId: int = Field(..., description="Post ID")
    id: int = Field(..., description="Comment ID")
    name: str = Field(..., description="Comment author name")
    email: str = Field(..., description="Comment author email")
    body: str = Field(..., description="Comment text content")

    class Config:
        json_schema_extra = {
            "example": {
                "postId": 1,
                "id": 1,
                "name": "id labore ex et quam laborum",
                "email": "Eliseo@gardn.biz",
                "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\nquisquam sunt aut facere saepe veniam quis\net sequi qui fugit sunt in. totam sitaque\nmolestiae praesentium quia vero quos aut rerum"
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


class CommentApiResponse(BaseModel):
    """API response wrapper for comments"""
    status: bool = Field(..., description="Response status (success/failure)")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message or error description")
    data: List[CommentSchema] = Field(..., description="Comment data array")

    class Config:
        json_schema_extra = {
            "example": {
                "status": True,
                "code": 200,
                "message": "Comments retrieved successfully",
                "data": [
                    {
                        "postId": 1,
                        "id": 1,
                        "name": "id labore ex et quam laborum",
                        "email": "Eliseo@gardn.biz",
                        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos"
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
