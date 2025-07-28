"""
Basic integration tests for NetBird API client.

These tests require a valid NetBird API token set in the NETBIRD_TEST_TOKEN
environment variable.
"""

import pytest

from netbird.exceptions import NetBirdAPIError


@pytest.mark.integration
class TestBasicIntegration:
    """Basic integration tests that don't modify data."""

    def test_get_current_user(self, integration_client):
        """Test getting current user information."""
        user = integration_client.users.get_current()

        assert user["id"] is not None
        assert user["email"] is not None
        assert user["role"] in ["admin", "user", "owner"]
        assert user["status"] in ["active", "disabled", "invited"]

    def test_list_users(self, integration_client):
        """Test listing users."""
        users = integration_client.users.list()

        assert isinstance(users, list)
        assert len(users) > 0  # Should have at least the current user

        # Check first user structure
        first_user = users[0]
        assert "id" in first_user
        assert "email" in first_user
        assert "role" in first_user
        assert "status" in first_user

    def test_list_peers(self, integration_client):
        """Test listing peers."""
        peers = integration_client.peers.list()

        assert isinstance(peers, list)
        # Note: Could be empty if no peers are registered

        if peers:
            first_peer = peers[0]
            assert "id" in first_peer
            assert "name" in first_peer
            assert "ip" in first_peer
            assert "connected" in first_peer

    def test_list_groups(self, integration_client):
        """Test listing groups."""
        groups = integration_client.groups.list()

        assert isinstance(groups, list)
        # Note: Could be empty if no groups exist

        if groups:
            first_group = groups[0]
            assert "id" in first_group
            assert "name" in first_group
            assert "peers_count" in first_group

    def test_list_accounts(self, integration_client):
        """Test listing accounts."""
        accounts = integration_client.accounts.list()

        assert isinstance(accounts, list)
        assert len(accounts) == 1  # Should always have exactly one account

        account = accounts[0]
        assert "id" in account
        assert "domain" in account

    def test_list_setup_keys(self, integration_client):
        """Test listing setup keys."""
        setup_keys = integration_client.setup_keys.list()

        assert isinstance(setup_keys, list)
        # Note: Could be empty if no setup keys exist

        if setup_keys:
            first_key = setup_keys[0]
            assert "id" in first_key
            assert "name" in first_key
            assert "type" in first_key
            assert "valid" in first_key

    def test_list_policies(self, integration_client):
        """Test listing policies."""
        policies = integration_client.policies.list()

        assert isinstance(policies, list)
        # Note: Could be empty if no policies exist

        if policies:
            first_policy = policies[0]
            assert "id" in first_policy
            assert "name" in first_policy
            assert "enabled" in first_policy
            assert "rules" in first_policy

    # def test_list_routes(self, integration_client):
    #     """Test listing routes."""
    #     routes = integration_client.routes.list()
    #
    #     assert isinstance(routes, list)
    #     # Note: Could be empty if no routes exist
    #
    #     if routes:
    #         first_route = routes[0]
    #         assert hasattr(first_route, 'id')
    #         assert hasattr(first_route, 'network_id')
    #         assert hasattr(first_route, 'enabled')

    def test_list_networks(self, integration_client):
        """Test listing networks."""
        networks = integration_client.networks.list()

        assert isinstance(networks, list)
        # Note: Could be empty if no networks exist

        if networks:
            first_network = networks[0]
            assert "id" in first_network
            assert "name" in first_network

    def test_get_dns_settings(self, integration_client):
        """Test getting DNS settings."""
        try:
            dns_settings = integration_client.dns.get_settings()
            assert "disabled_management_groups" in dns_settings
        except NetBirdAPIError as e:
            # DNS settings might not be available in all NetBird instances
            if e.status_code == 404:
                pytest.skip("DNS settings not available")
            else:
                raise

    def test_list_dns_nameserver_groups(self, integration_client):
        """Test listing DNS nameserver groups."""
        try:
            nameserver_groups = integration_client.dns.list_nameserver_groups()
            assert isinstance(nameserver_groups, list)

            if nameserver_groups:
                first_group = nameserver_groups[0]
                assert "id" in first_group
                assert "name" in first_group
                assert "nameservers" in first_group
        except NetBirdAPIError as e:
            # DNS features might not be available in all NetBird instances
            if e.status_code == 404:
                pytest.skip("DNS nameserver groups not available")
            else:
                raise

    def test_get_audit_events(self, integration_client):
        """Test getting audit events."""
        try:
            audit_events = integration_client.events.get_audit_events()
            assert isinstance(audit_events, list)

            if audit_events:
                first_event = audit_events[0]
                assert "timestamp" in first_event
                assert "activity" in first_event
                assert "initiator_id" in first_event
        except NetBirdAPIError as e:
            # Events might not be available in all NetBird instances
            if e.status_code == 404:
                pytest.skip("Audit events not available")
            else:
                raise

    def test_invalid_resource_id_raises_not_found(self, integration_client):
        """Test that requesting invalid resource IDs raises API error."""
        from netbird.exceptions import NetBirdAPIError

        # Different endpoints may return different error codes
        # Let's test with a known endpoint that gives 404
        with pytest.raises(NetBirdAPIError) as exc_info:
            integration_client.groups.get("invalid-group-id-12345")

        # Should be 404 or 405 - both are valid API errors
        assert exc_info.value.status_code in [404, 405]

    def test_client_context_manager(self, integration_client):
        """Test using client as context manager."""
        # The integration_client fixture creates a client, so we'll test
        # context manager behavior with a new client
        import os

        from netbird import APIClient

        api_token = os.getenv("NETBIRD_TEST_TOKEN") or os.getenv("NETBIRD_API_TOKEN")
        host = os.getenv("NETBIRD_TEST_HOST") or os.getenv(
            "NETBIRD_HOST", "api.netbird.io"
        )

        with APIClient(host=host, api_token=api_token) as client:
            users = client.users.list()
            assert isinstance(users, list)

        # Client should be properly closed after context exit
        # No specific assertion needed - test passes if no exception is raised
