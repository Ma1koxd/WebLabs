from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from application.book_service import BookService
from infrastructure.memory_book_repository import MemoryBookRepository
from presentation.book_api import create_book_router


app = FastAPI(
    title="Библиотека API",
    description="Простой CRUD web-сервис для лабораторной работы № 2.",
    version="1.0.0",
)

# Здесь соединяются слои приложения.
repository = MemoryBookRepository()
service = BookService(repository)
app.include_router(create_book_router(service))

# Статические HTML, CSS и JS файлы фронтенда.
static_folder = Path(__file__).parent.parent / "static"
app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")
