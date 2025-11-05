from abc import ABC, abstractmethod
from typing import Optional
from core.models.repo_jsonplacehodel import User


class jsonplaceHolderRepository(ABC):
    """Interface (Port) สำหรับ Repository ของ JsonplaceHolderAPI"""

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """ดึงข้อมูลผู้ใช้ตาม ID"""
        pass
