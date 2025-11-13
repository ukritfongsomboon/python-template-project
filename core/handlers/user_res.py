from beartype import beartype
from typing import Any, Dict
from fastapi import HTTPException
from core.services.user_srv import UserService


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
    async def get_all_users(self) -> Dict[str, Any]:
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
            "data": (
                [
                    {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "email": user.email,
                    }
                    for user in service_response.data
                ]
                if service_response.status
                else []
            ),
        }

        # Check if there was an error
        if not response.get("status") and response.get("code") == 500:
            raise HTTPException(
                status_code=response.get("code", 500),
                detail=response.get("message", "Internal server error"),
            )

        return response
