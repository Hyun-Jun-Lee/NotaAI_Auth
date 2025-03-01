import secrets
from datetime import datetime, timedelta
from typing import List

from utils import hash_password, check_password
from domain.permission import ROLE_ACTIONS
from exception.domain.user_exception import (
    EmailCodeNotGeneratedException,
    EmailCodeExpiredException,
    EmailCodeMismatchException,
    RoleNotFoundException,
    UserRoleNotFoundException,
    InvalidPasswordException
)

class User:
    def __init__(self, id: str, email: str, password_hash: str, tenant_id: str, roles: List[str] = None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.tenant_id = tenant_id
        self.roles = roles or []
        self.is_active = True
        self.email_verified = False
        self.email_code = None
        self.email_code_expires_at = None

    def generate_email_code(self, expires_in_minutes: int = 30) -> str:
        """이메일 인증 코드를 생성합니다."""

        self.email_code = secrets.token_hex(8)
        self.email_code_expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        return self.email_code

    def verify_email(self, email_code: str) -> bool:
        """이메일 인증 코드를 검증합니다."""

        if not self.email_code:
            raise EmailCodeNotGeneratedException()
            
        if datetime.now() > self.email_code_expires_at:
            self.email_code = None
            self.email_code_expires_at = None
            raise EmailCodeExpiredException()
            
        if self.email_code != email_code:
            raise EmailCodeMismatchException()
            
        self.email_verified = True
        self.email_code = None
        self.email_code_expires_at = None
        return True

    def verify_password(self, password: str) -> bool:
        """비밀번호를 검증합니다."""

        result = check_password(password, self.password_hash)
        if not result:
            raise InvalidPasswordException()
        return result

    def reset_password(self, email_code: str, new_password: str) -> bool:
        """비밀번호를 재설정합니다."""

        if not self.email_code:
            raise EmailCodeNotGeneratedException()
            
        if datetime.now() > self.email_code_expires_at:
            self.email_code = None
            self.email_code_expires_at = None
            raise EmailCodeExpiredException()
            
        if self.email_code != email_code:
            raise EmailCodeMismatchException()
            
        self.password_hash = hash_password(new_password)
        self.email_code = None
        self.email_code_expires_at = None
        return True

    def add_role(self, role: str) -> None:
        """사용자에게 역할을 추가합니다."""

        if role not in ROLE_ACTIONS:
            raise RoleNotFoundException(role)
            
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role: str) -> None:
        """사용자의 역할을 제거합니다."""

        if role in self.roles:
            self.roles.remove(role)
        else:
            raise UserRoleNotFoundException(role)
    
    def has_role(self, role: str) -> bool:
        """사용자가 특정 역할을 가지고 있는지 확인합니다."""

        if role not in ROLE_ACTIONS:
            raise RoleNotFoundException(role)
            
        return role in self.roles