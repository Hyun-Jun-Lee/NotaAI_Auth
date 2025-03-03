from typing import List, Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from db.model import TenantModel
from domain import Tenant
from repository.interface import ITenantRepository


class TenantPgRepository(ITenantRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, entity: Tenant) -> Tenant:
        """
        테넌트 엔티티를 저장하거나 업데이트합니다.
        """
        tenant_model = TenantModel.from_domain(entity)
        
        # upsert
        self.session.add(tenant_model)
        await self.session.commit()
        await self.session.refresh(tenant_model)
        
        return tenant_model.to_domain()
    
    async def delete(self, id: int) -> bool:
        """
        ID로 테넌트를 삭제합니다.
        """
        tenant = await self.session.get(TenantModel, id)
        if not tenant:
            return False
        
        await self.session.delete(tenant)
        await self.session.commit()
        return True
    
    async def get_by_id(self, id: int) -> Optional[Tenant]:
        """
        ID로 테넌트를 조회합니다.
        """
        tenant = await self.session.get(TenantModel, id)
        if not tenant:
            return None
        return tenant.to_domain()
    
    async def get_all(self) -> List[Tenant]:
        """
        모든 테넌트를 조회합니다.
        """
        result = await self.session.execute(select(TenantModel))
        tenants = result.scalars().all()
        return [tenant.to_domain() for tenant in tenants]
    
    async def count(self) -> int:
        """
        전체 테넌트 수를 반환합니다.
        """
        result = await self.session.execute(select(TenantModel))
        return len(result.scalars().all())
    
    async def exists(self, id: int) -> bool:
        """
        해당 ID의 테넌트가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(TenantModel.id == id))
        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        테넌트 이름으로 테넌트를 조회합니다.
        """
        stmt = select(TenantModel).where(TenantModel.name == name)
        result = await self.session.execute(stmt)
        tenant = result.scalars().first()
        return tenant.to_domain() if tenant else None
    
    async def exists_by_name(self, name: str) -> bool:
        """
        해당 이름의 테넌트가 존재하는지 확인합니다.
        """
        stmt = select(exists().where(TenantModel.name == name))
        result = await self.session.execute(stmt)
        return result.scalar()