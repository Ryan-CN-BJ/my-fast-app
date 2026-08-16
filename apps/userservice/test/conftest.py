import os
import sys
from contextlib import contextmanager
from pathlib import Path

import psycopg2
import psycopg2.sql
from alembic import command
from alembic.config import Config

import signal
import subprocess
import time
from subprocess import Popen
import pytest

# SRC_DIR = Path(__file__).resolve().parent.parent / "src"
# if str(SRC_DIR) not in sys.path:
#     sys.path.insert(0, str(SRC_DIR))

PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR.parent.parent / ".env"


def _load_db_env():
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key.startswith("DB_") and key not in os.environ:
                os.environ[key] = value


_load_db_env()
TEST_DB_NAME = os.environ.get("TEST_DB_NAME", "my_test_db")
os.environ["DB_NAME"] = TEST_DB_NAME

from userservice.core.config.dbconfig import dbSetting  # noqa: E402


def pytest_sessionstart(session):
    recreate_database()
    run_alembic_migration()
    _start_server()


def pytest_sessionfinish(session, exitstatus):
    drop_database()
    _stop_server()


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
        yield conn
    finally:
        conn.close()


def _drop_database(conn):
    db_ident = psycopg2.sql.Identifier(dbSetting.name)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = %s "
            "AND pid <> pg_backend_pid()",
            (dbSetting.name,),
        )
        cur.execute(psycopg2.sql.SQL("DROP DATABASE IF EXISTS {}").format(db_ident))


def drop_database():
    with maintenance_connection() as conn:
        _drop_database(conn)


server_port = "18000"

_server_process: Popen | None = None
_log_file = None


def _start_server():
    global server_port, _log_file, _server_process

    tmp_dir = Path(__file__).resolve().parent.parent.parent / "temp"
    tmp_dir.mkdir(exist_ok=True)
    _log_file = open(tmp_dir / "test_server.log", "w")
    _server_process = subprocess.Popen(
        [
            "uv",
            "run",
            "--package",
            "userservice",
            "fastapi",
            "dev",
            "apps/userservice/src/userservice/main.py",
            "--port",
            server_port,
        ],
        shell=False,
        # start_new_session=True,
        stdout=_log_file,
    )

    import httpx

    for _ in range(50):
        try:
            res = httpx.get(
                f"http://localhost:{server_port}/docs",
                trust_env=False,
                timeout=2,
            )
            if res.status_code == 200:
                break
        except Exception as e:
            pass
        time.sleep(0.1)
    else:
        raise RuntimeError("测试服务器启动失败！")


def _stop_server():
    global _server_process, _log_file
    if _server_process is not None:
        _server_process.terminate()
        _server_process.wait(timeout=10)
        # try:
        #     os.killpg(_server_process.pid, signal.SIGTERM)
        #     _server_process.wait(timeout=10)
        #     _server_process = None
        # except Exception as e:
        #     os.killpg(_server_process.pid, signal.SIGKILL)
    if _log_file is not None:
        _log_file.close()
        _log_file = None


def recreate_database():
    with maintenance_connection() as conn:
        _drop_database(conn)
        with conn.cursor() as cur:
            cur.execute(
                psycopg2.sql.SQL("CREATE DATABASE {}").format(
                    psycopg2.sql.Identifier(dbSetting.name)
                )
            )


def run_alembic_migration():
    cfg = Config(str(PROJECT_DIR / "alembic.ini"))
    command.upgrade(cfg, "head")


from userservice.core.db import get_db
from sqlalchemy import text


@pytest.fixture
async def db_session():
    from userservice.core.db import get_db

    async for db in get_db():
        yield db
        break


@pytest.fixture(autouse=True)
async def clean_database(db_session):
    result = await db_session.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    )
    tables = [row[0] for row in result.fetchall()]

    # 清除所有表数据
    for table in tables:
        await db_session.execute(text(f'TRUNCATE TABLE "{table}" CASCADE'))
    yield  # 执行测试
