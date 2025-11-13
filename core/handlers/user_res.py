from beartype import beartype
from core.handlers.user import userHandler
from core.services.user_srv import UserService
from core.models.srv_global import ResponseModel


class UserHandler(userHandler):
    """Handler (Adapter) implementation for User HTTP endpoints"""

    @beartype
    def __init__(self, userService: UserService):
        """Initialize UserHandler with UserService dependency

        Args:
            userService: UserService instance for handling business logic
        """
        self.userService = userService

    @beartype
    def get_all_users(self) -> ResponseModel:
        """Retrieve all users from the JSONPlaceholder API

        This endpoint fetches a complete list of all available users and returns them
        in a standardized format with status and metadata information.

        **Features:**
        - Returns all users from JSONPlaceholder API
        - Consistent response format with status codes
        - Error handling and informative messages

        Returns:
            ResponseModel: Response with status, code, message and user data

        Raises:
            Exception: If service returns error
        """
        return self.userService.getAllUser()
