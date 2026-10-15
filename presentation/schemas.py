from pydantic import BaseModel, Field


class BookData(BaseModel):
    """Данные, которые пользователь вводит для книги."""

    name: str = Field(min_length=1, max_length=100, examples=["Маленький принц"])
    author: str = Field(min_length=1, max_length=100, examples=["Антуан де Сент-Экзюпери"])
    description: str = Field(
        min_length=1,
        max_length=1000,
        examples=["Сказка о дружбе, любви и ответственности."],
    )


class BookResponse(BookData):
    """Книга, которую сервер возвращает клиенту."""

    id: int


class MessageResponse(BaseModel):
    detail: str
