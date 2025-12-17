class DomainException(Exception):
    """Base exception for domain layer rules."""


class InvalidEmail(DomainException):
    pass


class DuplicateUser(DomainException):
    pass
