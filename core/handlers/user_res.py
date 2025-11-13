from beartype import beartype
from typing import Any, Dict
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from core.services.user_srv import UserService
from core.models.srv_global import ResponseModel


class userHandler:
    """Handler (Adapter) *3+#1 User HTTP endpoints"""

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
            BeartypeCallHintParamViolation: I27H2D!HC
H ResponseModel
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

    @beartype
    def list_users_handler(self) -> JSONResponse:
        """FastAPI endpoint handler for GET /api/users

        Returns:
            JSONResponse: JSON response with status, code, message and user data

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

        return JSONResponse(
            status_code=response.get("code", 200),
            content=response,
        )

    @beartype
    def list_users_with_filter_handler(
        self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)
    ) -> JSONResponse:
        """FastAPI endpoint handler for GET /api/users/filtered with pagination

        Args:
            skip: Number of users to skip (default 0)
            limit: Maximum number of users to return (default 10, max 100)

        Returns:
            JSONResponse: JSON response with filtered users and pagination info

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

        return JSONResponse(
            status_code=200,
            content={
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
            },
        )
