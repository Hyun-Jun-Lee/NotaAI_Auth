from typing import List, Optional

from domain.project import Project, ProjectMember
from repository.interface.project_repository import IProjectRepository, IProjectMemberRepository
from exception.domain import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException,
    ProjectMemberNotFoundException,
    ProjectMemberAlreadyExistsException,
    InvalidRoleException
)


class ProjectService:
    
    def __init__(self, project_repository: IProjectRepository, project_member_repository: IProjectMemberRepository):
        self.project_repository = project_repository
        self.project_member_repository = project_member_repository
    
    async def create_project(self, name: str, description: str, owner_id: int, tenant_id: int) -> Project:
        """
        새로운 프로젝트를 생성합니다.
        """
        if await self.project_repository.get_by_name(name):
            raise ProjectAlreadyExistsException(name)

        project = Project.create(name=name, description=description, owner_id=owner_id, tenant_id=tenant_id)
        return await self.project_repository.save(project)
    
    async def get_project_by_id(self, project_id: int) -> Project:
        """
        ID로 프로젝트를 조회합니다.
        """
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(str(project_id))
        return project
    
    async def get_project_by_name(self, name: str) -> Optional[Project]:
        """
        이름으로 프로젝트를 조회합니다.
        """
        return await self.project_repository.get_by_name(name)
    
    async def get_projects_by_tenant(self, tenant_id: int) -> List[Project]:
        """
        테넌트 ID로 프로젝트 목록을 조회합니다.
        """
        return await self.project_repository.get_by_tenant_id(tenant_id)
    
    async def get_projects_by_owner(self, owner_id: int) -> List[Project]:
        """
        소유자 ID로 프로젝트 목록을 조회합니다.
        """
        return await self.project_repository.get_by_owner_id(owner_id)
    
    async def get_projects_by_user(self, user_id: int) -> List[Project]:
        """
        사용자 ID로 사용자가 속한 프로젝트 목록을 조회합니다.
        """
        return await self.project_repository.get_by_user_id(user_id)
    
    async def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None, user_id: Optional[int] = None) -> Project:
        """
        프로젝트 정보를 업데이트합니다.
        """
        project = await self.get_project_by_id(project_id)
        
        project.update(name=name, description=description)
        return await self.project_repository.save(project)
    
    async def delete_project(self, project_id: int) -> bool:
        """
        프로젝트를 삭제합니다.
        """
        if not await self.project_repository.exists(project_id):
            raise ProjectNotFoundException(str(project_id))
        
        return await self.project_repository.delete(project_id)
    
    async def invite_user_to_project(self, project_id: int, user_id: int, role: str, invited_by: int) -> ProjectMember:
        """
        프로젝트에 사용자를 초대합니다.
        """
        project = await self.get_project_by_id(project_id)
        
        members = await self.project_member_repository.get_by_project_id(project_id)
        for member in members:
            if member.user_id == user_id:
                raise ProjectMemberAlreadyExistsException(str(user_id), str(project_id))
        
        project_member = ProjectMember.create(
            project_id=project_id,
            user_id=user_id,
            role=role,
            invited_by=invited_by
        )
        
        return await self.project_member_repository.save(project_member)
    
    async def get_project_members(self, project_id: int) -> List[ProjectMember]:
        """
        프로젝트 멤버 목록을 조회합니다.
        """
        if not await self.project_repository.exists(project_id):
            raise ProjectNotFoundException(str(project_id))
        
        return await self.project_member_repository.get_by_project_id(project_id)
    
    async def get_user_memberships(self, user_id: int) -> List[ProjectMember]:
        """
        사용자의 프로젝트 멤버십 목록을 조회합니다.
        """
        return await self.project_member_repository.get_by_user_id(user_id)
    
    async def change_member_role(self, member_id: int, new_role: str) -> ProjectMember:
        """
        프로젝트 멤버의 역할을 변경합니다.
        """
        member = await self.project_member_repository.get_by_id(member_id)
        if not member:
            raise ProjectMemberNotFoundException(member_id=str(member_id))
        
        member.change_role(new_role)
        return await self.project_member_repository.save(member)
    
    async def remove_member_from_project(self, member_id: int) -> bool:
        """
        프로젝트에서 멤버를 제거합니다.
        """
        member = await self.project_member_repository.get_by_id(member_id)
        if not member:
            raise ProjectMemberNotFoundException(member_id=str(member_id))
        
        return await self.project_member_repository.delete(member_id)