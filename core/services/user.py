from abc import ABC, abstractmethod
from core.models.srv_global import ResponseModel


class userService(ABC):
    """Interface (Port) สำหรับ Repository ของ JsonplaceHolderAPI"""

    @abstractmethod
    def getAllUser(self) -> ResponseModel:
        """ดึงข้อมูลผู้ใช้ทั้งหมด"""
        pass
