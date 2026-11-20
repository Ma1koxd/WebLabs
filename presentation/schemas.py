from pydantic import BaseModel, ConfigDict, Field


class BookData(BaseModel):
    """Данные, которые пользователь вводит для книги."""

    model_config = ConfigDict(str_strip_whitespace=True)

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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
