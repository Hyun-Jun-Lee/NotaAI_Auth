from exception.base import DomainException


class ProjectException(DomainException):
    """프로젝트 관련 기본 예외 클래스"""
    pass


class ProjectNotFoundException(ProjectException):
    """프로젝트를 찾을 수 없는 경우 발생하는 예외"""
    
    def __init__(self, project_id: str = None, name: str = None):
        if project_id:
            message = f"ID가 '{project_id}'인 프로젝트를 찾을 수 없습니다."
        elif name:
            message = f"이름이 '{name}'인 프로젝트를 찾을 수 없습니다."
        else:
            message = "프로젝트를 찾을 수 없습니다."
        super().__init__(message)


class ProjectAlreadyExistsException(ProjectException):
    """프로젝트가 이미 존재하는 경우 발생하는 예외"""
    
    def __init__(self, name: str = None):
        if name:
            message = f"이름이 '{name}'인 프로젝트가 이미 존재합니다."
        else:
            message = "프로젝트가 이미 존재합니다."
        super().__init__(message)


class ProjectMemberNotFoundException(ProjectException):
    """프로젝트 멤버를 찾을 수 없는 경우 발생하는 예외"""
    
    def __init__(self, member_id: str = None, user_id: str = None, project_id: str = None):
        if member_id:
            message = f"ID가 '{member_id}'인 프로젝트 멤버를 찾을 수 없습니다."
        elif user_id and project_id:
            message = f"프로젝트 '{project_id}'에 사용자 '{user_id}'가 멤버로 존재하지 않습니다."
        else:
            message = "프로젝트 멤버를 찾을 수 없습니다."
        super().__init__(message)


class ProjectMemberAlreadyExistsException(ProjectException):
    """프로젝트 멤버가 이미 존재하는 경우 발생하는 예외"""
    
    def __init__(self, user_id: str = None, project_id: str = None):
        if user_id and project_id:
            message = f"사용자 '{user_id}'는 이미 프로젝트 '{project_id}'의 멤버입니다."
        else:
            message = "사용자가 이미 프로젝트의 멤버입니다."
        super().__init__(message)