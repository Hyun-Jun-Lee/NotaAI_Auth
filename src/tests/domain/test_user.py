import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from utils import hash_password
from exception.domain.user_exception import (
    EmailCodeNotGeneratedException,
    EmailCodeExpiredException,
    EmailCodeMismatchException,
    RoleNotFoundException,
    UserRoleNotFoundException,
    InvalidPasswordException
)


def test_user_creation(user):
    """User 객체가 올바르게 생성되는지 테스트"""
    assert user.id == "user123"
    assert user.email == "test@example.com"
    assert user.tenant_id == "tenant456"
    assert user.is_admin is False
    assert user.email_verified is False
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_generate_email_code(user):
    """이메일 인증 코드 생성 테스트"""
    code = user.generate_email_code()
    
    assert user.email_code is not None
    assert user.email_code_expires_at is not None
    time_diff = user.email_code_expires_at - datetime.now()
    assert 1750 <= time_diff.total_seconds() <= 1850
    assert code == user.email_code

def test_verify_email_success(user):
    """이메일 인증 성공 테스트"""
    code = user.generate_email_code()
    
    result = user.verify_email(code)
    
    assert result is True
    assert user.email_verified is True
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_verify_email_wrong_code(user):
    """잘못된 이메일 인증 코드 테스트"""
    code = user.generate_email_code()
    
    with pytest.raises(EmailCodeMismatchException):
        user.verify_email("wrong_code")

def test_verify_email_expired_code(user):
    """만료된 이메일 인증 코드 테스트"""
    code = user.generate_email_code()
    
    user.email_code_expires_at = datetime.now() - timedelta(hours=1)
    
    with pytest.raises(EmailCodeExpiredException):
        user.verify_email(code)

def test_verify_password_success(user):
    """비밀번호 검증 테스트"""
    assert user.verify_password("password123") is True

def test_verify_password_failure(user):
    """잘못된 비밀번호 검증 테스트"""
    with pytest.raises(InvalidPasswordException):
        user.verify_password("wrong_password")

def test_reset_password_success(user):
    """비밀번호 재설정 테스트"""
    code = user.generate_email_code()
    old_password_hash = user.password_hash
    
    result = user.reset_password(code, "new_password123")
    
    assert result is True
    assert user.password_hash != old_password_hash
    assert user.email_code is None
    assert user.email_code_expires_at is None

def test_reset_password_wrong_code(user):
    """비밀번호 재설정 실패 테스트"""
    code = user.generate_email_code()
    
    with pytest.raises(EmailCodeMismatchException):
        user.reset_password("wrong_code", "new_password123")

def test_reset_password_expired_code(user):
    """만료된 코드로 비밀번호 재설정 실패 테스트"""
    code = user.generate_email_code()
    
    user.email_code_expires_at = datetime.now() - timedelta(hours=1)
    
    with pytest.raises(EmailCodeExpiredException):
        user.reset_password(code, "new_password123")
