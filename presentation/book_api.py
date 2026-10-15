from fastapi import APIRouter, HTTPException, Response, status

from application.book_service import BookService
from presentation.schemas import BookData, BookResponse, MessageResponse


def create_book_router(service: BookService) -> APIRouter:
    """Создаёт все адреса API для книг."""

    router = APIRouter(prefix="/api/books", tags=["Книги"])

    @router.get(
        "",
        response_model=list[BookResponse],
        summary="Получить список книг",
        description="Возвращает все книги из памяти в виде списка.",
    )
    def get_books():
        return service.get_all_books()

    @router.get(
        "/{book_id}",
        response_model=BookResponse,
        responses={404: {"model": MessageResponse}},
        summary="Получить одну книгу",
        description="Ищет книгу по её номеру и возвращает подробное описание.",
    )
    def get_book(book_id: int):
        book = service.get_book(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book

    @router.post(
        "",
        response_model=BookResponse,
        status_code=status.HTTP_201_CREATED,
        responses={400: {"model": MessageResponse}},
        summary="Добавить книгу",
        description="Создаёт новую книгу. В памяти может быть не больше 50 книг.",
    )
    def create_book(data: BookData):
        try:
            return service.add_book(data.name, data.author, data.description)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @router.put(
        "/{book_id}",
        response_model=BookResponse,
        responses={404: {"model": MessageResponse}},
        summary="Изменить книгу",
        description="Полностью заменяет название, автора и описание книги.",
    )
    def update_book(book_id: int, data: BookData):
        book = service.update_book(
            book_id, data.name, data.author, data.description
        )
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book

    @router.delete(
        "/{book_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={404: {"model": MessageResponse}},
        summary="Удалить книгу",
        description="Удаляет книгу из памяти по её номеру.",
    )
    def delete_book(book_id: int):
        was_deleted = service.delete_book(book_id)
        if not was_deleted:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
