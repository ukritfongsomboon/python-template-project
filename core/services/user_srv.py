from beartype import beartype
import core.services.user as userService
from core.repositories.jsonplaceholder import jsonplaceHolderRepository
from core.models.srv_user import User
from core.models.srv_global import ResponseModel


class UserService(userService.userService):
    """Service implementation สำหรับ User"""

    @beartype
    def __init__(
        self,
        userRepo: jsonplaceHolderRepository,
    ):
        """Initialize UserService with repository dependency

        Args:
            userRepo: JSONPlaceholder repository for fetching user data
        """
        self.userRepo = userRepo

    @beartype
    def getAllUser(self) -> ResponseModel:
        """ดึงข้อมูลผู้ใช้ทั้งหมดและคืนค่าเป็น ResponseModel

        Returns:
            ResponseModel: ข้อมูลผู้ใช้ทั้งหมดหรือข้อความ error

        Raises:
            BeartypeCallHintParamViolation: ถ้าคืนค่าไม่ใช่ ResponseModel
        """
        try:
            # ดึงข้อมูลผู้ใช้จาก repository
            repo_users = self.userRepo.get_users()

            # ตรวจสอบว่าได้ข้อมูลหรือไม่
            if not repo_users:
                return ResponseModel(
                    status=False,
                    code=404,
                    message="ไม่พบข้อมูลผู้ใช้",
                    data=[],
                )

            # Map repository-level User models to service-level User models
            service_users = []
            for repo_user in repo_users:
                service_user = User(
                    id=repo_user.id,
                    name=repo_user.name,
                    username=repo_user.username,
                    email=repo_user.email,
                )
                service_users.append(service_user)

            return ResponseModel(
                status=True,
                code=200,
                message="ดึงข้อมูลผู้ใช้สำเร็จ",
                data=service_users,
            )

        except Exception as e:
            print(f"Error fetching users in service: {e}")
            return ResponseModel(
                status=False,
                code=500,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                data=[],
            )
