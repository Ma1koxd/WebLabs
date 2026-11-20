from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from application.user_repository import UserRepository
from domain.user import User
from infrastructure.security import create_token, verify_password
from presentation.schemas import MessageResponse, TokenResponse, UserResponse


def create_auth_router(user_repository_provider, current_user_provider) -> APIRouter:
    router = APIRouter(prefix="/api/auth", tags=["Вход"])

    @router.post(
        "/token",
        response_model=TokenResponse,
        responses={401: {"model": MessageResponse}},
        summary="Войти и получить токен",
        description="Принимает логин и пароль формы. Токен действует один час.",
    )
    def login(
        form: OAuth2PasswordRequestForm = Depends(),
        repository: UserRepository = Depends(user_repository_provider),
    ):
        user = repository.get_by_username(form.username)
        if user is None or not verify_password(form.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": create_token(user.id), "token_type": "bearer"}

    @router.get(
        "/me",
        response_model=UserResponse,
        responses={401: {"model": MessageResponse}},
        summary="Получить текущего пользователя",
    )
    def me(user: User = Depends(current_user_provider)):
        return user

    return router
