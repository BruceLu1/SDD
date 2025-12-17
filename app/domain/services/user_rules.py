from app.core.exceptions.domain_exceptions import DuplicateUser
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


def ensure_user_not_exists(user_repo: UserRepository, email: str) -> None:
    if user_repo.get_by_email(email):
        raise DuplicateUser(f"User with email {email} already exists")
