from beartype import beartype
from typing import Any, Dict
from fastapi import HTTPException
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
