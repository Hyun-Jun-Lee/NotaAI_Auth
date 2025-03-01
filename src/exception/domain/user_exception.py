from exception.base import DomainException


class EmailCodeException(DomainException):
    """이메일 코드 관련 기본 예외 클래스"""
    pass


class EmailCodeNotGeneratedException(EmailCodeException):
    """이메일 코드가 생성되지 않은 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "이메일 인증 코드가 생성되지 않았습니다.")


class EmailCodeExpiredException(EmailCodeException):
    """이메일 코드가 만료된 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "이메일 인증 코드가 만료되었습니다.")


class EmailCodeMismatchException(EmailCodeException):
    """이메일 코드가 일치하지 않는 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "이메일 인증 코드가 일치하지 않습니다.")


class UserNotFoundException(DomainException):
    """사용자를 찾을 수 없는 경우 발생하는 예외"""
    
    def __init__(self, user_id: str = None, email: str = None):
        if user_id:
            message = f"ID가 '{user_id}'인 사용자를 찾을 수 없습니다."
        elif email:
            message = f"이메일이 '{email}'인 사용자를 찾을 수 없습니다."
        else:
            message = "사용자를 찾을 수 없습니다."
        super().__init__(message)


class InvalidPasswordException(DomainException):
    """비밀번호가 유효하지 않은 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "비밀번호가 유효하지 않습니다.")


class UserInactiveException(DomainException):
    """사용자 계정이 비활성화된 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "사용자 계정이 비활성화되었습니다.")


class EmailNotVerifiedException(DomainException):
    """이메일이 인증되지 않은 경우 발생하는 예외"""
    
    def __init__(self, message: str = None):
        super().__init__(message or "이메일이 인증되지 않았습니다.")


class RoleException(DomainException):
    """역할 관련 기본 예외 클래스"""
    pass


class RoleNotFoundException(RoleException):
    """시스템에 역할이 존재하지 않는 경우 발생하는 예외"""
    
    def __init__(self, role: str):
        super().__init__(f"'{role}' 역할이 시스템에 존재하지 않습니다.")


class UserRoleNotFoundException(RoleException):
    """사용자에게 역할이 없는 경우 발생하는 예외"""
    
    def __init__(self, role: str):
        super().__init__(f"사용자에게 '{role}' 역할이 없습니다.")


class UserAlreadyExistsException(DomainException):
    """사용자가 이미 존재하는 경우 발생하는 예외"""
    
    def __init__(self, email: str = None):
        if email:
            message = f"이메일이 '{email}'인 사용자가 이미 존재합니다."
        else:
            message = "사용자가 이미 존재합니다."
        super().__init__(message)