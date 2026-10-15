from domain.book import Book
from domain.book_repository import BookRepository


class BookService:
    """Выполняет основные действия с книгами."""

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_all_books(self) -> list[Book]:
        return self.repository.get_all()

    def get_book(self, book_id: int) -> Book | None:
        return self.repository.get_by_id(book_id)

    def add_book(self, name: str, author: str, description: str) -> Book:
        return self.repository.create(name, author, description)

    def update_book(
        self, book_id: int, name: str, author: str, description: str
    ) -> Book | None:
        return self.repository.update(book_id, name, author, description)

    def delete_book(self, book_id: int) -> bool:
        return self.repository.delete(book_id)
