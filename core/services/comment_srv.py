from beartype import beartype
from core.services.comment import commentService
from core.repositories.jsonplaceholder import jsonplaceHolderRepository
from core.models.srv_comment import SrvCommentModel
from core.models.srv_global import ResponseModel


class CommentService(commentService):
    """Service implementation สำหรับ User"""

    @beartype
    def __init__(
        self,
        jsonplaceHolderRepo: jsonplaceHolderRepository,
    ):
        """Initialize UserService with repository dependency

        Args:
            userRepo: JSONPlaceholder repository for fetching user data
        """
        self.jsonplaceHolderRepo = jsonplaceHolderRepo

    @beartype
    def getAllComments(self) -> ResponseModel:
        """ดึงข้อมูลผู้ใช้ทั้งหมดและคืนค่าเป็น ResponseModel

        Returns:
            ResponseModel: ข้อมูลผู้ใช้ทั้งหมดหรือข้อความ error

        Raises:
            BeartypeCallHintParamViolation: ถ้าคืนค่าไม่ใช่ ResponseModel
        """
        try:
            # ดึงข้อมูลผู้ใช้จาก repository
            comments = self.jsonplaceHolderRepo.get_comments()

            # ตรวจสอบว่าได้ข้อมูลหรือไม่
            if not comments:
                return ResponseModel(
                    status=False,
                    code=404,
                    message="ไม่พบข้อมูลผู้ใช้",
                    data=[],
                )

            # Map repository-level User models to service-level User models
            result_comments = []
            for comment in comments:
                newComment = SrvCommentModel(
                    postId=comment.postId,
                    id=comment.id,
                    name=comment.name,
                    email=comment.email,
                    body=comment.body,
                )
                result_comments.append(newComment)

            return ResponseModel(
                status=True,
                code=200,
                message="ดึงข้อมูลผู้ใช้สำเร็จ",
                data=result_comments,
            )

        except Exception as e:
            print(f"Error fetching users in service: {e}")
            return ResponseModel(
                status=False,
                code=500,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                data=[],
            )
