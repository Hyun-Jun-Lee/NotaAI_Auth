# src/domain/tenant.py
from typing import List, Optional
from datetime import datetime

from domain.base import BaseDomain


class Tenant(BaseDomain):
    def __init__(self, name: str = None, created_at: datetime = None):
        self.name = name