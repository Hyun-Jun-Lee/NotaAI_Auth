import pytest
import time

from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from domain.project import Project, ProjectMember
from domain.permission import ROLE_ACTIONS, Action
from exception.domain import InvalidRoleException


def test_project_creation(project):
    """Project 객체가 올바르게 생성되는지 테스트"""
    assert project.id == 1
    assert project.name == "테스트 프로젝트"
    assert project.description == "테스트 프로젝트 설명"
    assert project.owner_id == 100
    assert project.tenant_id == 200
    assert isinstance(project.members, list)
    assert len(project.members) == 0
    assert project.created_at is not None
    assert project.updated_at is not None


def test_project_update(project):
    """프로젝트 정보 업데이트 테스트"""
    original_updated_at = project.updated_at
    
    time.sleep(1)
    
    project.update(name="업데이트된 프로젝트", description="업데이트된 설명")
    
    assert project.name == "업데이트된 프로젝트"
    assert project.description == "업데이트된 설명"
    assert project.updated_at > original_updated_at


def test_project_update_partial(project):
    """프로젝트 정보 부분 업데이트 테스트"""
    original_name = project.name
    original_description = project.description
    
    project.update(description="새로운 설명")
    project.update(name="새로운 이름")
    
    assert project.name == "새로운 이름"
    assert project.description == "새로운 설명"    


def test_invite_user_valid_role(project):
    """사용자 초대 테스트"""
    assert len(project.members) == 0
    
    project.invite_user(user_id=101, role="EDITOR", invited_by=100)
    
    assert len(project.members) == 1
    member = project.members[0]
    assert member.project_id == project.id
    assert member.user_id == 101
    assert member.role == "EDITOR"
    assert member.invited_by == 100


def test_invite_user_invalid_role(project):
    """유효하지 않은 역할로 사용자 초대 테스트"""
    with pytest.raises(InvalidRoleException):
        project.invite_user(user_id=101, role="INVALID_ROLE", invited_by=100)

    assert len(project.members) == 0


def test_project_with_members(project_with_members):
    """멤버가 있는 프로젝트 테스트"""
    assert len(project_with_members.members) == 3
    
    roles = [member.role for member in project_with_members.members]
    assert "PROJECT_OWNER" in roles
    assert "EDITOR" in roles
    assert "VIEWER" in roles
    
    # 특정 사용자 찾기
    editor = next(m for m in project_with_members.members if m.role == "EDITOR")
    assert editor.user_id == 101


def test_project_member_creation(project_member):
    """ProjectMember 객체가 올바르게 생성되는지 테스트"""
    assert project_member.id == 1
    assert project_member.project_id == 1
    assert project_member.user_id == 100
    assert project_member.role == "EDITOR"
    assert project_member.invited_by == 200
    assert project_member.created_at is not None
    assert project_member.updated_at is not None


def test_project_member_change_role_valid(project_member):
    """프로젝트 멤버 역할 변경 테스트"""
    original_updated_at = project_member.updated_at
    
    time.sleep(1)
    
    project_member.change_role("ADMIN")
    
    assert project_member.role == "ADMIN"
    assert project_member.updated_at > original_updated_at


def test_project_member_change_role_invalid(project_member):
    """프로젝트 멤버 유효하지 않는 역활 변경 테스트"""
    original_role = project_member.role
    
    with pytest.raises(InvalidRoleException) as excinfo:
        project_member.change_role("INVALID_ROLE")
    
    assert project_member.role == original_role
