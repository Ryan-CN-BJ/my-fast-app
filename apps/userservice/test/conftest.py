import os
import sys
from pathlib import Path

import psycopg2
import psycopg2.sql
from alembic import command
from alembic.config import Config

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

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

from core.config.dbconfig import dbSetting  # noqa: E402


def pytest_sessionstart(session):
    recreate_database()
    run_alembic_migration()


def pytest_sessionfinish(session, exitstatus):
    print("pytest_sessionend+++++++")


def recreate_database():
    conn = psycopg2.connect(
        user=dbSetting.user,
        password=dbSetting.password,
        host=dbSetting.host,
        port=dbSetting.port,
        dbname="postgres",
    )
    conn.autocommit = True
    db_ident = psycopg2.sql.Identifier(dbSetting.name)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                "WHERE pg_stat_activity.datname = %s "
                "AND pid <> pg_backend_pid()",
                (dbSetting.name,),
            )
            cur.execute(
                psycopg2.sql.SQL(f"DROP DATABASE IF EXISTS {dbSetting.name}").format(
                    db_ident
                )
            )
            cur.execute(
                psycopg2.sql.SQL(f"CREATE DATABASE {dbSetting.name}").format(db_ident)
            )
    finally:
        conn.close()


def run_alembic_migration():
    cfg = Config(str(PROJECT_DIR / "alembic.ini"))
    command.upgrade(cfg, "head")
