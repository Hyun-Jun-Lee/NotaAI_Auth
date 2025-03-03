from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.model.base import BaseDBModel
from domain import Project, ProjectMember


class ProjectModel(BaseDBModel):
    
    __tablename__ = "project"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenant.id"), nullable=False)
    
    owner = relationship("UserModel", foreign_keys=[owner_id])
    tenant = relationship("TenantModel", back_populates="projects")
    members = relationship("ProjectMemberModel", back_populates="project", cascade="all, delete-orphan")
    
    def to_domain(self) -> Project:
        """DB 모델을 도메인 모델로 변환"""
        project = Project(
            id=self.id,
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            tenant_id=self.tenant_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
        
        # 프로젝트 멤버 변환
        if self.members:
            project.members = [member.to_domain() for member in self.members]
        
        return project
    
    @classmethod
    def from_domain(cls, domain: Project) -> "ProjectModel":
        """도메인 모델을 DB 모델로 변환"""
        return cls(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            owner_id=domain.owner_id,
            tenant_id=domain.tenant_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )

class ProjectMemberModel(BaseDBModel):
    
    __tablename__ = "project_member"
    
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    role = Column(String(50), nullable=False)
    invited_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    project = relationship("ProjectModel", back_populates="members")
    user = relationship("UserModel", foreign_keys=[user_id], back_populates="project_members")
    inviter = relationship("UserModel", foreign_keys=[invited_by])
    
    def to_domain(self) -> ProjectMember:
        """DB 모델을 도메인 모델로 변환"""
        return ProjectMember(
            id=self.id,
            project_id=self.project_id,
            user_id=self.user_id,
            role=self.role,
            invited_by=self.invited_by,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, domain: ProjectMember) -> "ProjectMemberModel":
        """도메인 모델을 DB 모델로 변환"""
        return cls(
            id=domain.id,
            project_id=domain.project_id,
            user_id=domain.user_id,
            role=domain.role,
            invited_by=domain.invited_by,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )