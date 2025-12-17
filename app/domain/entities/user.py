from dataclasses import dataclass
from typing import Optional

from app.core.enums.user_role import UserRole
from app.domain.value_objects.email import Email


@dataclass
class User:
    id: Optional[int]
    name: str
    email: Email
    role: UserRole = UserRole.MEMBER
