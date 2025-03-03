# src/domain/project.py
from typing import List, Optional
from datetime import datetime

from domain.base import BaseDomain
from domain.permission import ROLE_ACTIONS
from exception.domain import InvalidRoleException

class Project(BaseDomain):
    def __init__(self, id : int = None, name: str = None, description: str = None, owner_id: int = None, tenant_id: int = None, created_at: datetime = None, updated_at: datetime = None):
        super().__init__(id, created_at, updated_at)
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.tenant_id = tenant_id
        self.members : List[ProjectMember] = []

    @classmethod
    def create(cls, name: str, description: str, owner_id: int, tenant_id: int) -> "Project":
        project = cls(name=name, description=description, owner_id=owner_id, tenant_id=tenant_id)
        project.create_timestamp()
        return project
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """프로젝트 정보를 업데이트합니다."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.update_timestamp()

    def invite_user(self, user_id: int, role: str, invited_by: int) -> None:
        """프로젝트에 멤버를 초대합니다.."""
        if role not in ROLE_ACTIONS:
            raise InvalidRoleException(f"Invalid role: {role}. Must be one of {ROLE_ACTIONS}")
        self.members.append(ProjectMember(project_id=self.id, user_id=user_id, role=role, invited_by=invited_by))
        self.update_timestamp()

class ProjectMember(BaseDomain):
    def __init__(self, id : int = None, project_id: int = None, user_id: int = None, 
                 role: str = None, invited_by: int = None, created_at: datetime = None, updated_at: datetime = None):
        super().__init__(id, created_at, updated_at)
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.invited_by = invited_by

    @classmethod
    def create(cls, project_id: int, user_id: int, role: str, invited_by: int) -> "ProjectMember":
        project_member = cls(project_id=project_id, user_id=user_id, role=role, invited_by=invited_by)
        project_member.create_timestamp()
        return project_member

    def change_role(self, new_role: str) -> None:
        """멤버의 역할을 변경합니다."""
        if new_role not in ROLE_ACTIONS:
            raise InvalidRoleException(f"Invalid role: {new_role}. Must be one of {ROLE_ACTIONS}")
        
        self.role = new_role
        self.update_timestamp()