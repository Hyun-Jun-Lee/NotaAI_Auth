from datetime import datetime
from typing import List

from domain.user import User
from repository.interface import IUserRepository
from exception.domain import (
    UserNotFoundException,
    UserAlreadyExistsException,
    EmailCodeExpiredException
)


class UserService:
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_all_user(self, skip: int = 0, limit: int = 100) -> List[User]:
        """모든 사용자 조회"""
        return await self.user_repository.get_all_user(skip, limit)
    
    async def create_user(self, email: str, name: str, password: str, tenant_id: int, is_admin: bool = False) -> User:
        """
        새로운 사용자를 생성합니다.
        """
        if await self.user_repository.exists_by_email(email):
            raise UserAlreadyExistsException(email)
        
        user = User.create(
            email=email,
            name=name,
            password=password,
            tenant_id=tenant_id,
            is_admin=is_admin
        )
        
        return await self.user_repository.save(user)
    
    async def get_user_by_id(self, user_id: int) -> User:
        """
        ID로 사용자를 조회합니다.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=str(user_id))
        return user
    
    async def get_user_by_email(self, email: str) -> User:
        """
        이메일로 사용자를 조회합니다.
        """
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(email=email)
        return user
    
    async def get_users_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[User]:
        """
        테넌트 ID로 사용자 목록을 조회합니다.
        """
        return await self.user_repository.get_by_tenant_id(tenant_id, skip, limit)
    
    async def get_admin_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        관리자 사용자 목록을 조회합니다.
        """
        return await self.user_repository.get_admin_users(skip, limit)
    
    async def authenticate_user(self, email: str, password: str) -> User:
        """
        사용자 인증을 수행합니다.
        """
        user = await self.get_user_by_email(email)
        
        user.verify_password(password)
        
        return user
    
    async def update_user(self, user: User) -> User:
        """
        사용자 정보를 업데이트합니다.
        """
        return await self.user_repository.save(user)
    
    async def delete_user(self, user_id: int) -> bool:
        """
        사용자를 삭제합니다.
        """
        if not await self.user_repository.exists(user_id):
            raise UserNotFoundException(user_id=str(user_id))
        
        return await self.user_repository.delete(user_id)
    
    async def change_password(self, user_id: int, current_password: str, new_password: str) -> User:
        """
        사용자 비밀번호를 변경합니다.
        """
        user = await self.get_user_by_id(user_id)
        
        user.change_password(current_password, new_password)
        
        return await self.update_user(user)
    
    async def generate_email_verification_code(self, user_id: int, expires_in_minutes: int = 30) -> str:
        """
        이메일 인증 코드를 생성합니다.
        """
        user = await self.get_user_by_id(user_id)
        
        email_code = user.generate_email_code(expires_in_minutes)
        
        await self.update_user(user)
        
        return email_code
    
    async def verify_email(self, user_id: int, email_code: str) -> User:
        """
        이메일 인증을 수행합니다.
        """
        user = await self.get_user_by_id(user_id)
        
        user.verify_email(email_code)
        
        return await self.update_user(user)
    
    async def request_password_reset(self, email: str, expires_in_minutes: int = 30) -> str:
        """
        비밀번호 재설정 요청을 처리합니다.
        """
        user = await self.get_user_by_email(email)
        
        if user.email_code:
            if datetime.now() < user.email_code_expires_at:
                return user.email_code
            else:
                raise EmailCodeExpiredException()

        
        email_code = user.generate_email_code(expires_in_minutes)
        
        await self.update_user(user)
        
        return email_code
    
    async def verify_email_code(self, user_id: int, email_code: str) -> bool:
        """
        이메일 코드의 유효성을 검증합니다.
        """
        user = await self.get_user_by_id(user_id)
        
        # 코드가 유효한지 확인
        if not user.email_code or user.email_code != email_code:
            return False
            
        # 코드가 만료되었는지 확인
        if datetime.now() > user.email_code_expires_at:
            return False
            
        return True
    
    async def reset_password(self, user_id: int, new_password: str) -> User:
        """
        비밀번호를 재설정합니다.
        """
        user = await self.get_user_by_id(user_id)
        
        # 비밀번호 변경
        user.password = new_password
        user.hash_password()
        
        # 인증 코드 초기화
        user.email_code = None
        user.email_code_expires_at = None
        
        # 사용자 정보 업데이트
        return await self.update_user(user)