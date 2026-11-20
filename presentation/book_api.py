from fastapi import APIRouter, Depends, HTTPException, Response, status

from application.book_service import BookService
from presentation.schemas import BookData, BookResponse, MessageResponse


def create_book_router(service_provider, current_user_provider) -> APIRouter:
    """Создаёт все адреса API для книг."""

    router = APIRouter(prefix="/api/books", tags=["Книги"])

    @router.get(
        "",
        response_model=list[BookResponse],
        summary="Получить список книг",
        description="Возвращает все книги из PostgreSQL. Вход не требуется.",
    )
    def get_books(service: BookService = Depends(service_provider)):
        return service.get_all_books()

    @router.get(
        "/{book_id}",
        response_model=BookResponse,
        responses={404: {"model": MessageResponse}},
        summary="Получить одну книгу",
        description="Ищет книгу по её номеру и возвращает подробное описание.",
    )
    def get_book(book_id: int, service: BookService = Depends(service_provider)):
        book = service.get_book(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book

    @router.post(
        "",
        response_model=BookResponse,
        status_code=status.HTTP_201_CREATED,
        responses={400: {"model": MessageResponse}, 401: {"model": MessageResponse}},
        summary="Добавить книгу",
        description="Создаёт книгу в PostgreSQL. Лимит — 50 книг. Нужен Bearer-токен.",
        dependencies=[Depends(current_user_provider)],
    )
    def create_book(data: BookData, service: BookService = Depends(service_provider)):
        try:
            return service.add_book(data.name, data.author, data.description)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @router.put(
        "/{book_id}",
        response_model=BookResponse,
        responses={404: {"model": MessageResponse}, 401: {"model": MessageResponse}},
        summary="Изменить книгу",
        description="Полностью заменяет название, автора и описание книги.",
        dependencies=[Depends(current_user_provider)],
    )
    def update_book(book_id: int, data: BookData, service: BookService = Depends(service_provider)):
        book = service.update_book(
            book_id, data.name, data.author, data.description
        )
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book

    @router.delete(
        "/{book_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={404: {"model": MessageResponse}, 401: {"model": MessageResponse}},
        summary="Удалить книгу",
        description="Удаляет книгу из PostgreSQL по её номеру. Требуется вход.",
        dependencies=[Depends(current_user_provider)],
    )
    def delete_book(book_id: int, service: BookService = Depends(service_provider)):
        was_deleted = service.delete_book(book_id)
        if not was_deleted:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
