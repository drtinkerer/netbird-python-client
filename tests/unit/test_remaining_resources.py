"""
Unit tests for remaining resource handlers to improve coverage.
"""

from unittest.mock import Mock

from netbird import APIClient
from netbird.models import (
    NetworkCreate,
    PolicyCreate,
    PolicyUpdate,
    RouteCreate,
    RouteUpdate,
)
from netbird.resources.dns import DNSResource
from netbird.resources.events import EventsResource
from netbird.resources.networks import NetworksResource
from netbird.resources.policies import PoliciesResource
from netbird.resources.routes import RoutesResource


class TestPoliciesResource:
    """Test PoliciesResource functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.policies_resource = PoliciesResource(self.mock_client)

    def test_list_policies(self):
        """Test listing policies."""
        mock_policies_data = [
            {
                "id": "policy-1",
                "name": "allow-ssh",
                "description": "Allow SSH access",
                "enabled": True,
                "rules": [],
            }
        ]
        self.mock_client.get.return_value = mock_policies_data

        policies = self.policies_resource.list()

        self.mock_client.get.assert_called_once_with("policies")
        assert len(policies) == 1
        assert isinstance(policies[0], dict)

    def test_create_policy(self):
        """Test creating a policy."""
        mock_policy_data = {
            "id": "policy-123",
            "name": "new-policy",
            "description": "New policy",
            "enabled": True,
            "rules": [],
        }
        self.mock_client.post.return_value = mock_policy_data

        policy_data = PolicyCreate(
            name="new-policy", description="New policy", rules=[]
        )
        policy = self.policies_resource.create(policy_data)

        self.mock_client.post.assert_called_once_with(
            "policies", data=policy_data.model_dump(exclude_unset=True)
        )
        assert policy["name"] == "new-policy"

    def test_get_policy(self):
        """Test getting a specific policy."""
        mock_policy_data = {
            "id": "policy-123",
            "name": "test-policy",
            "enabled": True,
            "rules": [],
        }
        self.mock_client.get.return_value = mock_policy_data

        policy = self.policies_resource.get("policy-123")

        self.mock_client.get.assert_called_once_with("policies/policy-123")
        assert policy["name"] == "test-policy"

    def test_update_policy(self):
        """Test updating a policy."""
        mock_policy_data = {
            "id": "policy-123",
            "name": "updated-policy",
            "enabled": False,
            "rules": [],
        }
        self.mock_client.put.return_value = mock_policy_data

        update_data = PolicyUpdate(name="updated-policy", enabled=False)
        policy = self.policies_resource.update("policy-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "policies/policy-123",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert policy["name"] == "updated-policy"
        assert not policy["enabled"]

    def test_delete_policy(self):
        """Test deleting a policy."""
        self.policies_resource.delete("policy-123")

        self.mock_client.delete.assert_called_once_with("policies/policy-123")


class TestRoutesResource:
    """Test RoutesResource functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.routes_resource = RoutesResource(self.mock_client)

    def test_list_routes(self):
        """Test listing routes."""
        mock_routes_data = [
            {
                "id": "route-1",
                "network_id": "192.168.1.0/24",
                "network_type": "ipv4",
                "enabled": True,
                "metric": 100,
                "masquerade": False,
                "keep_route": True,
            }
        ]
        self.mock_client.get.return_value = mock_routes_data

        routes = self.routes_resource.list()

        self.mock_client.get.assert_called_once_with("routes")
        assert len(routes) == 1
        assert isinstance(routes[0], dict)

    def test_create_route(self):
        """Test creating a route."""
        mock_route_data = {
            "id": "route-123",
            "description": "Test route",
            "network_id": "10.0.0.0/8",
            "network_type": "ipv4",
            "enabled": True,
            "metric": 200,
            "masquerade": False,
            "keep_route": False,
        }
        self.mock_client.post.return_value = mock_route_data

        route_data = RouteCreate(
            description="Test route",
            network_id="10.0.0.0/8",
            network_type="ipv4",
            metric=200,
        )
        route = self.routes_resource.create(route_data)

        self.mock_client.post.assert_called_once_with(
            "routes", data=route_data.model_dump(exclude_unset=True)
        )
        assert route["description"] == "Test route"

    def test_get_route(self):
        """Test getting a specific route."""
        mock_route_data = {
            "id": "route-123",
            "network_id": "192.168.1.0/24",
            "network_type": "ipv4",
            "enabled": True,
            "metric": 100,
            "masquerade": False,
            "keep_route": True,
        }
        self.mock_client.get.return_value = mock_route_data

        route = self.routes_resource.get("route-123")

        self.mock_client.get.assert_called_once_with("routes/route-123")
        assert route["network_id"] == "192.168.1.0/24"

    def test_update_route(self):
        """Test updating a route."""
        mock_route_data = {
            "id": "route-123",
            "description": "Updated route",
            "network_id": "192.168.1.0/24",
            "network_type": "ipv4",
            "enabled": False,
            "metric": 100,
            "masquerade": False,
            "keep_route": True,
        }
        self.mock_client.put.return_value = mock_route_data

        update_data = RouteUpdate(description="Updated route", enabled=False)
        route = self.routes_resource.update("route-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "routes/route-123", data=update_data.model_dump(exclude_unset=True)
        )
        assert route["description"] == "Updated route"
        assert not route["enabled"]

    def test_delete_route(self):
        """Test deleting a route."""
        self.routes_resource.delete("route-123")

        self.mock_client.delete.assert_called_once_with("routes/route-123")


