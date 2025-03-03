from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.model.base import Base
from config import DatabaseConfig


class PgSessionManager:
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or self._get_database_url()
        self.engine = self._create_engine()
        self.async_session_maker = async_sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False,
            autoflush=False
        )
    
    def _get_database_url(self) -> str:
        """DatabaseConfig에서 데이터베이스 URL을 가져옵니다"""
        db_host = DatabaseConfig.DB_HOST
        db_port = DatabaseConfig.DB_PORT
        db_name = DatabaseConfig.DB_NAME
        db_user = DatabaseConfig.DB_USER
        db_password = DatabaseConfig.DB_PASSWORD
        
        # 비동기 URL은 'postgresql+asyncpg://' 형태로 시작해야 합니다.
        return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def _create_engine(self):
        """SQLAlchemy 비동기 엔진 생성"""
        return create_async_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
        )
    
    async def get_db(self) -> AsyncSession:
        """비동기 데이터베이스 세션을 제공하는 의존성 함수"""
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def init_db(self) -> None:
        """데이터베이스 초기화 함수"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def close_db(self) -> None:
        """데이터베이스 연결 종료 함수"""
        await self.engine.dispose()


session_manager = PgSessionManager()

async def get_db() -> AsyncSession:
    """비동기 데이터베이스 세션을 제공하는 의존성 함수"""
    async for session in session_manager.get_db():
        yield session