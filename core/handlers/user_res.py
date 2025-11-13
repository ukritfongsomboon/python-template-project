from beartype import beartype
from typing import Any, Dict
from fastapi import HTTPException
from core.services.user_srv import UserService
from core.models.srv_global import ResponseModel


class userHandler:
    """Handler (Adapter) for User HTTP endpoints"""

    @beartype
    def __init__(self, userService: UserService):
        """Initialize userHandler with UserService dependency

        Args:
            userService: UserService instance for handling business logic
        """
        self.userService = userService

    @beartype
    def get_all_users(self) -> ResponseModel:
        """Handle GET /users request

        Returns:
            ResponseModel: Array of all users or error message

        Raises:
            BeartypeCallHintParamViolation: If return type is not ResponseModel
        """
        return self.userService.getAllUser()

    @beartype
    def get_user_response(self) -> Dict[str, Any]:
        """Prepare user response for HTTP response

        Returns:
            Dict: HTTP response format ready to be serialized to JSON
        """
        response = self.userService.getAllUser()

        return {
            "status": response.status,
            "code": response.code,
            "message": response.message,
            "data": [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                }
                for user in response.data
            ]
            if response.status
            else [],
        }

    async def list_users_handler(self) -> Dict[str, Any]:
        """FastAPI endpoint handler for GET /api/v1/users

        Returns:
            Dict: Response with status, code, message and user data

        Raises:
            HTTPException: If service returns status=False with code 500
        """
        response = self.get_user_response()

        # Check if there was an error
        if not response.get("status") and response.get("code") == 500:
            raise HTTPException(
                status_code=response.get("code", 500),
                detail=response.get("message", "Internal server error"),
            )

        return response

    async def list_users_with_filter_handler(
        self, skip: int = 0, limit: int = 10
    ) -> Dict[str, Any]:
        """FastAPI endpoint handler for GET /api/v1/users/filtered with pagination

        Args:
            skip: Number of users to skip (default 0)
            limit: Maximum number of users to return (default 10, max 100)

        Returns:
            Dict: Response with filtered users and pagination info

        Raises:
            HTTPException: If service returns error
        """
        response = self.get_user_response()

        if not response.get("status"):
            raise HTTPException(
                status_code=response.get("code", 500),
                detail=response.get("message", "Failed to fetch users"),
            )

        # Apply pagination
        all_users = response.get("data", [])
        paginated_users = all_users[skip : skip + limit]

        return {
            "status": True,
            "code": 200,
            "message": "Users retrieved successfully with pagination",
            "data": paginated_users,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": len(all_users),
                "returned": len(paginated_users),
            },
        }
