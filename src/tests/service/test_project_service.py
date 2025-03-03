import pytest
import asyncio
from unittest.mock import patch

from domain.project import Project, ProjectMember
from domain.permission import ROLE_ACTIONS
from exception.domain import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException,
    ProjectMemberNotFoundException,
    ProjectMemberAlreadyExistsException,
    InvalidRoleException
)


@pytest.mark.asyncio
async def test_create_project_success(project_service, project_repository_mock):
    """프로젝트 생성 성공 테스트"""
    
    project_repository_mock.get_by_name.return_value = None
    project_repository_mock.save.side_effect = lambda project_obj: project_obj
    
    result = await project_service.create_project(
        name="테스트 프로젝트",
        description="테스트 프로젝트 설명",
        owner_id=100,
        tenant_id=200
    )
    
    assert result is not None
    assert result.name == "테스트 프로젝트"
    assert result.description == "테스트 프로젝트 설명"
    assert result.owner_id == 100
    assert result.tenant_id == 200
    
    project_repository_mock.get_by_name.assert_called_once_with("테스트 프로젝트")
    project_repository_mock.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_project_already_exists(project_service, project_repository_mock, project):
    """이미 존재하는 이름으로 프로젝트 생성 시도"""
    
    project_repository_mock.get_by_name.return_value = project
    
    with pytest.raises(ProjectAlreadyExistsException):
        await project_service.create_project(
            name="테스트 프로젝트",
            description="테스트 프로젝트 설명",
            owner_id=100,
            tenant_id=200
        )
    
    project_repository_mock.get_by_name.assert_called_once_with("테스트 프로젝트")
    project_repository_mock.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_project_by_id_success(project_service, project_repository_mock, project):
    """ID로 프로젝트 조회 성공 테스트"""
    
    project_repository_mock.get_by_id.return_value = project
    
    result = await project_service.get_project_by_id(1)
    
    assert result is not None
    assert result.id == 1
    assert result.name == project.name
    project_repository_mock.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_project_by_id_not_found(project_service, project_repository_mock):
    """존재하지 않는 ID로 프로젝트 조회 테스트"""
    
    project_repository_mock.get_by_id.return_value = None
    
    with pytest.raises(ProjectNotFoundException):
        await project_service.get_project_by_id(999)
    
    project_repository_mock.get_by_id.assert_called_once_with(999)


@pytest.mark.asyncio
async def test_get_project_by_name_success(project_service, project_repository_mock, project):
    """이름으로 프로젝트 조회 테스트"""
    
    project_repository_mock.get_by_name.return_value = project
    
    result = await project_service.get_project_by_name("테스트 프로젝트")
    
    assert result is not None
    assert result.name == "테스트 프로젝트"
    project_repository_mock.get_by_name.assert_called_once_with("테스트 프로젝트")


@pytest.mark.asyncio
async def test_get_projects_by_tenant(project_service, project_repository_mock, project):
    """테넌트 ID로 프로젝트 목록 조회 테스트"""
    
    project_repository_mock.get_by_tenant_id.return_value = [project]
    
    result = await project_service.get_projects_by_tenant(200)
    
    assert len(result) == 1
    assert result[0].tenant_id == 200
    project_repository_mock.get_by_tenant_id.assert_called_once_with(200)


@pytest.mark.asyncio
async def test_get_projects_by_owner(project_service, project_repository_mock, project):
    """소유자 ID로 프로젝트 목록 조회 테스트"""
    
    project_repository_mock.get_by_owner_id.return_value = [project]
    
    result = await project_service.get_projects_by_owner(100)
    
    assert len(result) == 1
    assert result[0].owner_id == 100
    project_repository_mock.get_by_owner_id.assert_called_once_with(100)


@pytest.mark.asyncio
async def test_get_projects_by_user(project_service, project_repository_mock, project):
    """사용자 ID로 프로젝트 목록 조회 테스트"""
    
    project_repository_mock.get_by_user_id.return_value = [project]
    
    result = await project_service.get_projects_by_user(100)
    
    assert len(result) == 1
    project_repository_mock.get_by_user_id.assert_called_once_with(100)


@pytest.mark.asyncio
async def test_update_project(project_service, project_repository_mock, project):
    """프로젝트 정보 업데이트 테스트"""
    
    project_repository_mock.get_by_id.return_value = project
    project_repository_mock.save.side_effect = lambda project_obj: project_obj
    
    result = await project_service.update_project(
        project_id=1,
        name="업데이트된 프로젝트",
        description="업데이트된 설명"
    )
    
    assert result is not None
    assert result.name == "업데이트된 프로젝트"
    assert result.description == "업데이트된 설명"
    project_repository_mock.get_by_id.assert_called_once_with(1)
    project_repository_mock.save.assert_called_once()


