from app.application.dto.user_dto import CreateUserInput, UserOutput
from app.core.exceptions.application_exceptions import UserNotFound
from app.core.exceptions.domain_exceptions import DuplicateUser
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.user_rules import ensure_user_not_exists
from app.domain.value_objects.email import Email


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, data: CreateUserInput) -> UserOutput:
        ensure_user_not_exists(self._user_repo, data.email)
        user = User(id=None, name=data.name, email=Email(data.email), role=data.role)
        created = self._user_repo.add(user)
        return UserOutput(id=created.id or 0, name=created.name, email=str(created.email), role=created.role)


class ListUsersUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self) -> list[UserOutput]:
        users = self._user_repo.list()
        return [UserOutput(id=user.id or 0, name=user.name, email=str(user.email), role=user.role) for user in users]


class GetUserByEmailUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, email: str) -> UserOutput:
        user = self._user_repo.get_by_email(email)
        if not user:
            raise UserNotFound(f"User with email {email} not found")
        return UserOutput(id=user.id or 0, name=user.name, email=str(user.email), role=user.role)
