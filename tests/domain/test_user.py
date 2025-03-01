import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.utils import hash_password
from src.exception.domain.user_exception import (
    EmailCodeNotGeneratedException,
    EmailCodeExpiredException,
    EmailCodeMismatchException,
    RoleNotFoundException,
    UserRoleNotFoundException,
    InvalidPasswordException
)


def test_user_creation(self, user):
    """User 객체가 올바르게 생성되는지 테스트"""
    assert user.id == "user123"
    assert user.email == "test@example.com"
    assert user.tenant_id == "tenant456"
    assert user.roles == ["user"]
    assert user.is_active is True
    assert user.email_verified is False
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_generate_email_code(self, user):
    """이메일 인증 코드 생성 테스트"""
    code = user.generate_email_code()
    
    assert user.email_code is not None
    assert user.email_code_expires_at is not None
    time_diff = user.email_code_expires_at - datetime.now()
    assert 23.9 <= time_diff.total_seconds() / 3600 <= 24.1
    assert code == user.email_code

def test_generate_email_code_custom_expiry(self, user):
    """사용자 지정 만료 시간으로 이메일 인증 코드 생성 테스트"""
    user.generate_email_code(expires_in_minutes=30)
    
    time_diff = user.email_code_expires_at - datetime.now()
    assert 0.9 <= time_diff.total_seconds() / 3600 <= 1.1

def test_verify_email_success(self, user):
    """이메일 인증 성공 테스트"""
    code = user.generate_email_code()
    
    result = user.verify_email(code)
    
    assert result is True
    assert user.email_verified is True
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_verify_email_wrong_code(self, user):
    """잘못된 이메일 인증 코드 테스트"""
    code = user.generate_email_code()
    
    with pytest.raises(EmailCodeMismatchException):
        user.verify_email("wrong_code")

def test_verify_email_expired_code(self, user):
    """만료된 이메일 인증 코드 테스트"""
    code = user.generate_email_code()
    
    user.email_code_expires_at = datetime.now() - timedelta(hours=1)
    
    with pytest.raises(EmailCodeExpiredException):
        user.verify_email(code)

def test_verify_password_success(self, user):
    """올바른 비밀번호 검증 테스트"""
    assert user.verify_password("password123") is True

def test_verify_password_failure(self, user):
    """잘못된 비밀번호 검증 테스트"""
    with pytest.raises(InvalidPasswordException):
        user.verify_password("wrong_password")

def test_reset_password_success(self, user):
    """비밀번호 재설정 성공 테스트"""
    code = user.generate_email_code()
    old_password_hash = user.password_hash
    
    result = user.reset_password(code, "new_password123")
    
    assert result is True
    assert user.password_hash != old_password_hash
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_reset_password_wrong_code(self, user):
    """잘못된 코드로 비밀번호 재설정 실패 테스트"""
    user.generate_email_code()
    
    with pytest.raises(EmailCodeMismatchException):
        user.reset_password("wrong_code", "new_password123")

def test_reset_password_expired_code(self, user):
    """만료된 코드로 비밀번호 재설정 실패 테스트"""
    code = user.generate_email_code()
    
    user.email_code_expires_at = datetime.now() - timedelta(hours=1)
    
    with pytest.raises(EmailCodeExpiredException):
        user.reset_password(code, "new_password123")

def test_add_role_success(self, user):
    """역할 추가 성공 테스트"""
    assert user.roles == ["user"]
    
    # ROLE_ACTIONS에 정의된 역할만 추가 가능
    with patch('src.domain.user.ROLE_ACTIONS', {"user": [], "admin": [], "editor": []}):
        user.add_role("admin")
        assert "admin" in user.roles
        assert len(user.roles) == 2
        
        # 이미 가지고 있는 역할 추가 시 변화 없음
        user.add_role("user")
        assert len(user.roles) == 2

def test_add_role_not_found(self, user):
    """존재하지 않는 역할 추가 시 예외 발생 테스트"""
    with patch('src.domain.user.ROLE_ACTIONS', {"user": [], "admin": []}):
        with pytest.raises(RoleNotFoundException):
            user.add_role("non_existent_role")

def test_remove_role_success(self, user):
    """역할 제거 성공 테스트"""  
    assert user.roles == ["user"]
    
    user.remove_role("user")
    assert "user" not in user.roles
    assert len(user.roles) == 0

def test_remove_role_not_found(self, user):
    """사용자가 가지고 있지 않은 역할 제거 시 예외 발생 테스트"""  
    with pytest.raises(UserRoleNotFoundException):
        user.remove_role("admin")

def test_has_role(self, user):
    """역할 확인 테스트"""
    # ROLE_ACTIONS에 정의된 역할만 확인 가능
    with patch('src.domain.user.ROLE_ACTIONS', {"user": [], "admin": []}):
        assert user.has_role("user") is True
        assert user.has_role("admin") is False
        
        user.add_role("admin")
        assert user.has_role("admin") is True

def test_has_role_not_found(self, user):
    """존재하지 않는 역할 확인 시 예외 발생 테스트"""
    with patch('src.domain.user.ROLE_ACTIONS', {"user": []}):
        with pytest.raises(RoleNotFoundException):
            user.has_role("non_existent_role")

def test_email_code_not_generated(self, user):
    """이메일 코드가 생성되지 않은 상태에서 예외 발생 테스트"""
    with pytest.raises(EmailCodeNotGeneratedException):
        user.verify_email("any_code")
    
    with pytest.raises(EmailCodeNotGeneratedException):
        user.reset_password("any_code", "new_password")
