# src/domain/project.py
from typing import List, Optional
from datetime import datetime
import uuid

from domain.base import BaseDomain
from exception.domain.role_exception import InvalidRoleException

class Project(BaseDomain):
    def __init__(self,name: str = None, description: str = None, 
                 owner_id: str = None, tenant_id: str = None, created_at: datetime = None):
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.tenant_id = tenant_id
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """프로젝트 정보를 업데이트합니다."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()


class ProjectMember(BaseDomain):
    def __init__(self, project_id: str = None, user_id: str = None, 
                 roles: List[str] = None, invited_by: str = None):
        self.project_id = project_id
        self.user_id = user_id
        self.roles = roles or []
        self.invited_by = invited_by

    def change_role(self, new_role: str) -> None:
        """멤버의 역할을 변경합니다."""
        if new_role not in self.ROLES:
            raise InvalidRoleException(f"Invalid role: {new_role}. Must be one of {self.ROLES}")
        
        self.role = new_role
        self.updated_at = datetime.now()