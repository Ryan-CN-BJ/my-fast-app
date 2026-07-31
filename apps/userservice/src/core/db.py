from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from core.config.dbconfig import dbSetting
from collections.abc import AsyncGenerator

_engine: AsyncEngine | None = None


def get_async_engine():
    global _engine
    if _engine is None:
        url = f"postgresql+asyncpg://{dbSetting.user}:{dbSetting.password}@{dbSetting.host}:{dbSetting.port}/{dbSetting.name}"
        _engine = create_async_engine(
            url, pool_size=10, max_overflow=20, pool_pre_ping=True, echo=True
        )
    return _engine


_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_async_engine(), expire_on_commit=False, autoflush=True
        )
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with get_session_factory().begin() as session:
        yield session
