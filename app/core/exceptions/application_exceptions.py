class ApplicationException(Exception):
    """Base exception for application layer errors."""


class UserNotFound(ApplicationException):
    pass
