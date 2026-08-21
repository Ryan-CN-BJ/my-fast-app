import pytest
from userservice.main import app
from httpx import AsyncClient, ASGITransport

from pathlib import Path
import os
import psycopg2
import psycopg2.sql
from contextlib import contextmanager
from alembic.config import Config
from alembic import command


# 加载环境变量
def _load_env():
    _env_file = Path(__file__).parent.parent.parent.parent.parent / ".env"
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if (
            not line
            or line.startswith("#")
            or "=" not in line
            or not line.startswith("DB")
        ):
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        os.environ[key] = value


_load_env()

os.environ["DB_NAME"] = "my_test_db"
from userservice.core.config.dbconfig import DbSetting

dbSetting = DbSetting()


# 创建数据库同步连接
@contextmanager
def maintenance_connection():
    conn = psycopg2.connect(
        user=dbSetting.user,
        password=dbSetting.password,
        host=dbSetting.host,
        port=dbSetting.port,
        dbname="postgres",
    )
    conn.autocommit = True
    try:
        yield conn.cursor()
    finally:
        conn.close()  # 保证连接关闭


# 创建测试数据库
def _create_test_db():
    _del_test_db()
    with maintenance_connection() as cur:
        cur.execute(
            psycopg2.sql.SQL("CREATE DATABASE {}").format(
                psycopg2.sql.Identifier(dbSetting.name)
            )
        )


# 删除测试数据库
def _del_test_db():
    db_ident = psycopg2.sql.Identifier(dbSetting.name)
    with maintenance_connection() as cur:
        cur.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = %s "
            "AND pid <> pg_backend_pid()",
            (dbSetting.name,),
        )
        cur.execute(psycopg2.sql.SQL("DROP DATABASE IF EXISTS {}").format(db_ident))


# 数据库升级
def _upgrade_db():
    PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
    cfg = Config(str(PROJECT_DIR / "alembic.ini"))
    command.upgrade(cfg, "head")


def pytest_sessionstart(session):
    _create_test_db()
    _upgrade_db()


def pytest_sessionfinish(session):
    _del_test_db()


# 清除数据库表数据

from userservice.core.db import get_session_factory
from sqlalchemy import text


@pytest.fixture(autouse=True)
async def clean_db():
    async with get_session_factory().begin() as session:
        result = await session.execute(
            text(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public' "
                "AND tablename != 'alembic_version'"
            )
        )
        tables = [row[0] for row in result.fetchall()]
        for table in tables:
            await session.execute(text(f'TRUNCATE TABLE "{table}" CASCADE'))


# 启动服务器
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
