from domain.book import Book
from domain.book_repository import BookRepository


class MemoryBookRepository(BookRepository):
    """Хранит книги в обычном списке, пока программа запущена."""

    MAX_BOOKS = 50

    def __init__(self):
        self.books: list[Book] = []
        self.next_id = 1

        # Две начальные записи помогают сразу увидеть работу приложения.
        self.create(
            "Мастер и Маргарита",
            "Михаил Булгаков",
            "Роман о любви, добре, зле и необычных событиях в Москве.",
        )
        self.create(
            "Преступление и наказание",
            "Фёдор Достоевский",
            "Роман о Раскольникове, его преступлении и раскаянии.",
        )

    def get_all(self) -> list[Book]:
        return self.books.copy()

    def get_by_id(self, book_id: int) -> Book | None:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def create(self, name: str, author: str, description: str) -> Book:
        if len(self.books) >= self.MAX_BOOKS:
            raise ValueError("В библиотеке уже 50 книг")

        book = Book(
            id=self.next_id,
            name=name,
            author=author,
            description=description,
        )
        self.books.append(book)
        self.next_id += 1
        return book

    def update(
        self, book_id: int, name: str, author: str, description: str
    ) -> Book | None:
        book = self.get_by_id(book_id)
        if book is None:
            return None

        book.name = name
        book.author = author
        book.description = description
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book is None:
            return False

        self.books.remove(book)
        return True
