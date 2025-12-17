from collections.abc import Iterable
from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions.infrastructure_exceptions import DBConnectionError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.infrastructure.db.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def add(self, user: User) -> User:
        try:
            with self._session_factory() as session:
                db_user = UserModel(name=user.name, email=str(user.email), role=user.role)
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
                return User(id=db_user.id, name=db_user.name, email=Email(db_user.email), role=db_user.role)
        except Exception as exc:  # pragma: no cover - infrastructure guardrail
            raise DBConnectionError(str(exc)) from exc

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            with self._session_factory() as session:
                db_user = session.query(UserModel).filter(UserModel.email == email).first()
                if not db_user:
                    return None
                return User(id=db_user.id, name=db_user.name, email=Email(db_user.email), role=db_user.role)
        except Exception as exc:  # pragma: no cover
            raise DBConnectionError(str(exc)) from exc

    def list(self) -> Iterable[User]:
        try:
            with self._session_factory() as session:
                db_users = session.query(UserModel).all()
                return [User(id=u.id, name=u.name, email=Email(u.email), role=u.role) for u in db_users]
        except Exception as exc:  # pragma: no cover
            raise DBConnectionError(str(exc)) from exc
