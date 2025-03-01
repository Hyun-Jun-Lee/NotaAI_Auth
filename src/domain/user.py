from typing import List

class User:
    def __init__(self, id: str, email: str, password_hash: str, tenant_id: str, roles: List[str]):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.tenant_id = tenant_id
        self.roles = roles