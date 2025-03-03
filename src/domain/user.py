import secrets
from datetime import datetime, timedelta

from utils import hash_password, check_password
from domain.base import BaseDomain
from domain.permission import ROLE_ACTIONS, Action
from domain.project import Project
from exception.domain import (
    EmailCodeNotGeneratedException,
    EmailCodeExpiredException,
    EmailCodeMismatchException,
    InvalidPasswordException,
    RoleNotFoundException,
)

class User(BaseDomain):
    def __init__(self, email: str, name: str, password_hash: str, tenant_id: str, is_admin: bool = False, created_at: datetime = None, updated_at: datetime = None, id: int = None):
        super().__init__(id, created_at, updated_at)
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.tenant_id = tenant_id
        self.is_admin = is_admin
        self.email_verified = False
        self.email_code = None
        self.email_code_expires_at = None

    def generate_email_code(self, expires_in_minutes: int = 30) -> str:
        """이메일 인증 코드를 생성합니다."""

        self.email_code = secrets.token_hex(8)
        self.email_code_expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        self.update_timestamp()
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
        self.update_timestamp()
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
        self.update_timestamp()
        return True
