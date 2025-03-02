# src/domain/tenant.py
from datetime import datetime

from domain.base import BaseDomain


class Tenant(BaseDomain):
    def __init__(self, id: int = None, name: str = None, created_at: datetime = None, updated_at: datetime = None):
        super().__init__(id, created_at, updated_at)
        self.name = name