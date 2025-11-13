from abc import ABC, abstractmethod
from typing import List
from core.models.repo_jsonplacehodel import User


class jsonplaceHolderRepository(ABC):
    """Interface (Port) สำหรับ Repository ของ JsonplaceHolderAPI"""

    @abstractmethod
    def get_users(self) -> List[User]:
        """ดึงข้อมูลผู้ใช้ทั้งหมด"""
        pass
