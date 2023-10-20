"""Errors for the backend."""


class NotFoundError(Exception):
    """Error raised when an object is not found."""


class CourseNotFoundError(NotFoundError):
    """Error raised when a course is not found."""


class CohortNotFoundError(NotFoundError):
    """Error raised when a cohort is not found."""


class EvaluationNotFoundError(NotFoundError):
    """Error raised when an evaluation is not found."""


class DatabaseConnectionError(Exception):
    """Error raised when a database connection cannot be established."""
