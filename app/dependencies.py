import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.book_service import BookService
from application.user_repository import UserRepository
from domain.user import User
from infrastructure.database import SessionLocal
from infrastructure.security import read_token
from infrastructure.sql_book_repository import SqlBookRepository
from infrastructure.sql_user_repository import SqlUserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_session():
    # Каждый HTTP-запрос получает свою сессию. В конце она закрывается.
    with SessionLocal() as session:
        yield session


def get_book_service(session: Session = Depends(get_session)) -> BookService:
    return BookService(SqlBookRepository(session))


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return SqlUserRepository(session)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    error = HTTPException(
        status_code=401,
        detail="Нужно войти в систему",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = read_token(token)
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise error from None
    user = repository.get_by_id(user_id)
    if user is None:
        raise error
    return user
