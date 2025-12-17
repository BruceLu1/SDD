from abc import ABC, abstractmethod
from typing import Iterable, Optional, Protocol

from app.domain.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Iterable[User]:
        raise NotImplementedError


class UserRepositoryABC(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Iterable[User]:
        raise NotImplementedError
