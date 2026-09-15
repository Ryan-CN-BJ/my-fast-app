from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from userservice.core.config.dbconfig import dbSetting
from collections.abc import AsyncGenerator

from sqlalchemy import event
import time

from userservice.core.config.logConfig import logSetting

_engine: AsyncEngine | None = None


def _register_db_events(engine: AsyncEngine) -> None:
    from userservice.core.logger.db_log import DBLog

    @event.listens_for(engine.sync_engine, "before_cursor_execute", named=True)
    def _before_cursor_execute(context, **kw):
        context._query_start_time = time.perf_counter()

    @event.listens_for(engine.sync_engine, "after_cursor_execute", named=True)
    def _after_cursor_execute(context, **kw):
        _query_start_time = context._query_start_time
        duration_ms = (time.perf_counter() - _query_start_time) * 1000
        if duration_ms > logSetting.slow_query_threshold:
            DBLog(
                message="慢查询",
                duration_ms=duration_ms,
            )


def get_async_engine():
    global _engine
    if _engine is None:
        url = f"postgresql+asyncpg://{dbSetting.user}:{dbSetting.password}@{dbSetting.host}:{dbSetting.port}/{dbSetting.name}"
        _engine = create_async_engine(
            url, pool_size=10, max_overflow=20, pool_pre_ping=True, echo=False
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


# async def get_db() -> AsyncGenerator[AsyncSession]:
#     async with get_session_factory().begin() as session:
#         yield session


async def get_db() -> AsyncGenerator[AsyncSession]:
    session = get_session_factory()()
    session.begin()
    try:
        yield session
    except:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()
