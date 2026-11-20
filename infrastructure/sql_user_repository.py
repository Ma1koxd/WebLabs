from sqlalchemy import select
from sqlalchemy.orm import Session

from application.user_repository import UserRepository
from domain.user import User
from infrastructure.models import UserModel


def to_user(model: UserModel) -> User:
    return User(model.id, model.username, model.password_hash)


class SqlUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        model = self.session.scalar(select(UserModel).where(UserModel.username == username))
        return to_user(model) if model else None

    def get_by_id(self, user_id: int) -> User | None:
        model = self.session.get(UserModel, user_id)
        return to_user(model) if model else None

    def create(self, username: str, password_hash: str) -> User:
        model = UserModel(username=username, password_hash=password_hash)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_user(model)
