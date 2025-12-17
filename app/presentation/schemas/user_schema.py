from pydantic import BaseModel, EmailStr
from app.core.enums.user_role import UserRole


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.MEMBER


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
