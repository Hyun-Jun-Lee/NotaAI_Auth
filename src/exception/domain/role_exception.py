
class InvalidRoleException(Exception):
    """유효하지 않은 역할이 있는 경우 발생하는 예외"""
    def __init__(self, role: str = None):
        super().__init__(f"Invalid role: {role}")

class UnauthorizedAccessException(Exception):
    """사용자가 권한이 없는 경우 발생하는 예외"""
    def __init__(self, user_id: str, action: str):
        self.user_id = user_id
        self.action = action
        super().__init__(f"User {user_id} is not authorized to perform {action}")