class TestDNSResource:
    """Test DNSResource functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.dns_resource = DNSResource(self.mock_client)

    def test_list_nameserver_groups(self):
        """Test listing nameserver groups."""
        mock_ns_groups_data = [
            {
                "id": "ns-1",
                "name": "corporate-dns",
                "nameservers": ["8.8.8.8", "8.8.4.4"],
                "enabled": True,
                "search_domains_enabled": False,
            }
        ]
        self.mock_client.get.return_value = mock_ns_groups_data

        ns_groups = self.dns_resource.list_nameserver_groups()

        self.mock_client.get.assert_called_once_with("dns/nameservers")
        assert len(ns_groups) == 1
        assert isinstance(ns_groups[0], dict)

    def test_create_nameserver_group(self):
        """Test creating a nameserver group."""
        mock_ns_group_data = {
            "id": "ns-123",
            "name": "new-dns",
            "nameservers": ["1.1.1.1", "1.0.0.1"],
            "enabled": True,
            "search_domains_enabled": False,
        }
        self.mock_client.post.return_value = mock_ns_group_data

        ns_data = {
            "name": "new-dns",
            "nameservers": ["1.1.1.1", "1.0.0.1"],
            "enabled": True,
        }
        ns_group = self.dns_resource.create_nameserver_group(ns_data)

        self.mock_client.post.assert_called_once_with("dns/nameservers", data=ns_data)
        assert ns_group["name"] == "new-dns"

    def test_get_nameserver_group(self):
        """Test getting a specific nameserver group."""
        mock_ns_group_data = {
            "id": "ns-123",
            "name": "test-dns",
            "nameservers": ["8.8.8.8"],
            "enabled": True,
            "search_domains_enabled": False,
        }
        self.mock_client.get.return_value = mock_ns_group_data

        ns_group = self.dns_resource.get_nameserver_group("ns-123")

        self.mock_client.get.assert_called_once_with("dns/nameservers/ns-123")
        assert ns_group["name"] == "test-dns"

    def test_update_nameserver_group(self):
        """Test updating a nameserver group."""
        mock_ns_group_data = {
            "id": "ns-123",
            "name": "updated-dns",
            "nameservers": ["8.8.8.8"],
            "enabled": False,
            "search_domains_enabled": False,
        }
        self.mock_client.put.return_value = mock_ns_group_data

        update_data = {"name": "updated-dns", "enabled": False}
        ns_group = self.dns_resource.update_nameserver_group("ns-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "dns/nameservers/ns-123", data=update_data
        )
        assert ns_group["name"] == "updated-dns"
        assert not ns_group["enabled"]

    def test_delete_nameserver_group(self):
        """Test deleting a nameserver group."""
        self.dns_resource.delete_nameserver_group("ns-123")

        self.mock_client.delete.assert_called_once_with("dns/nameservers/ns-123")

    def test_get_settings(self):
        """Test getting DNS settings."""
        mock_settings_data = {"disabled_management_groups": ["group-1", "group-2"]}
        self.mock_client.get.return_value = mock_settings_data

        settings = self.dns_resource.get_settings()

        self.mock_client.get.assert_called_once_with("dns/settings")
        assert isinstance(settings, dict)
        assert len(settings["disabled_management_groups"]) == 2

    def test_update_settings(self):
        """Test updating DNS settings."""
        mock_settings_data = {"disabled_management_groups": ["group-3"]}
        self.mock_client.put.return_value = mock_settings_data

        update_data = {"disabled_management_groups": ["group-3"]}
        settings = self.dns_resource.update_settings(update_data)

        self.mock_client.put.assert_called_once_with("dns/settings", data=update_data)
        assert len(settings["disabled_management_groups"]) == 1


class TestEventsResource:
    """Test EventsResource functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.events_resource = EventsResource(self.mock_client)

    def test_get_audit_events(self):
        """Test getting audit events."""
        mock_events_data = [
            {
                "timestamp": "2023-01-01T00:00:00Z",
                "activity": "user.created",
                "initiator_id": "user-123",
            }
        ]
        self.mock_client.get.return_value = mock_events_data

        events = self.events_resource.get_audit_events()

        self.mock_client.get.assert_called_once_with("events/audit")
        assert len(events) == 1
        assert isinstance(events[0], dict)

    def test_get_network_traffic_events_no_params(self):
        """Test getting network traffic events without parameters."""
        mock_events_data = [
            {
                "timestamp": "2023-01-01T00:00:00Z",
                "source_ip": "10.0.0.1",
                "destination_ip": "10.0.0.2",
                "source_port": 12345,
                "destination_port": 80,
                "protocol": "tcp",
                "bytes_sent": 1024,
                "bytes_received": 2048,
                "peer_id": "peer-123",
                "reporter_id": "peer-456",
                "direction": "sent",
                "connection_type": "p2p",
                "allowed": True,
            }
        ]
        self.mock_client.get.return_value = mock_events_data

        events = self.events_resource.get_network_traffic_events()

        self.mock_client.get.assert_called_once_with(
            "events/network-traffic", params=None
        )
        assert len(events) == 1
        assert isinstance(events[0], dict)

    def test_get_network_traffic_events_with_params(self):
        """Test getting network traffic events with parameters."""
        mock_events_data = []
        self.mock_client.get.return_value = mock_events_data

        self.events_resource.get_network_traffic_events(
            page=1,
            page_size=50,
            user_id="user-123",
            protocol="tcp",
            direction="sent",
        )

        expected_params = {
            "page": 1,
            "page_size": 50,
            "user_id": "user-123",
            "protocol": "tcp",
            "direction": "sent",
        }
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic", params=expected_params
        )


