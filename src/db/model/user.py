from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.model.base import BaseDBModel
from domain import User


class UserModel(BaseDBModel):
    
    __tablename__ = "user"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenant.id"), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_code = Column(String(255), nullable=True)
    email_code_expires_at = Column(DateTime, nullable=True)
    
    tenant = relationship("TenantModel", back_populates="users")
    project_members = relationship("ProjectMemberModel", back_populates="user", cascade="all, delete-orphan")
    
    def to_domain(self) -> User:
        """DB 모델을 도메인 모델로 변환"""
        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            password_hash=self.password_hash,
            tenant_id=self.tenant_id,
            is_admin=self.is_admin,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, domain: User) -> "UserModel":
        """도메인 모델을 DB 모델로 변환"""
        return cls(
            id=domain.id,
            email=domain.email,
            name=domain.name,
            password_hash=domain.password_hash,
            tenant_id=domain.tenant_id,
            is_admin=domain.is_admin,
            email_verified=domain.email_verified,
            email_code=domain.email_code,
            email_code_expires_at=domain.email_code_expires_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
