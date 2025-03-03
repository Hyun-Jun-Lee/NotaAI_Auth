from typing import List, Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from db.model import UserModel
from domain import User
from repository.interface import IUserRepository


class UserPgRepository(IUserRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, entity: User) -> User:
        """
        사용자 엔티티를 저장하거나 업데이트합니다.
        """
        user_model = UserModel.from_domain(entity)
        
        # upsert
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        
        return user_model.to_domain()
    
    async def delete(self, id: int) -> bool:
        """
        ID로 사용자를 삭제합니다.
        """
        user = await self.session.get(UserModel, id)
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.commit()
        return True
    
    async def get_by_id(self, id: int) -> Optional[User]:
        """
        ID로 사용자를 조회합니다.
        """
        user = await self.session.get(UserModel, id)
        if not user:
            return None
        return user.to_domain()
    
    async def get_all(self) -> List[User]:
        """
        모든 사용자를 조회합니다.
        """
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [user.to_domain() for user in users]
    
    async def count(self) -> int:
        """
        전체 사용자 수를 반환합니다.
        """
        result = await self.session.execute(select(UserModel))
        return len(result.scalars().all())
    
    async def exists(self, id: int) -> bool:
        """
        해당 ID의 사용자가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(UserModel.id == id))
        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자를 조회합니다.
        """
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user.to_domain() if user else None
    
    async def get_by_tenant_id(self, tenant_id: int) -> List[User]:
        """
        테넌트 ID로 사용자 목록을 조회합니다.
        """
        stmt = select(UserModel).where(UserModel.tenant_id == tenant_id)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [user.to_domain() for user in users]
    
    async def get_admin_users(self) -> List[User]:
        """
        관리자 사용자 목록을 조회합니다.
        """
        stmt = select(UserModel).where(UserModel.is_admin == True)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [user.to_domain() for user in users]
    
    async def exists_by_email(self, email: str) -> bool:
        """
        해당 이메일의 사용자가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(UserModel.email == email))
        result = await self.session.execute(stmt)
        return result.scalar()