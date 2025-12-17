class InfrastructureException(Exception):
    """Base exception for infrastructure layer issues."""


class DBConnectionError(InfrastructureException):
    pass
