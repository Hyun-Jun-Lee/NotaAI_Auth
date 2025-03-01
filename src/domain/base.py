from datetime import datetime

class BaseDomain:
    def __init__(self, id: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def update_timestamps(self) -> None:
        self.updated_at = datetime.now()