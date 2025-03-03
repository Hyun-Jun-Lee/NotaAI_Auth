from typing import List, Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.model.project import ProjectModel, ProjectMemberModel
from domain import Project, ProjectMember
from repository.interface.project_repository import IProjectRepository, IProjectMemberRepository


class ProjectPgRepository(IProjectRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, entity: Project) -> Project:
        """
        프로젝트 엔티티를 저장하거나 업데이트합니다.
        """
        project_model = ProjectModel.from_domain(entity)
        
        # upsert
        self.session.add(project_model)
        await self.session.commit()
        await self.session.refresh(project_model)
        
        return project_model.to_domain()
    
    async def delete(self, id: int) -> bool:
        """
        ID로 프로젝트를 삭제합니다.
        """
        project = await self.session.get(ProjectModel, id)
        if not project:
            return False
        
        await self.session.delete(project)
        await self.session.commit()
        return True
    
    async def get_by_id(self, id: int) -> Optional[Project]:
        """
        ID로 프로젝트를 조회합니다.
        """
        project = await self.session.get(ProjectModel, id)
        if not project:
            return None
        return project.to_domain()
    
    async def get_all(self) -> List[Project]:
        """
        모든 프로젝트를 조회합니다.
        """
        result = await self.session.execute(select(ProjectModel))
        projects = result.scalars().all()
        return [project.to_domain() for project in projects]
    
    async def count(self) -> int:
        """
        전체 프로젝트 수를 반환합니다.
        """
        result = await self.session.execute(select(ProjectModel))
        return len(result.scalars().all())
    
    async def exists(self, id: int) -> bool:
        """
        해당 ID의 프로젝트가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(ProjectModel.id == id))
        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def get_by_name(self, name: str) -> Optional[Project]:
        """
        프로젝트 이름으로 프로젝트를 조회합니다.
        """
        stmt = select(ProjectModel).where(ProjectModel.name == name)
        result = await self.session.execute(stmt)
        project = result.scalars().first()
        return project.to_domain() if project else None
    
    async def get_by_tenant_id(self, tenant_id: int) -> List[Project]:
        """
        테넌트 ID로 프로젝트 목록을 조회합니다.
        """
        stmt = select(ProjectModel).where(ProjectModel.tenant_id == tenant_id)
        result = await self.session.execute(stmt)
        projects = result.scalars().all()
        return [project.to_domain() for project in projects]
    
    async def get_by_owner_id(self, owner_id: int) -> List[Project]:
        """
        소유자 ID로 프로젝트 목록을 조회합니다.
        """
        stmt = select(ProjectModel).where(ProjectModel.owner_id == owner_id)
        result = await self.session.execute(stmt)
        projects = result.scalars().all()
        return [project.to_domain() for project in projects]
    
    async def get_by_user_id(self, user_id: int) -> List[Project]:
        """
        사용자 ID로 사용자가 속한 프로젝트 목록을 조회합니다.
        """
        # TODO : Eager loading
        owned_stmt = select(ProjectModel).where(ProjectModel.owner_id == user_id)
        member_stmt = select(ProjectModel).join(
            ProjectMemberModel, 
            ProjectModel.id == ProjectMemberModel.project_id
        ).where(ProjectMemberModel.user_id == user_id)
        
        owned_result = await self.session.execute(owned_stmt)
        member_result = await self.session.execute(member_stmt)
        
        owned_projects = owned_result.scalars().all()
        member_projects = member_result.scalars().all()
        
        all_projects = {}
        for project in owned_projects + member_projects:
            all_projects[project.id] = project
        
        return [project.to_domain() for project in all_projects.values()]


class ProjectMemberPgRepository(IProjectMemberRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, entity: ProjectMember) -> ProjectMember:
        """
        프로젝트 멤버 엔티티를 저장하거나 업데이트합니다.
        """
        member_model = ProjectMemberModel.from_domain(entity)
        
        # upsert
        self.session.add(member_model)
        await self.session.commit()
        await self.session.refresh(member_model)
        
        return member_model.to_domain()
    
    async def delete(self, id: int) -> bool:
        """
        ID로 프로젝트 멤버를 삭제합니다.
        """
        member = await self.session.get(ProjectMemberModel, id)
        if not member:
            return False
        
        await self.session.delete(member)
        await self.session.commit()
        return True
    
    async def get_by_id(self, id: int) -> Optional[ProjectMember]:
        """
        ID로 프로젝트 멤버를 조회합니다.
        """
        member = await self.session.get(ProjectMemberModel, id)
        if not member:
            return None
        return member.to_domain()
    
    async def get_all(self) -> List[ProjectMember]:
        """
        모든 프로젝트 멤버를 조회합니다.
        """
        result = await self.session.execute(select(ProjectMemberModel))
        members = result.scalars().all()
        return [member.to_domain() for member in members]
    
    async def count(self) -> int:
        """
        전체 프로젝트 멤버 수를 반환합니다.
        """
        result = await self.session.execute(select(ProjectMemberModel))
        return len(result.scalars().all())
    
    async def exists(self, id: int) -> bool:
        """
        해당 ID의 프로젝트 멤버가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(ProjectMemberModel.id == id))
        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def get_by_project_id(self, project_id: int) -> List[ProjectMember]:
        """
        프로젝트 ID로 프로젝트 멤버 목록을 조회합니다.
        """
        stmt = select(ProjectMemberModel).where(ProjectMemberModel.project_id == project_id)
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return [member.to_domain() for member in members]
    
    async def get_by_user_id(self, user_id: int) -> List[ProjectMember]:
        """
        사용자 ID로 프로젝트 멤버 목록을 조회합니다.
        """
        stmt = select(ProjectMemberModel).where(ProjectMemberModel.user_id == user_id)
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return [member.to_domain() for member in members]
    
    async def get_by_role(self, role: str) -> List[ProjectMember]:
        """
        역할로 프로젝트 멤버 목록을 조회합니다.
        """
        stmt = select(ProjectMemberModel).where(ProjectMemberModel.role == role)
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return [member.to_domain() for member in members]