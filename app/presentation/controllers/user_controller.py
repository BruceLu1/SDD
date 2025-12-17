from fastapi import HTTPException, status

from app.application.dto.user_dto import CreateUserInput
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByEmailUseCase,
    ListUsersUseCase,
)
from app.core.exceptions.application_exceptions import UserNotFound
from app.core.exceptions.domain_exceptions import DuplicateUser, InvalidEmail
from app.presentation.schemas.user_schema import UserCreateSchema, UserResponseSchema


class UserController:
    def __init__(
        self,
        create_use_case: CreateUserUseCase,
        list_use_case: ListUsersUseCase,
        get_use_case: GetUserByEmailUseCase,
    ) -> None:
        self._create_use_case = create_use_case
        self._list_use_case = list_use_case
        self._get_use_case = get_use_case

    def create(self, payload: UserCreateSchema) -> UserResponseSchema:
        try:
            result = self._create_use_case.execute(CreateUserInput(**payload.dict()))
            return UserResponseSchema(**result.__dict__)
        except DuplicateUser as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
        except InvalidEmail as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    def list(self) -> list[UserResponseSchema]:
        results = self._list_use_case.execute()
        return [UserResponseSchema(**res.__dict__) for res in results]

    def get_by_email(self, email: str) -> UserResponseSchema:
        try:
            result = self._get_use_case.execute(email)
            return UserResponseSchema(**result.__dict__)
        except UserNotFound as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
