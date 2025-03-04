from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from typing import List

from service.user_service import UserService
from api.dependency import get_user_service
from api.schemas.user_schema import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    PasswordChange,
    EmailVerification
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """모든 사용자 조회"""
    return await user_service.get_all_users(skip, limit)

@router.get("/admins", response_model=List[UserResponse])
async def get_admin_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """관리자 사용자 목록 조회"""
    return await user_service.get_admin_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """특정 사용자 조회"""
    return await user_service.get_user_by_id(user_id)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """새 사용자 생성"""
    return await user_service.create_user(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password,
        tenant_id=user_data.tenant_id,
        is_admin=user_data.is_admin
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """사용자 정보 업데이트"""
    user = await user_service.get_user_by_id(user_id)
    
    if user_data.name:
        user.name = user_data.name
    if user_data.email:
        user.email = user_data.email
    
    return await user_service.update_user(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """사용자 삭제"""
    result = await user_service.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/{user_id}/change-password", response_model=UserResponse)
async def change_password(
    password_data: PasswordChange,
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """비밀번호 변경"""
    return await user_service.change_password(
        user_id=user_id,
        current_password=password_data.current_password,
        new_password=password_data.new_password
    )

@router.post("/{user_id}/email-verification")
async def generate_email_verification(
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """이메일 인증 코드 생성"""
    email_code = await user_service.generate_email_verification_code(user_id)
    return {"message": "Email verification code generated", "email_code": email_code}

@router.post("/{user_id}/verify-email", response_model=UserResponse)
async def verify_user_email(
    verification_data: EmailVerification,
    user_id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
):
    """이메일 인증 수행"""
    return await user_service.verify_email(user_id, verification_data.email_code)

@router.get("/by-tenant/{tenant_id}", response_model=List[UserResponse])
async def get_users_by_tenant(
    tenant_id: int = Path(...),
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """테넌트별 사용자 목록 조회"""
    return await user_service.get_users_by_tenant(tenant_id, skip, limit)

@router.get("/by-email", response_model=UserResponse)
async def get_user_by_email(
    email: str = Query(...),
    user_service: UserService = Depends(get_user_service)
):
    """이메일로 사용자 조회"""
    return await user_service.get_user_by_email(email)