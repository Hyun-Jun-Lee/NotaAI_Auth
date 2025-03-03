import pytest

from domain.user import User


@pytest.fixture
def user():
    """기본 사용자 객체를 생성하는 fixture"""
    user = User.create(
        email="test@example.com",
        name="Test User",
        password="password123",
        tenant_id="tenant456",
        is_admin=False
    )
    user.id = "user123" 
    return user
