"""
Unit tests for the APIClient class.
"""

from unittest.mock import Mock, patch

import pytest

from netbird import APIClient
from netbird.auth import TokenAuth
from netbird.cloud import CloudResources
from netbird.exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)
from netbird.resources.dns_zones import DNSZonesResource
from netbird.resources.geo_locations import GeoLocationsResource
from netbird.resources.identity_providers import IdentityProvidersResource
from netbird.resources.instance import InstanceResource
from netbird.resources.posture_checks import PostureChecksResource


class TestAPIClient:
    """Test cases for APIClient initialization and basic functionality."""

    def test_client_initialization(self):
        """Test basic client initialization."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        assert client.host == "api.netbird.io"
        assert client.base_url == "https://api.netbird.io/api"
        assert isinstance(client.auth, TokenAuth)

    def test_client_initialization_with_custom_settings(self):
        """Test client initialization with custom settings."""
        client = APIClient(
            host="http://custom.netbird.com:8080",
            api_token="test-token",
            timeout=60.0,
            base_path="/custom-api",
        )

        assert client.host == "http://custom.netbird.com:8080"
        assert client.base_url == "http://custom.netbird.com:8080/custom-api"
        assert client.timeout == 60.0

    def test_build_url(self):
        """Test URL building functionality."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        assert client._build_url("users") == "https://api.netbird.io/api/users"
        assert client._build_url("/users") == "https://api.netbird.io/api/users"
        assert client._build_url("users/123") == "https://api.netbird.io/api/users/123"

    def test_handle_response_success(self):
        """Test successful response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.json.return_value = {"id": "123", "name": "test"}
        mock_response.content = b'{"id": "123", "name": "test"}'

        result = client._handle_response(mock_response)
        assert result == {"id": "123", "name": "test"}

    def test_handle_response_validation_error(self):
        """Test 400 Bad Request response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid request"}
        mock_response.content = b'{"message": "Invalid request"}'

        with pytest.raises(NetBirdValidationError) as exc_info:
            client._handle_response(mock_response)

        assert "Invalid request" in str(exc_info.value)
        assert exc_info.value.status_code == 400

    def test_handle_response_authentication_error(self):
        """Test 401 Unauthorized response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Unauthorized"}
        mock_response.content = b'{"message": "Unauthorized"}'

        with pytest.raises(NetBirdAuthenticationError) as exc_info:
            client._handle_response(mock_response)

        assert "Unauthorized" in str(exc_info.value)
        assert exc_info.value.status_code == 401

    def test_handle_response_not_found_error(self):
        """Test 404 Not Found response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_response.content = b'{"message": "User not found"}'

        with pytest.raises(NetBirdNotFoundError) as exc_info:
            client._handle_response(mock_response)

        assert "User not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    def test_handle_response_rate_limit_error(self):
        """Test 429 Rate Limited response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limit exceeded"}
        mock_response.content = b'{"message": "Rate limit exceeded"}'
        mock_response.headers = {"Retry-After": "60"}

        with pytest.raises(NetBirdRateLimitError) as exc_info:
            client._handle_response(mock_response)

        assert "Rate limit exceeded" in str(exc_info.value)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60

    def test_handle_response_server_error(self):
        """Test 500 Server Error response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Internal server error"}
        mock_response.content = b'{"message": "Internal server error"}'

        with pytest.raises(NetBirdServerError) as exc_info:
            client._handle_response(mock_response)

        assert "Internal server error" in str(exc_info.value)
        assert exc_info.value.status_code == 500

    def test_handle_response_generic_error(self):
        """Test generic API error response handling."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 418  # I'm a teapot
        mock_response.json.return_value = {"message": "I'm a teapot"}
        mock_response.content = b'{"message": "I\'m a teapot"}'

        with pytest.raises(NetBirdAPIError) as exc_info:
            client._handle_response(mock_response)

        assert "I'm a teapot" in str(exc_info.value)
        assert exc_info.value.status_code == 418

    def test_handle_response_invalid_json(self):
        """Test response handling with invalid JSON."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.content = b"invalid json"

        with pytest.raises(NetBirdValidationError) as exc_info:
            client._handle_response(mock_response)

        assert "Invalid JSON response" in str(exc_info.value)

    @patch("netbird.client.httpx.Client.get")
    def test_get_request(self, mock_get):
        """Test GET request functionality."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.json.return_value = {"users": []}
        mock_response.content = b'{"users": []}'
        mock_get.return_value = mock_response

        result = client.get("users", params={"limit": 10})

        assert result == {"users": []}
        mock_get.assert_called_once_with(
            "https://api.netbird.io/api/users", params={"limit": 10}
        )

    @patch("netbird.client.httpx.Client.post")
    def test_post_request(self, mock_post):
        """Test POST request functionality."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.json.return_value = {"id": "123", "name": "Test User"}
        mock_response.content = b'{"id": "123", "name": "Test User"}'
        mock_post.return_value = mock_response

        result = client.post("users", data={"name": "Test User"})

        assert result == {"id": "123", "name": "Test User"}
        mock_post.assert_called_once_with(
            "https://api.netbird.io/api/users",
            json={"name": "Test User"},
            params=None,
        )

    def test_context_manager(self):
        """Test client as context manager."""
        with APIClient(host="api.netbird.io", api_token="test-token") as client:
            assert client.host == "api.netbird.io"

        # Client should be closed after context exit
        # This is tested by ensuring no exceptions are raised

    def test_resource_properties(self):
        """Test that resource properties are accessible."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        # Test that resource properties exist and are lazy-loaded
        assert hasattr(client, "accounts")
        assert hasattr(client, "users")
        assert hasattr(client, "tokens")
        assert hasattr(client, "peers")
        assert hasattr(client, "setup_keys")
        assert hasattr(client, "groups")
        assert hasattr(client, "networks")
        assert hasattr(client, "policies")
        assert hasattr(client, "routes")
        assert hasattr(client, "dns")
        assert hasattr(client, "events")

        # Test that accessing properties works
        accounts_resource = client.accounts
        users_resource = client.users

        # Resources should be properly instantiated
        assert accounts_resource is not None
        assert users_resource is not None

        # Accessing again should return the same instance (lazy loading)
        assert client.accounts is accounts_resource
        assert client.users is users_resource

    @patch("netbird.client.httpx.Client.put")
    def test_put_request(self, mock_put):
        """Test PUT request functionality."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.json.return_value = {"id": "123", "name": "Updated"}
        mock_response.content = b'{"id": "123", "name": "Updated"}'
        mock_put.return_value = mock_response

        result = client.put("users/123", data={"name": "Updated"})

        assert result == {"id": "123", "name": "Updated"}
        mock_put.assert_called_once_with(
            "https://api.netbird.io/api/users/123",
            json={"name": "Updated"},
            params=None,
        )

    @patch("netbird.client.httpx.Client.delete")
    def test_delete_request(self, mock_delete):
        """Test DELETE request functionality."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.content = b'{"status": "deleted"}'
        mock_response.json.return_value = {"status": "deleted"}
        mock_delete.return_value = mock_response

        result = client.delete("users/123")
        assert result == {"status": "deleted"}
        mock_delete.assert_called_once_with(
            "https://api.netbird.io/api/users/123", params=None
        )

    def test_handle_response_empty_content(self):
        """Test response handling with empty content."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = True
        mock_response.content = b""

        result = client._handle_response(mock_response)
        assert result == {}
        mock_response.json.assert_not_called()

    def test_handle_response_409_conflict(self):
        """Test 409 Conflict maps to ValidationError."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 409
        mock_response.json.return_value = {"message": "Conflict"}
        mock_response.content = b'{"message": "Conflict"}'

        with pytest.raises(NetBirdValidationError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 409

    def test_handle_response_422_unprocessable(self):
        """Test 422 Unprocessable Entity maps to ValidationError."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 422
        mock_response.json.return_value = {"message": "Unprocessable"}
        mock_response.content = b'{"message": "Unprocessable"}'

        with pytest.raises(NetBirdValidationError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 422

    def test_handle_response_rate_limit_no_retry_after(self):
        """Test 429 without Retry-After header."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limited"}
        mock_response.content = b'{"message": "Rate limited"}'
        mock_response.headers = {}

        with pytest.raises(NetBirdRateLimitError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.retry_after is None

    def test_handle_response_error_fallback_message(self):
        """Test error message fallback to 'error' key then status code."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 503
        mock_response.json.return_value = {"error": "Service unavailable"}
        mock_response.content = b'{"error": "Service unavailable"}'

        with pytest.raises(NetBirdServerError) as exc_info:
            client._handle_response(mock_response)
        assert "Service unavailable" in str(exc_info.value)

    def test_handle_response_no_message_fallback(self):
        """Test error falls back to HTTP status code when no message/error key."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 502
        mock_response.json.return_value = {}
        mock_response.content = b"{}"

        with pytest.raises(NetBirdServerError) as exc_info:
            client._handle_response(mock_response)
        assert "HTTP 502" in str(exc_info.value)

    def test_new_resource_properties(self):
        """Test Phase 2 resource properties are accessible and lazy-loaded."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        dns_zones = client.dns_zones
        assert isinstance(dns_zones, DNSZonesResource)
        assert client.dns_zones is dns_zones  # same instance

        posture_checks = client.posture_checks
        assert isinstance(posture_checks, PostureChecksResource)
        assert client.posture_checks is posture_checks

        geo_locations = client.geo_locations
        assert isinstance(geo_locations, GeoLocationsResource)
        assert client.geo_locations is geo_locations

        identity_providers = client.identity_providers
        assert isinstance(identity_providers, IdentityProvidersResource)
        assert client.identity_providers is identity_providers

        instance = client.instance
        assert isinstance(instance, InstanceResource)
        assert client.instance is instance

    def test_cloud_property(self):
        """Test cloud namespace property is accessible and lazy-loaded."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        cloud = client.cloud
        assert isinstance(cloud, CloudResources)
        assert client.cloud is cloud  # same instance

    def test_repr(self):
        """Test string representation of client."""
        client = APIClient(host="api.netbird.io", api_token="test-token")

        repr_str = repr(client)
        assert "APIClient" in repr_str
        assert "api.netbird.io" in repr_str
        assert "https://api.netbird.io/api" in repr_str
