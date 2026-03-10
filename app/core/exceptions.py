class AppException(Exception):
    """Base exception for application-level failures."""


class ConfigurationError(AppException):
    """Raised when required local configuration is missing or invalid."""


class ApiClientError(AppException):
    """Raised when the remote API request fails."""


class SyncError(AppException):
    """Raised when synchronization cannot be completed."""


class ValidationError(AppException):
    """Raised when user or API data is invalid."""
