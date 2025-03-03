import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import patch

from exception.domain import (
    UserNotFoundException,
    UserAlreadyExistsException,
    EmailCodeExpiredException
)

@pytest.mark.asyncio
async def test_create_user_success(user_service, user_repository_mock):
    """사용자 생성 테스트"""

    user_repository_mock.exists_by_email.return_value = False
    user_repository_mock.save.side_effect = lambda user_obj: user_obj
    
    result = await user_service.create_user(
        email="test@example.com",
        name="Test User",
        password="password123",
        tenant_id="tenant456"
    )
    
    assert result is not None
    assert result.email == "test@example.com"
    assert result.name == "Test User"
    assert result.password_hash != "password123"
    user_repository_mock.exists_by_email.assert_called_once_with("test@example.com")
    user_repository_mock.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_already_exists(user_service, user_repository_mock):
    """이미 존재하는 이메일로 사용자 생성 시도"""

    user_repository_mock.exists_by_email.return_value = True
    
    with pytest.raises(UserAlreadyExistsException):
        await user_service.create_user(
            email="test@example.com",
            name="Test User",
            password="password123",
            tenant_id="tenant456"
        )
    
    user_repository_mock.exists_by_email.assert_called_once_with("test@example.com")
    user_repository_mock.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_by_id_success(user_service, user_repository_mock, user):
    """ID로 사용자 조회 성공 테스트"""
    
    user_repository_mock.get_by_id.return_value = user
    
    result = await user_service.get_user_by_id("user123")
    
    assert result is not None
    assert result.id == "user123"
    assert result.email == "test@example.com"
    user_repository_mock.get_by_id.assert_called_once_with("user123")


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_service, user_repository_mock):
    """존재하지 않는 ID로 사용자 조회 테스트"""

    user_repository_mock.get_by_id.return_value = None
    
    with pytest.raises(UserNotFoundException):
        await user_service.get_user_by_id("nonexistent_id")
    
    user_repository_mock.get_by_id.assert_called_once_with("nonexistent_id")


@pytest.mark.asyncio
async def test_get_user_by_email_success(user_service, user_repository_mock, user):
    """이메일로 사용자 조회 성공 테스트"""

    user_repository_mock.get_by_email.return_value = user
    
    result = await user_service.get_user_by_email("test@example.com")
    
    assert result is not None
    assert result.email == "test@example.com"
    user_repository_mock.get_by_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_service, user_repository_mock):
    """존재하지 않는 이메일로 사용자 조회 테스트"""

    user_repository_mock.get_by_email.return_value = None
    
    with pytest.raises(UserNotFoundException):
        await user_service.get_user_by_email("nonexistent@example.com")
    
    user_repository_mock.get_by_email.assert_called_once_with("nonexistent@example.com")


@pytest.mark.asyncio
async def test_generate_email_verification_code(user_service, user_repository_mock, user):
    """이메일 인증 코드 생성 테스트"""

    user_repository_mock.get_by_id.return_value = user
    user_repository_mock.save.return_value = user
    
    code = await user_service.generate_email_verification_code("user123")
    
    assert code is not None
    assert user.email_code == code

    user_repository_mock.get_by_id.assert_called_once_with("user123")
    user_repository_mock.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_verify_email_success(user_service, user_repository_mock, user):
    """이메일 인증 성공 테스트"""

    user_repository_mock.get_by_id.return_value = user
    user_repository_mock.save.return_value = user

    code = user.generate_email_code()
    
    result = await user_service.verify_email("user123", code)
    
    assert result is not None
    assert result.email_verified is True
    
    user_repository_mock.get_by_id.assert_called_once_with("user123")
    user_repository_mock.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_request_password_reset_new_code(user_service, user_repository_mock, user):
    """비밀번호 재설정 요청 테스트"""

    user_repository_mock.get_by_email.return_value = user
    user_repository_mock.save.return_value = user

    assert user.email_code is None
    
    code = await user_service.request_password_reset("test@example.com")
    
    assert code is not None
    assert user.email_code == code
    
    user_repository_mock.get_by_email.assert_called_once_with("test@example.com")
    user_repository_mock.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_request_password_reset_existing_valid_code(user_service, user_repository_mock, user):
    """비밀번호 재설정 요청 (이미 유효한 code 존재) 테스트"""

    user.email_code = "existing_code"
    user.email_code_expires_at = datetime.now() + timedelta(minutes=10)
    
    user_repository_mock.get_by_email.return_value = user
    
    code = await user_service.request_password_reset("test@example.com")
    
    assert code == "existing_code"
    user_repository_mock.get_by_email.assert_called_once_with("test@example.com")
    user_repository_mock.save.assert_not_called()

@pytest.mark.asyncio
async def test_request_password_reset_expired_valid_code(user_service, user_repository_mock, user):
    """비밀번호 재설정 요청 (이미 code 존재, 유효기간 완료) 테스트"""

    user.email_code = "existing_code"
    user.email_code_expires_at = datetime.now() - timedelta(minutes=10)
    
    user_repository_mock.get_by_email.return_value = user
    
    with pytest.raises(EmailCodeExpiredException):
        code = await user_service.request_password_reset("test@example.com")
    
    user_repository_mock.get_by_email.assert_called_once_with("test@example.com")
    user_repository_mock.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_user(user_service, user_repository_mock, user):
    """사용자 정보 업데이트 테스트"""
    # 준비
    user_repository_mock.save.return_value = user
    
    # 실행
    result = await user_service.update_user(user)
    
    # 검증
    assert result is not None
    assert result.id == user.id
    user_repository_mock.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_delete_user_success(user_service, user_repository_mock):
    """사용자 삭제 성공 테스트"""

    user_repository_mock.exists.return_value = True
    user_repository_mock.delete.return_value = True
    
    result = await user_service.delete_user("user123")
    
    assert result is True
    user_repository_mock.exists.assert_called_once_with("user123")
    user_repository_mock.delete.assert_called_once_with("user123")


@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, user_repository_mock):
    """존재하지 않는 사용자 삭제 테스트"""
    # 준비
    user_repository_mock.exists.return_value = False
    
    # 실행 및 검증
    with pytest.raises(UserNotFoundException):
        await user_service.delete_user(999)
    
    user_repository_mock.exists.assert_called_once_with(999)
    user_repository_mock.delete.assert_not_called()
