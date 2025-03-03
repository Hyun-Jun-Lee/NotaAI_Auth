import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from domain.project import Project, ProjectMember
from service import ProjectService


@pytest.fixture
def project():
    """기본 프로젝트 객체를 생성하는 fixture"""
    return Project(
        id=1,
        name="테스트 프로젝트",
        description="테스트 프로젝트 설명",
        owner_id=100,
        tenant_id=200
    )


@pytest.fixture
def project_with_members():
    """멤버가 있는 프로젝트 객체를 생성하는 fixture"""
    project = Project(
        id=1,
        name="테스트 프로젝트",
        description="테스트 프로젝트 설명",
        owner_id=100,
        tenant_id=200
    )
    
    project.members.append(
        ProjectMember(
            id=1,
            project_id=1,
            user_id=100,
            role="PROJECT_OWNER",
            invited_by=100
        )
    )
    
    project.members.append(
        ProjectMember(
            id=2,
            project_id=1,
            user_id=101,
            role="EDITOR",
            invited_by=100
        )
    )
    
    project.members.append(
        ProjectMember(
            id=3,
            project_id=1,
            user_id=102,
            role="VIEWER",
            invited_by=100
        )
    )
    
    return project


@pytest.fixture
def project_member():
    """기본 프로젝트 멤버 객체를 생성하는 fixture"""
    return ProjectMember(
        id=1,
        project_id=1,
        user_id=100,
        role="EDITOR",
        invited_by=200
    )


@pytest.fixture
def project_repository_mock():
    """ProjectRepository mock fixture"""
    repository = AsyncMock()
    return repository


@pytest.fixture
def project_member_repository_mock():
    """ProjectMemberRepository mock fixture"""
    repository = AsyncMock()
    return repository


@pytest.fixture
def project_service(project_repository_mock, project_member_repository_mock):
    """ProjectService fixture"""
    return ProjectService(project_repository_mock, project_member_repository_mock)
