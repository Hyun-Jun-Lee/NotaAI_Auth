from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from service.user_service import UserService
from api.dependency import get_user_service
from api.schemas.auth_schema import Token, SignupRequest, EmailVerificationRequest, ResetPasswordRequest
from api.schemas.user_schema import UserResponse
from auth import create_access_token, get_current_user
from domain import User

router = APIRouter(tags=["Auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    user_service: UserService = Depends(get_user_service)
):
    """새 사용자 가입"""
    try:
        user = await user_service.create_user(
            email=signup_data.email,
            name=signup_data.name,
            password=signup_data.password,
            tenant_id=signup_data.tenant_id,
            is_admin=False
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """사용자 로그인 및 JWT 토큰 발급"""
    try:
        # 사용자 인증
        user = await user_service.authenticate_user(form_data.username, form_data.password)
        
        # 액세스 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "tenant_id": user.tenant_id,
                "is_admin": user.is_admin
            },
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """사용자 로그아웃"""
    # JWT는 서버에 상태를 저장하지 않으므로 클라이언트에서 토큰을 삭제하는 것으로 충분합니다.
    # 실제 구현에서는 토큰 블랙리스트 등을 사용할 수 있습니다.
    return {"message": "로그아웃 되었습니다"}

@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_active_user)
):
    """현재 로그인한 사용자 정보 조회"""
    return current_user

@router.post("/send-email")
async def send_email(
    email_data: EmailVerificationRequest,
    user_service: UserService = Depends(get_user_service)
):
    """이메일 인증 코드 전송"""
    try:
        # 이메일로 사용자 조회
        user = await user_service.get_user_by_email(email_data.email)
        
        # 이메일 인증 코드 생성
        email_code = await user_service.generate_email_verification_code(user.id)
        
        # 실제 구현에서는 이메일 발송 로직 추가
        # 개발 환경에서는 코드를 직접 반환
        return {"message": "이메일 인증 코드가 발송되었습니다", "email_code": email_code}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    verification_data: EmailVerificationRequest,
    code: str,
    user_service: UserService = Depends(get_user_service)
):
    """이메일 인증 수행"""
    try:
        # 이메일로 사용자 조회
        user = await user_service.get_user_by_email(verification_data.email)
        
        # 이메일 인증 수행
        verified_user = await user_service.verify_email(user.id, code)
        return verified_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/request-password-reset")
async def request_password_reset(
    email_data: EmailVerificationRequest,
    user_service: UserService = Depends(get_user_service)
):
    """비밀번호 재설정 요청"""
    try:
        # 이메일로 사용자 조회
        user = await user_service.get_user_by_email(email_data.email)
        
        # 비밀번호 재설정 코드 생성
        reset_code = await user_service.generate_email_verification_code(user.id)
        
        # 실제 구현에서는 이메일 발송 로직 추가
        # 개발 환경에서는 코드를 직접 반환
        return {"message": "비밀번호 재설정 코드가 발송되었습니다", "reset_code": reset_code}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/reset-password", response_model=UserResponse)
async def reset_password(
    reset_data: ResetPasswordRequest,
    user_service: UserService = Depends(get_user_service)
):
    """비밀번호 재설정 수행"""
    try:
        # 이메일로 사용자 조회
        user = await user_service.get_user_by_email(reset_data.email)
        
        # 코드 검증 및 비밀번호 재설정
        if not await user_service.verify_email_code(user.id, reset_data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 코드입니다"
            )
        
        # 비밀번호 변경
        updated_user = await user_service.reset_password(user.id, reset_data.new_password)
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )