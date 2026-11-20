from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from application.book_repository import BookRepository
from domain.book import Book
from infrastructure.models import BookModel


def to_book(model: BookModel) -> Book:
    return Book(model.id, model.name, model.author, model.description)


class SqlBookRepository(BookRepository):
    MAX_BOOKS = 50

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Book]:
        models = self.session.scalars(select(BookModel).order_by(BookModel.id)).all()
        return [to_book(model) for model in models]

    def get_by_id(self, book_id: int) -> Book | None:
        model = self.session.get(BookModel, book_id)
        return to_book(model) if model else None

    def create(self, name: str, author: str, description: str) -> Book:
        # Блокировка защищает лимит, если несколько запросов пришли одновременно.
        self.session.execute(text("LOCK TABLE books IN EXCLUSIVE MODE"))
        count = self.session.scalar(select(func.count()).select_from(BookModel))
        if count >= self.MAX_BOOKS:
            raise ValueError("В библиотеке уже 50 книг")

        model = BookModel(name=name, author=author, description=description)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_book(model)

    def update(self, book_id: int, name: str, author: str, description: str) -> Book | None:
        model = self.session.get(BookModel, book_id, with_for_update=True)
        if model is None:
            return None
        model.name = name
        model.author = author
        model.description = description
        self.session.commit()
        return to_book(model)

    def delete(self, book_id: int) -> bool:
        model = self.session.get(BookModel, book_id, with_for_update=True)
        if model is None:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
