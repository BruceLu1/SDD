from dataclasses import dataclass
from app.core.enums.user_role import UserRole


@dataclass
class CreateUserInput:
    name: str
    email: str
    role: UserRole = UserRole.MEMBER


@dataclass
class UserOutput:
    id: int
    name: str
    email: str
    role: UserRole