@pytest.mark.asyncio
async def test_delete_project_not_found(project_service, project_repository_mock):
    """존재하지 않는 프로젝트 삭제 테스트"""
    
    project_repository_mock.exists.return_value = False
    
    with pytest.raises(ProjectNotFoundException):
        await project_service.delete_project(999)
    
    project_repository_mock.exists.assert_called_once_with(999)
    project_repository_mock.delete.assert_not_called()


@pytest.mark.asyncio
async def test_invite_user_to_project_success(project_service, project_repository_mock, project_member_repository_mock, project):
    """프로젝트에 사용자 초대 성공 테스트"""
    
    project_repository_mock.get_by_id.return_value = project
    project_member_repository_mock.get_by_project_id.return_value = []
    project_member_repository_mock.save.side_effect = lambda member_obj: member_obj
    
    result = await project_service.invite_user_to_project(
        project_id=1,
        user_id=101,
        role="EDITOR",
        invited_by=100
    )
    
    assert result is not None
    assert result.project_id == 1
    assert result.user_id == 101
    assert result.role == "EDITOR"
    assert result.invited_by == 100
    project_repository_mock.get_by_id.assert_called_once_with(1)
    project_member_repository_mock.get_by_project_id.assert_called_once_with(1)
    project_member_repository_mock.save.assert_called_once()


@pytest.mark.asyncio
async def test_invite_user_to_project_invalid_role(project_service, project_repository_mock, project):
    """유효하지 않은 역할로 사용자 초대 테스트"""
    
    with pytest.raises(InvalidRoleException):
        await project_service.invite_user_to_project(
            project_id=1,
            user_id=101,
            role="INVALID_ROLE",
            invited_by=100
        )


@pytest.mark.asyncio
async def test_invite_user_to_project_already_member(project_service, project_repository_mock, project_member_repository_mock, project, project_member):
    """이미 멤버인 사용자 초대 테스트"""
    
    project_repository_mock.get_by_id.return_value = project
    project_member.user_id = 101
    project_member_repository_mock.get_by_project_id.return_value = [project_member]
    
    with pytest.raises(ProjectMemberAlreadyExistsException):
        await project_service.invite_user_to_project(
            project_id=1,
            user_id=101,
            role="EDITOR",
            invited_by=100
        )
    
    project_repository_mock.get_by_id.assert_called_once_with(1)
    project_member_repository_mock.get_by_project_id.assert_called_once_with(1)
    project_member_repository_mock.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_project_members(project_service, project_repository_mock, project_member_repository_mock, project_member):
    """프로젝트 멤버 목록 조회 테스트"""
    
    project_repository_mock.exists.return_value = True
    project_member_repository_mock.get_by_project_id.return_value = [project_member]
    
    result = await project_service.get_project_members(1)
    
    assert len(result) == 1
    assert result[0].project_id == 1
    project_repository_mock.exists.assert_called_once_with(1)
    project_member_repository_mock.get_by_project_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_project_members_not_found(project_service, project_repository_mock):
    """존재하지 않는 프로젝트의 멤버 목록 조회 테스트"""
    
    project_repository_mock.exists.return_value = False
    
    with pytest.raises(ProjectNotFoundException):
        await project_service.get_project_members(999)
    
    project_repository_mock.exists.assert_called_once_with(999)


@pytest.mark.asyncio
async def test_get_user_memberships(project_service, project_member_repository_mock, project_member):
    """사용자의 프로젝트 멤버십 목록 조회 테스트"""
    
    project_member_repository_mock.get_by_user_id.return_value = [project_member]
    
    result = await project_service.get_user_memberships(100)
    
    assert len(result) == 1
    assert result[0].user_id == 100
    project_member_repository_mock.get_by_user_id.assert_called_once_with(100)


@pytest.mark.asyncio
async def test_change_member_role(project_service, project_member_repository_mock, project_member):
    """프로젝트 멤버 역할 변경 테스트"""
    
    project_member_repository_mock.get_by_id.return_value = project_member
    project_member_repository_mock.save.side_effect = lambda member_obj: member_obj
    
    result = await project_service.change_member_role(
        member_id=1,
        new_role="VIEWER"
    )
    
    assert result is not None
    assert result.role == "VIEWER"
    project_member_repository_mock.get_by_id.assert_called_once_with(1)
    project_member_repository_mock.save.assert_called_once()


@pytest.mark.asyncio
async def test_change_member_role_not_found(project_service, project_member_repository_mock):
    """존재하지 않는 멤버 역할 변경 테스트"""
    
    project_member_repository_mock.get_by_id.return_value = None
    
    with pytest.raises(ProjectMemberNotFoundException):
        await project_service.change_member_role(
            member_id=999,
            new_role="VIEWER"
        )
    
    project_member_repository_mock.get_by_id.assert_called_once_with(999)
    project_member_repository_mock.save.assert_not_called()