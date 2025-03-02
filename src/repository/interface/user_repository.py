from typing import List, Optional, Union

from repository.interface.base_repository import BaseRepository
from domain.user import User


class IUserRepository(BaseRepository):
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자를 조회
        """
        pass

    def get_by_tenant_id(self, tenant_id: str) -> List[User]:
        """
        테넌트 ID로 사용자 목록을 조회합니다.
        """
        pass
    
    def get_admin_users(self) -> List[User]:
        """
        admin 사용자 조회
        """
        pass
    
    def exists_by_email(self, email: str) -> bool:
        """
        해당 이메일의 사용자가 존재하는지 확인합니다.
        """
        pass