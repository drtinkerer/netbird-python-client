"""
Unit tests for exception classes.
"""

import pytest

from netbird.exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)


class TestNetBirdAPIError:
    """Test cases for NetBirdAPIError base class."""

    def test_basic_initialization(self):
        """Test basic error initialization."""
        error = NetBirdAPIError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.status_code is None
        assert error.response_data == {}

    def test_initialization_with_status_code(self):
        """Test error initialization with status code."""
        error = NetBirdAPIError("Test error", status_code=400)

        assert error.message == "Test error"
        assert error.status_code == 400

    def test_initialization_with_response_data(self):
        """Test error initialization with response data."""
        response_data = {"error": "validation_failed", "details": "Invalid email"}
        error = NetBirdAPIError("Test error", response_data=response_data)

        assert error.response_data == response_data

    def test_initialization_with_all_parameters(self):
        """Test error initialization with all parameters."""
        response_data = {"error": "test_error"}
        error = NetBirdAPIError(
            "Test error message", status_code=422, response_data=response_data
        )

        assert error.message == "Test error message"
        assert error.status_code == 422
        assert error.response_data == response_data

    def test_none_response_data_defaults_to_empty_dict(self):
        """Test that None response_data defaults to empty dict."""
        error = NetBirdAPIError("Test error", response_data=None)
        assert error.response_data == {}


class TestNetBirdAuthenticationError:
    """Test cases for NetBirdAuthenticationError."""

    def test_inheritance(self):
        """Test that NetBirdAuthenticationError inherits from NetBirdAPIError."""
        error = NetBirdAuthenticationError("Auth failed")

        assert isinstance(error, NetBirdAPIError)
        assert str(error) == "Auth failed"

    def test_initialization_with_parameters(self):
        """Test authentication error with parameters."""
        error = NetBirdAuthenticationError(
            "Invalid token", status_code=401, response_data={"error": "invalid_token"}
        )

        assert error.message == "Invalid token"
        assert error.status_code == 401
        assert error.response_data == {"error": "invalid_token"}


class TestNetBirdValidationError:
    """Test cases for NetBirdValidationError."""

    def test_inheritance(self):
        """Test that NetBirdValidationError inherits from NetBirdAPIError."""
        error = NetBirdValidationError("Validation failed")

        assert isinstance(error, NetBirdAPIError)
        assert str(error) == "Validation failed"


class TestNetBirdNotFoundError:
    """Test cases for NetBirdNotFoundError."""

    def test_inheritance(self):
        """Test that NetBirdNotFoundError inherits from NetBirdAPIError."""
        error = NetBirdNotFoundError("Resource not found")

        assert isinstance(error, NetBirdAPIError)
        assert str(error) == "Resource not found"


class TestNetBirdServerError:
    """Test cases for NetBirdServerError."""

    def test_inheritance(self):
        """Test that NetBirdServerError inherits from NetBirdAPIError."""
        error = NetBirdServerError("Internal server error")

        assert isinstance(error, NetBirdAPIError)
        assert str(error) == "Internal server error"


class TestNetBirdRateLimitError:
    """Test cases for NetBirdRateLimitError."""

    def test_inheritance(self):
        """Test that NetBirdRateLimitError inherits from NetBirdAPIError."""
        error = NetBirdRateLimitError("Rate limit exceeded")

        assert isinstance(error, NetBirdAPIError)
        assert str(error) == "Rate limit exceeded"

    def test_initialization_without_retry_after(self):
        """Test rate limit error without retry_after."""
        error = NetBirdRateLimitError("Rate limit exceeded")

        assert error.message == "Rate limit exceeded"
        assert error.retry_after is None

    def test_initialization_with_retry_after(self):
        """Test rate limit error with retry_after."""
        error = NetBirdRateLimitError(
            "Rate limit exceeded",
            status_code=429,
            response_data={"error": "rate_limit"},
            retry_after=60,
        )

        assert error.message == "Rate limit exceeded"
        assert error.status_code == 429
        assert error.response_data == {"error": "rate_limit"}
        assert error.retry_after == 60

    def test_retry_after_as_string(self):
        """Test retry_after handling when passed as string."""
        # Note: This tests the expected behavior - the code should handle
        # retry_after as received from HTTP headers (typically strings)
        error = NetBirdRateLimitError(
            "Rate limit exceeded",
            retry_after="120",  # String value as might come from headers
        )

        # The current implementation expects int, but this documents the interface
        assert error.retry_after == "120"


class TestExceptionHierarchy:
    """Test the exception hierarchy and relationships."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all custom exceptions inherit from NetBirdAPIError."""
        exceptions = [
            NetBirdAuthenticationError("test"),
            NetBirdValidationError("test"),
            NetBirdNotFoundError("test"),
            NetBirdRateLimitError("test"),
            NetBirdServerError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, NetBirdAPIError)
            assert isinstance(exc, Exception)

    def test_base_exception_inherits_from_exception(self):
        """Test that base NetBirdAPIError inherits from Exception."""
        error = NetBirdAPIError("test")
        assert isinstance(error, Exception)

    def test_exception_catching(self):
        """Test that specific exceptions can be caught by base class."""
        with pytest.raises(NetBirdAPIError):
            raise NetBirdAuthenticationError("Auth failed")

        with pytest.raises(NetBirdAPIError):
            raise NetBirdValidationError("Validation failed")

        with pytest.raises(NetBirdAPIError):
            raise NetBirdNotFoundError("Not found")

        with pytest.raises(NetBirdAPIError):
            raise NetBirdRateLimitError("Rate limited")

        with pytest.raises(NetBirdAPIError):
            raise NetBirdServerError("Server error")
