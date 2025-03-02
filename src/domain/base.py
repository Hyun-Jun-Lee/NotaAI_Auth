from datetime import datetime
from typing import Any

class BaseDomain:
    def __init__(self, id: int = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at

    def update_timestamp(self) -> None:
        """엔티티의 업데이트 시간을 현재 시간으로 설정합니다."""
        self.updated_at = datetime.now()