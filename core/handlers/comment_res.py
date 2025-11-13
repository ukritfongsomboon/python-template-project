from beartype import beartype
from core.handlers.comment import commentHandler
from core.services.comment_srv import CommentService
from core.models.srv_global import ResponseModel


class CommentHandler(commentHandler):
    """Handler (Adapter) implementation for User HTTP endpoints"""

    @beartype
    def __init__(self, commentService: CommentService):
        """Initialize UserHandler with UserService dependency

        Args:
            userService: UserService instance for handling business logic
        """
        self.commentService = commentService

    @beartype
    def get_all_comment(self) -> ResponseModel:
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
        return self.commentService.getAllComments()
