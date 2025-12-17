from fastapi import APIRouter

from app.presentation.controllers.user_controller import UserController
from app.presentation.schemas.user_schema import UserCreateSchema, UserResponseSchema


def get_user_router(controller: UserController) -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("", response_model=UserResponseSchema, status_code=201)
    def create_user(payload: UserCreateSchema):
        return controller.create(payload)

    @router.get("", response_model=list[UserResponseSchema])
    def list_users():
        return controller.list()

    @router.get("/{email}", response_model=UserResponseSchema)
    def get_user(email: str):
        return controller.get_by_email(email)

    return router
