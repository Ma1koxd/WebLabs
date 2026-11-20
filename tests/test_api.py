import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import jwt

from infrastructure.database import SessionLocal, engine
from infrastructure.sql_book_repository import SqlBookRepository
from infrastructure.sql_user_repository import SqlUserRepository
from scripts.seed import main as seed


BOOK = {"name": "Тестовая книга", "author": "Автор", "description": "Описание книги"}


def test_pages_and_swagger(client):
    for url in ["/", "/add.html", "/details.html?id=1", "/login.html", "/docs", "/health"]:
        assert client.get(url).status_code == 200
    schema = client.get("/openapi.json").json()
    for path in ["/api/books", "/api/books/{book_id}", "/api/auth/token", "/api/auth/me"]:
        assert path in schema["paths"]
        for operation in schema["paths"][path].values():
            assert operation.get("summary")
    assert schema["paths"]["/api/books"]["post"]["security"]


def test_writes_need_authentication(client):
    assert client.get("/api/books").status_code == 200
    assert client.post("/api/books", json=BOOK).status_code == 401
    assert client.put("/api/books/1", json=BOOK).status_code == 401
    assert client.delete("/api/books/1").status_code == 401
    assert client.get("/api/auth/me").status_code == 401
    response = client.post("/api/auth/token", data={"username": "student", "password": "wrong"})
    assert response.status_code == 401


def test_crud_and_persistence(client, auth_headers):
    created = client.post("/api/books", json=BOOK, headers=auth_headers)
    assert created.status_code == 201
    book_id = created.json()["id"]
    assert client.get(f"/api/books/{book_id}").json()["name"] == BOOK["name"]

    changed = {**BOOK, "description": "Изменённое описание"}
    assert client.put(f"/api/books/{book_id}", json=changed, headers=auth_headers).status_code == 200
    # Закрываем соединения: данные остаются в PostgreSQL, а не в объекте Python.
    engine.dispose()
    assert client.get(f"/api/books/{book_id}").json()["description"] == changed["description"]

    deleted = client.delete(f"/api/books/{book_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/api/books/{book_id}").status_code == 404
    assert client.put(f"/api/books/{book_id}", json=BOOK, headers=auth_headers).status_code == 404
    assert client.delete(f"/api/books/{book_id}", headers=auth_headers).status_code == 404


def test_user_response_does_not_expose_password(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert set(response.json()) == {"id", "username"}


def test_bad_and_expired_tokens(client):
    secret = os.environ["JWT_SECRET"]
    expired = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(seconds=1)}, secret, algorithm="HS256"
    )
    missing_exp = jwt.encode({"sub": "1"}, secret, algorithm="HS256")
    for token in ["not-a-token", expired, missing_exp]:
        assert client.post("/api/books", json=BOOK, headers={"Authorization": "Bearer " + token}).status_code == 401


def test_validation(client, auth_headers):
    for invalid in [{}, {**BOOK, "name": "   "}, {**BOOK, "name": "x" * 101}]:
        assert client.post("/api/books", json=invalid, headers=auth_headers).status_code == 422


def test_limit_with_simultaneous_requests(client, auth_headers):
    with SessionLocal() as session:
        repository = SqlBookRepository(session)
        for i in range(49):
            repository.create(f"Книга {i}", "Автор", "Описание")

    def create_one(i):
        return client.post("/api/books", json={**BOOK, "name": f"Одновременно {i}"}, headers=auth_headers).status_code

    with ThreadPoolExecutor(max_workers=4) as pool:
        codes = list(pool.map(create_one, range(4)))
    assert sorted(codes) == [201, 400, 400, 400]
    assert len(client.get("/api/books").json()) == 50


def test_seed_can_be_run_twice():
    seed()
    with SessionLocal() as session:
        books = SqlBookRepository(session)
        first = books.get_all()[0]
        books.update(first.id, "Моё изменение", first.author, first.description)
        original_hash = SqlUserRepository(session).get_by_username("student").password_hash
    seed()
    with SessionLocal() as session:
        assert len(SqlBookRepository(session).get_all()) == 5
        assert SqlBookRepository(session).get_all()[0].name == "Моё изменение"
        assert SqlUserRepository(session).get_by_username("student").password_hash == original_hash


def test_seed_keeps_an_empty_library_after_user_deleted_books():
    seed()
    with SessionLocal() as session:
        repository = SqlBookRepository(session)
        for book in repository.get_all():
            repository.delete(book.id)
    seed()
    with SessionLocal() as session:
        assert SqlBookRepository(session).get_all() == []
