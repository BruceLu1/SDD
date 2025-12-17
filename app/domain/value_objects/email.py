import re
from dataclasses import dataclass

from app.core.exceptions.domain_exceptions import InvalidEmail


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_REGEX.match(self.value):
            raise InvalidEmail(f"Invalid email: {self.value}")

    def __str__(self) -> str:  # pragma: no cover - simple passthrough
        return self.value
