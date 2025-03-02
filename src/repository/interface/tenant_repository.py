from typing import List, Optional

from repository.interface.base_repository import BaseRepository
from domain.tenant import Tenant


class ITenantRepository(BaseRepository[Tenant]):
    
    def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        테넌트 이름으로 테넌트를 조회합니다.
        """
        pass
    
    def exists_by_name(self, name: str) -> bool:
        """
        해당 이름의 테넌트가 존재하는지 확인합니다.
        """
        pass
