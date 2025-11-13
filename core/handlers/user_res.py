from beartype import beartype
from typing import Any, Dict
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
