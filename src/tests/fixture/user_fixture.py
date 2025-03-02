import pytest

from domain.user import User
from utils import hash_password


@pytest.fixture
def user():
    """기본 사용자 객체를 생성하는 fixture"""
    return User(
        id="user123",
        email="test@example.com",
        password_hash=hash_password("password123"),
        tenant_id="tenant456",
    )
