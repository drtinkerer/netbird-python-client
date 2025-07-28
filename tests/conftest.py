"""
Pytest configuration and shared fixtures.
"""

import os
import pytest
from unittest.mock import Mock

from netbird import APIClient
from tests.fixtures import load_sample_data, load_mock_config, load_api_response


@pytest.fixture
def mock_client():
    """Create a mock APIClient for testing."""
    client = Mock(spec=APIClient)
    client.host = "api.netbird.io"
    client.base_url = "https://api.netbird.io/api"
    return client


@pytest.fixture
def test_client():
    """Create a real APIClient instance for testing."""
    return APIClient(
        host="api.netbird.io",
        api_token="test-token-123"
    )


@pytest.fixture
def integration_client():
    """Create a client for integration tests (requires environment variables)."""
    # Try both test and regular env var names
    api_token = os.getenv("NETBIRD_TEST_TOKEN") or os.getenv("NETBIRD_API_TOKEN")
    if not api_token:
        pytest.skip("NETBIRD_TEST_TOKEN or NETBIRD_API_TOKEN environment variable not set")
    
    host = os.getenv("NETBIRD_TEST_HOST") or os.getenv("NETBIRD_HOST", "api.netbird.io")
    
    return APIClient(host=host, api_token=api_token)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return load_sample_data("user")


@pytest.fixture
def sample_peer_data():
    """Sample peer data for testing."""
    return load_sample_data("peer")


@pytest.fixture
def sample_group_data():
    """Sample group data for testing."""
    return load_sample_data("group")


@pytest.fixture
def sample_setup_key_data():
    """Sample setup key data for testing."""
    return load_api_response("setup_keys")[0]


@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing."""
    return load_api_response("policies")[0]


# New industry-standard fixtures using file-based data
@pytest.fixture
def mock_users_response():
    """Mock API response for users endpoint."""
    return load_api_response("users")


@pytest.fixture
def mock_peers_response():
    """Mock API response for peers endpoint."""
    return load_api_response("peers")


@pytest.fixture
def mock_groups_response():
    """Mock API response for groups endpoint."""
    return load_api_response("groups")


@pytest.fixture
def client_configs():
    """Mock client configurations."""
    return load_mock_config("client")


@pytest.fixture
def auth_configs():
    """Mock authentication configurations."""
    return load_mock_config("auth")


@pytest.fixture
def sample_route_data():
    """Sample route data for testing."""
    return {
        "id": "route-123",
        "description": "Test route",
        "network_id": "192.168.1.0/24",
        "network_type": "ipv4", 
        "enabled": True,
        "metric": 100,
        "masquerade": False,
        "keep_route": False
    }


@pytest.fixture
def sample_network_data():
    """Sample network data for testing."""
    return {
        "id": "network-123",
        "name": "test-network",
        "description": "Test network"
    }


@pytest.fixture
def sample_dns_nameserver_data():
    """Sample DNS nameserver group data for testing."""
    return {
        "id": "ns-group-123",
        "name": "test-nameservers",
        "description": "Test nameserver group",
        "nameservers": ["8.8.8.8", "8.8.4.4"],
        "enabled": True,
        "search_domains_enabled": False
    }


@pytest.fixture
def sample_token_data():
    """Sample token data for testing."""
    return {
        "id": "token-123",
        "name": "test-token",
        "creation_date": "2023-01-01T00:00:00Z",
        "expiration_date": "2023-12-31T23:59:59Z",
        "created_by": "user-123",
        "last_used": None
    }


# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )