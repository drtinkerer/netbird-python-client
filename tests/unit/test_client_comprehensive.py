"""
Comprehensive client.py coverage tests to improve coverage from 68% to 80%+.
Focuses on testing the diagram generation methods and other uncovered paths.
"""

import pytest

from netbird.client import APIClient


class TestClientHelperMethods:
    """Test client helper methods for coverage."""

    @pytest.fixture
    def client(self):
        return APIClient(host="test.example.com", api_token="test-token")

    def test_get_source_group_colors_comprehensive(self, client):
        """Test _get_source_group_colors with various inputs."""
        # Test with no groups
        colors = client._get_source_group_colors([])
        assert colors == {}

        # Test with single group
        colors = client._get_source_group_colors(["group1"])
        assert len(colors) == 1
        assert "group1" in colors
        assert colors["group1"].startswith("#")

        # Test with multiple groups
        groups = ["alpha", "beta", "gamma", "delta", "epsilon"]
        colors = client._get_source_group_colors(groups)
        assert len(colors) == 5
        assert all(color.startswith("#") for color in colors.values())

        # Test color consistency (same input should give same colors)
        colors2 = client._get_source_group_colors(groups)
        assert colors == colors2

        # Test with many groups (more than predefined colors)
        many_groups = [f"group{i}" for i in range(20)]
        colors = client._get_source_group_colors(many_groups)
        assert len(colors) == 20
        assert all(color.startswith("#") for color in colors.values())

    def test_format_policy_label_edge_cases(self, client):
        """Test _format_policy_label with edge cases."""
        # Test with empty list
        label = client._format_policy_label([], "Test")
        assert "Test" in label

        # Test with single policy
        label = client._format_policy_label(["policy1"], "Single")
        assert "policy1" in label

        # Test with exactly 2 policies
        label = client._format_policy_label(["p1", "p2"], "Two")
        assert "p1" in label and "p2" in label

        # Test with exactly 3 policies (should show count)
        label = client._format_policy_label(["p1", "p2", "p3"], "Three")
        assert "3 policies" in label

        # Test with many policies
        policies = [f"policy{i}" for i in range(10)]
        label = client._format_policy_label(policies, "Many")
        assert "10 policies" in label

    def test_sanitize_id_comprehensive(self, client):
        """Test _sanitize_id with comprehensive character sets."""
        # Test normal ID
        assert client._sanitize_id("normal_id") == "normal_id"

        # Test with hyphens
        assert client._sanitize_id("with-hyphens") == "with_hyphens"

        # Test with dots
        assert client._sanitize_id("with.dots.here") == "with_dots_here"

        # Test with spaces
        assert client._sanitize_id("with spaces") == "with_spaces"

        # Test with mixed special characters
        assert client._sanitize_id("test!@#$%^&*()") == "test__________"

        # Test with numbers (should be preserved)
        assert client._sanitize_id("test123") == "test123"

        # Test with underscores (should be preserved)
        assert client._sanitize_id("test_123_abc") == "test_123_abc"

        # Test empty string
        assert client._sanitize_id("") == ""

        # Test only special characters
        assert client._sanitize_id("!@#$") == "____"


class TestClientTypeCheckingImports:
    """Test TYPE_CHECKING imports indirectly."""

    def test_client_resource_attribute_access(self):
        """Test that all resource attributes are accessible."""
        client = APIClient(host="test.com", api_token="token")

        # Test that all resource attributes exist and are of correct type
        from netbird.resources.accounts import AccountsResource
        from netbird.resources.dns import DNSResource
        from netbird.resources.events import EventsResource
        from netbird.resources.groups import GroupsResource
        from netbird.resources.networks import NetworksResource
        from netbird.resources.peers import PeersResource
        from netbird.resources.policies import PoliciesResource
        from netbird.resources.routes import RoutesResource
        from netbird.resources.setup_keys import SetupKeysResource
        from netbird.resources.tokens import TokensResource
        from netbird.resources.users import UsersResource

        assert isinstance(client.accounts, AccountsResource)
        assert isinstance(client.users, UsersResource)
        assert isinstance(client.tokens, TokensResource)
        assert isinstance(client.peers, PeersResource)
        assert isinstance(client.setup_keys, SetupKeysResource)
        assert isinstance(client.groups, GroupsResource)
        assert isinstance(client.networks, NetworksResource)
        assert isinstance(client.policies, PoliciesResource)
        assert isinstance(client.routes, RoutesResource)
        assert isinstance(client.dns, DNSResource)
        assert isinstance(client.events, EventsResource)

    def test_client_initialization_with_all_parameters(self):
        """Test client initialization with various parameter combinations."""
        # Test minimal initialization
        client1 = APIClient(host="test1.com", api_token="token1")
        assert client1.host == "test1.com"
        assert client1.timeout == 30.0  # default

        # Test with custom timeout
        client2 = APIClient(host="test2.com", api_token="token2", timeout=60.0)
        assert client2.timeout == 60.0

        # Test with HTTP protocol specified
        client3 = APIClient(host="http://test3.com", api_token="token3")
        assert "http://" in client3.base_url

        # Test with custom base path
        client4 = APIClient(
            host="test4.com", api_token="token4", base_path="/custom/api"
        )
        assert "/custom/api" in client4.base_url


class TestClientEdgeCases:
    """Test client edge cases and error scenarios."""

    @pytest.fixture
    def client(self):
        return APIClient(host="test.example.com", api_token="test-token")
