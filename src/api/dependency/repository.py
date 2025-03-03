from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from repository.pg import UserPgRepository, ProjectPgRepository, ProjectMemberPgRepository, TenantPgRepository
from repository.interface import IUserRepository, IProjectRepository, IProjectMemberRepository, ITenantRepository


async def get_user_repository(session: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserPgRepository(session)


async def get_project_repository(session: AsyncSession = Depends(get_db)) -> IProjectRepository:
    return ProjectPgRepository(session)


async def get_project_member_repository(session: AsyncSession = Depends(get_db)) -> IProjectMemberRepository:
    return ProjectMemberPgRepository(session)


async def get_tenant_repository(session: AsyncSession = Depends(get_db)) -> ITenantRepository:
    return TenantPgRepository(session)
