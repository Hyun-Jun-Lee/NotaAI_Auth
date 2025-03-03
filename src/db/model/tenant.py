from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from typing import Optional, Type

from db.model.base import BaseDBModel
from domain.tenant import Tenant


class TenantModel(BaseDBModel):
    
    __tablename__ = "tenant"
    
    name = Column(String(255), unique=True, nullable=False, index=True)
    
    # 관계 설정
    users = relationship("UserModel", back_populates="tenant", cascade="all, delete-orphan")
    projects = relationship("ProjectModel", back_populates="tenant", cascade="all, delete-orphan")
    
    def to_domain(self) -> Tenant:
        """DB 모델을 도메인 모델로 변환"""
        return Tenant(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, domain: Tenant) -> "TenantModel":
        """도메인 모델을 DB 모델로 변환"""
        return cls(
            id=domain.id,
            name=domain.name,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
