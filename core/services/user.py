from abc import ABC, abstractmethod
from typing import List
from core.models.srv_user import User
from core.models.srv_global import ResponseModel


class userService(ABC):
    """Interface (Port) สำหรับ Repository ของ JsonplaceHolderAPI"""

    @abstractmethod
    def getAllUser(self) -> ResponseModel:
        """ดึงข้อมูลผู้ใช้ทั้งหมด"""
        pass
