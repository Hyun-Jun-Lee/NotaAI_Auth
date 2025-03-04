import os
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.user_api import router as user_router
from api.auth_api import router as auth_router
# from api import project_router, tenent_router

# 데이터베이스 초기화
from db.session import PgSessionManager

# 애플리케이션 생성
app = FastAPI(
    title="NotaAI Auth API",
    description="NotaAI 인증 및 권한 관리 API",
    version="0.1.0",
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화 이벤트 핸들러
@app.on_event("startup")
async def startup_db_client():
    # 데이터베이스 연결 초기화
    session_manager = PgSessionManager()
    await session_manager.init_db()
    app.state.session_manager = session_manager
    print("데이터베이스 연결 초기화 완료")

@app.on_event("shutdown")
async def shutdown_db_client():
    # 데이터베이스 연결 종료
    await app.state.session_manager.close()
    print("데이터베이스 연결 종료")

# 라우터 등록
app.include_router(user_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
# app.include_router(project_router, prefix="/api")
# app.include_router(tenent_router, prefix="/api")