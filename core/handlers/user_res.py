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

    async def list_users_handler(self) -> Dict[str, Any]:
        """FastAPI endpoint handler for GET /api/v1/users

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

        Returns:
            Dict: Response with status, code, message and user data

        Raises:
            HTTPException: If service returns status=False with code 500
        """
        # Get response from service
        service_response = self.userService.getAllUser()

        # Format response
        response = {
            "status": service_response.status,
            "code": service_response.code,
            "message": service_response.message,
            "data": [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                }
                for user in service_response.data
            ]
            if service_response.status
            else [],
        }

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

        Args:
            skip: Number of users to skip (default 0)
            limit: Maximum number of users to return (default 10, max 100)

        Returns:
            Dict: Response with filtered users and pagination info

        Raises:
            HTTPException: If service returns error
        """
        # Get response from service
        service_response = self.userService.getAllUser()

        # Format response
        response = {
            "status": service_response.status,
            "code": service_response.code,
            "message": service_response.message,
            "data": [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                }
                for user in service_response.data
            ]
            if service_response.status
            else [],
        }

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
