import pytest
from unittest.mock import patch, AsyncMock

from domain import User
from service import UserService



@pytest.fixture
def user():
    """User fixture"""
    user = User.create(
        email="test@example.com",
        name="Test User",
        password="password123",
        tenant_id="tenant456",
        is_admin=False
    )
    user.id = "user123" 
    return user

@pytest.fixture
def user_repository_mock():
    """UserRepository mock fixture"""
    repository = AsyncMock()
    return repository


@pytest.fixture
def user_service(user_repository_mock):
    """UserService fixture"""
    return UserService(user_repository_mock)
