from typing import List, Optional, Union

from repository.interface.base_repository import BaseRepository
from domain.project import Project, ProjectMember


class IProjectRepository(BaseRepository[Project]):
    
    def get_by_name(self, name: str) -> Optional[Project]:
        """
        프로젝트 이름으로 프로젝트를 조회합니다.
        """
        pass
    
    def get_by_tenant_id(self, tenant_id: int) -> List[Project]:
        """
        테넌트 ID로 프로젝트 목록을 조회합니다.
        """
        pass
    
    def get_by_owner_id(self, owner_id: int) -> List[Project]:
        """
        소유자 ID로 프로젝트 목록을 조회합니다.
        """
        pass
    
    def get_by_user_id(self, user_id: int) -> List[Project]:
        """
        사용자 ID로 사용자가 속한 프로젝트 목록을 조회합니다.
        """
        pass


class IProjectMemberRepository(BaseRepository[ProjectMember]):
    
    def get_by_project_id(self, project_id: int) -> List[ProjectMember]:
        """
        프로젝트 ID로 프로젝트 멤버 목록을 조회합니다.
        """
        pass
    
    def get_by_user_id(self, user_id: int) -> List[ProjectMember]:
        """
        사용자 ID로 프로젝트 멤버 목록을 조회합니다.
        """
        pass
    
    def get_by_role(self, role: str) -> List[ProjectMember]:
        """
        역할로 프로젝트 멤버 목록을 조회합니다.
        """
        pass