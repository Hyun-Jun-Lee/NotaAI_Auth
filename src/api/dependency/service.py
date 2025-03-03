from fastapi import Depends

from service.user_service import UserService
from service.project_service import ProjectService
from repository.interface import IUserRepository, IProjectRepository, IProjectMemberRepository, ITenantRepository
from api.dependency.repository import (
    get_user_repository,
    get_project_repository,
    get_project_member_repository,
    get_tenant_repository
)


async def get_user_service(
    user_repository: IUserRepository = Depends(get_user_repository)
) -> UserService:
    """
    사용자 서비스 의존성 함수
    """
    return UserService(user_repository)


async def get_project_service(
    project_repository: IProjectRepository = Depends(get_project_repository),
    project_member_repository: IProjectMemberRepository = Depends(get_project_member_repository)
) -> ProjectService:
    """
    프로젝트 서비스 의존성 함수
    """
    return ProjectService(project_repository, project_member_repository)