class TestNetworksResource:
    """Test NetworksResource functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.networks_resource = NetworksResource(self.mock_client)

    def test_list_networks(self):
        """Test listing networks."""
        mock_networks_data = [
            {
                "id": "network-1",
                "name": "production",
                "description": "Production network",
            }
        ]
        self.mock_client.get.return_value = mock_networks_data

        networks = self.networks_resource.list()

        self.mock_client.get.assert_called_once_with("networks")
        assert len(networks) == 1
        assert isinstance(networks[0], dict)

    def test_create_network(self):
        """Test creating a network."""
        mock_network_data = {
            "id": "network-123",
            "name": "new-network",
            "description": "New network",
        }
        self.mock_client.post.return_value = mock_network_data

        network_data = NetworkCreate(name="new-network", description="New network")
        network = self.networks_resource.create(network_data)

        self.mock_client.post.assert_called_once_with(
            "networks", data=network_data.model_dump(exclude_unset=True)
        )
        assert network["name"] == "new-network"


class TestAccountsResourceUpdate:
    """Test AccountsResource update functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.accounts import AccountsResource

        self.accounts_resource = AccountsResource(self.mock_client)

    def test_update_account(self):
        """Test updating account settings."""
        from netbird.models.account import AccountSettings

        mock_account_data = {
            "id": "account-123",
            "domain": "example.com",
            "settings": {
                "peer_login_expiration_enabled": True,
                "peer_login_expiration": 3600,
            },
        }
        self.mock_client.put.return_value = mock_account_data

        settings = AccountSettings(
            peer_login_expiration_enabled=True, peer_login_expiration=3600
        )
        account = self.accounts_resource.update("account-123", settings)

        self.mock_client.put.assert_called_once_with(
            "accounts/account-123",
            data={"settings": settings.model_dump(exclude_unset=True)},
        )
        assert account["domain"] == "example.com"

    def test_delete_account(self):
        """Test deleting an account."""
        self.accounts_resource.delete("account-123")

        self.mock_client.delete.assert_called_once_with("accounts/account-123")
