"""
NetBird API Client Exceptions

Custom exception classes for handling various API error conditions.
"""

from typing import Any, Dict, Optional


class NetBirdAPIError(Exception):
    """Base exception for all NetBird API errors.
    
    Attributes:
        message: Human-readable error message
        status_code: HTTP status code if available
        response_data: Raw response data from the API
    """
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class NetBirdAuthenticationError(NetBirdAPIError):
    """Raised when authentication fails (401 Unauthorized).
    
    This typically indicates:
    - Invalid or expired API token
    - Missing Authorization header
    - Token lacks required permissions
    """
    pass


class NetBirdValidationError(NetBirdAPIError):
    """Raised when request validation fails (400 Bad Request).
    
    This typically indicates:
    - Missing required parameters
    - Invalid parameter values
    - Malformed request body
    """
    pass


class NetBirdNotFoundError(NetBirdAPIError):
    """Raised when a requested resource is not found (404 Not Found).
    
    This typically indicates:
    - Resource ID does not exist
    - Resource has been deleted
    - Insufficient permissions to access resource
    """
    pass


class NetBirdRateLimitError(NetBirdAPIError):
    """Raised when API rate limit is exceeded (429 Too Many Requests).
    
    Attributes:
        retry_after: Number of seconds to wait before retrying
    """
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(message, status_code, response_data)
        self.retry_after = retry_after


class NetBirdServerError(NetBirdAPIError):
    """Raised when the server encounters an internal error (5xx status codes).
    
    This typically indicates:
    - Temporary server issues
    - Database connectivity problems
    - Internal service failures
    """
    pass