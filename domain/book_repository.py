from abc import ABC, abstractmethod

from domain.book import Book


class BookRepository(ABC):
    """Описывает, что должно уметь хранилище книг."""

    @abstractmethod
    def get_all(self) -> list[Book]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Book | None:
        pass

    @abstractmethod
    def create(self, name: str, author: str, description: str) -> Book:
        pass

    @abstractmethod
    def update(
        self, book_id: int, name: str, author: str, description: str
    ) -> Book | None:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass
