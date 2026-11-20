from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base


class BookModel(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="book_name_not_empty"),
        CheckConstraint("length(trim(author)) > 0", name="book_author_not_empty"),
        CheckConstraint("length(trim(description)) > 0", name="book_description_not_empty"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
