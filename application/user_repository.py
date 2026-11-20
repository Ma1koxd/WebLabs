from abc import ABC, abstractmethod

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def create(self, username: str, password_hash: str) -> User:
        pass
