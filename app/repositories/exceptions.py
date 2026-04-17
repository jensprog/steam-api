class RepositoryError(Exception):
    """Base exception for repository layer errors"""

    pass


class ConstraintViolationError(RepositoryError):
    """Raised when database constraints are violated"""

    pass
