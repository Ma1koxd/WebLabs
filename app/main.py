from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.dependencies import get_book_service, get_current_user, get_user_repository
from infrastructure.database import SessionLocal
from infrastructure.security import get_jwt_secret
from presentation.auth_api import create_auth_router
from presentation.book_api import create_book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_jwt_secret()
    yield


app = FastAPI(
    title="Библиотека API",
    description="Библиотека: PostgreSQL, SQLAlchemy и JWT. Лабораторная работа № 3.",
    version="3.0.0",
    lifespan=lifespan,
)

# Здесь соединяются слои приложения.
app.include_router(create_book_router(get_book_service, get_current_user))
app.include_router(create_auth_router(get_user_repository, get_current_user))


@app.get("/health", tags=["Сервис"], summary="Проверить соединение с БД")
def health():
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return {"status": "ok"}

# Статические HTML, CSS и JS файлы фронтенда.
static_folder = Path(__file__).parent.parent / "static"
app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")
