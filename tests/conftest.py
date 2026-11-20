import os
from pathlib import Path

import pytest
from sqlalchemy.engine import make_url


# Тесты очищают только отдельную тестовую БД, никогда не основную library.
test_url = os.getenv("TEST_DATABASE_URL", "")
if not test_url or not (make_url(test_url).database or "").endswith("_test"):
    raise pytest.UsageError("Укажите TEST_DATABASE_URL для отдельной PostgreSQL БД с окончанием _test")
if make_url(test_url).get_backend_name() != "postgresql":
    raise pytest.UsageError("Тесты нужно запускать на PostgreSQL")

os.environ["DATABASE_URL"] = test_url
os.environ["JWT_SECRET"] = "test-secret-only-for-automated-tests-123456789"
os.environ["SEED_USERNAME"] = "student"
os.environ["SEED_PASSWORD"] = "student12345"

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from infrastructure.database import engine, SessionLocal
from infrastructure.security import hash_password
from infrastructure.sql_user_repository import SqlUserRepository


@pytest.fixture(scope="session", autouse=True)
def migrate():
    config = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))
    command.upgrade(config, "head")
    yield
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_database(migrate):
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE books, users RESTART IDENTITY"))


@pytest.fixture
def client():
    with SessionLocal() as session:
        SqlUserRepository(session).create("student", hash_password("student12345"))
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/api/auth/token", data={"username": "student", "password": "student12345"}
    )
    assert response.status_code == 200
    return {"Authorization": "Bearer " + response.json()["access_token"]}
