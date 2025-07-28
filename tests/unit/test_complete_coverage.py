"""
Tests to achieve 100% code coverage.
"""

from unittest.mock import Mock, patch

from netbird import APIClient

# Note: These imports are kept for input validation, but responses are now dictionaries
from netbird.resources.base import BaseResource


class TestClientCompleteCode:
    """Test remaining client code paths."""

    def test_client_delete_method(self):
        """Test the delete method in client."""
        client = APIClient(host="api.netbird.io", api_token="test")

        with patch.object(client.client, "delete") as mock_delete:
            mock_response = Mock()
            mock_response.is_success = True
            mock_response.json.return_value = {}
            mock_response.content = b"{}"
            mock_delete.return_value = mock_response

            client.delete("test-path", params={"key": "value"})

            mock_delete.assert_called_once_with(
                "https://api.netbird.io/api/test-path", params={"key": "value"}
            )

    def test_client_put_method(self):
        """Test the put method in client."""
        client = APIClient(host="api.netbird.io", api_token="test")

        with patch.object(client.client, "put") as mock_put:
            mock_response = Mock()
            mock_response.is_success = True
            mock_response.json.return_value = {"result": "updated"}
            mock_response.content = b'{"result": "updated"}'
            mock_put.return_value = mock_response

            result = client.put(
                "test-path", data={"name": "test"}, params={"filter": "active"}
            )

            mock_put.assert_called_once_with(
                "https://api.netbird.io/api/test-path",
                json={"name": "test"},
                params={"filter": "active"},
            )
            assert result == {"result": "updated"}


class TestBaseResourceCompleteCode:
    """Test remaining base resource code paths."""

    def test_base_resource_init(self):
        """Test base resource initialization."""
        mock_client = Mock(spec=APIClient)
        resource = BaseResource(mock_client)
        assert resource.client == mock_client

    def test_parse_response_with_list_data(self):
        """Test parsing response when data is a list."""
        mock_client = Mock()
        resource = BaseResource(mock_client)

        # Mock model class for testing

        data = [{"id": "1"}, {"id": "2"}]
        result = resource._parse_response(data)

        # _parse_response is for single objects, should return empty dict for lists
        assert result == {}

    def test_parse_response_with_other_data(self):
        """Test parsing response with non-dict, non-list data."""
        mock_client = Mock()
        resource = BaseResource(mock_client)

        # Test with simple string data
        data = "simple string"
        result = resource._parse_response(data)

        # Should return empty dict for non-convertible data
        assert result == {}


class TestEventsResourceCompleteCode:
    """Test remaining events resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.events import EventsResource

        self.events_resource = EventsResource(self.mock_client)

    def test_get_network_traffic_events_all_params(self):
        """Test network traffic events with all possible parameters."""
        mock_events_data = []
        self.mock_client.get.return_value = mock_events_data

        # Test with all parameters that were missing coverage
        self.events_resource.get_network_traffic_events(
            page=1,
            page_size=50,
            user_id="user-123",
            reporter_id="reporter-456",
            protocol="tcp",
            event_type="connection",
            connection_type="relay",
            direction="received",
            search="test-search",
            start_date="2023-01-01",
            end_date="2023-12-31",
        )

        expected_params = {
            "page": 1,
            "page_size": 50,
            "user_id": "user-123",
            "reporter_id": "reporter-456",
            "protocol": "tcp",
            "type": "connection",
            "connection_type": "relay",
            "direction": "received",
            "search": "test-search",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic", params=expected_params
        )


class TestGroupsResourceCompleteCode:
    """Test remaining groups resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.groups import GroupsResource

        self.groups_resource = GroupsResource(self.mock_client)

    def test_get_group(self):
        """Test getting a specific group."""

        mock_group_data = {
            "id": "group-123",
            "name": "test-group",
            "peers_count": 5,
            "peers": [{"id": "peer-1"}, {"id": "peer-2"}],
        }
        self.mock_client.get.return_value = mock_group_data

        group = self.groups_resource.get("group-123")

        self.mock_client.get.assert_called_once_with("groups/group-123")
        assert isinstance(group, dict)
        assert group["id"] == "group-123"

    def test_update_group(self):
        """Test updating a group."""
        from netbird.models import GroupUpdate

        mock_group_data = {
            "id": "group-123",
            "name": "updated-group",
            "peers_count": 3,
            "peers": [{"id": "peer-1"}, {"id": "peer-2"}, {"id": "peer-3"}],
        }
        self.mock_client.put.return_value = mock_group_data

        update_data = GroupUpdate(
            name="updated-group", peers=["peer-1", "peer-2", "peer-3"]
        )
        group = self.groups_resource.update("group-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "groups/group-123", data=update_data.model_dump(exclude_unset=True)
        )
        assert group["name"] == "updated-group"

    def test_delete_group(self):
        """Test deleting a group."""
        self.groups_resource.delete("group-123")

        self.mock_client.delete.assert_called_once_with("groups/group-123")


class TestNetworksResourceCompleteCode:
    """Test remaining networks resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.networks import NetworksResource

        self.networks_resource = NetworksResource(self.mock_client)

    def test_get_network(self):
        """Test getting a specific network."""

        mock_network_data = {
            "id": "network-123",
            "name": "test-network",
            "description": "Test network",
        }
        self.mock_client.get.return_value = mock_network_data

        network = self.networks_resource.get("network-123")

        self.mock_client.get.assert_called_once_with("networks/network-123")
        assert isinstance(network, dict)
        assert network["id"] == "network-123"

    def test_update_network(self):
        """Test updating a network."""
        from netbird.models import NetworkUpdate

        mock_network_data = {
            "id": "network-123",
            "name": "updated-network",
            "description": "Updated description",
        }
        self.mock_client.put.return_value = mock_network_data

        update_data = NetworkUpdate(
            name="updated-network", description="Updated description"
        )
        network = self.networks_resource.update("network-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "networks/network-123",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert network["name"] == "updated-network"

    def test_delete_network(self):
        """Test deleting a network."""
        self.networks_resource.delete("network-123")

        self.mock_client.delete.assert_called_once_with("networks/network-123")

    def test_create_resource(self):
        """Test creating a network resource."""
        mock_resource_data = {
            "id": "resource-123",
            "name": "test-resource",
            "address": "192.168.1.0/24",
            "enabled": True,
            "groups": [],
        }
        self.mock_client.post.return_value = mock_resource_data

        resource_data = {
            "name": "test-resource",
            "address": "192.168.1.0/24",
            "enabled": True,
            "groups": [],
        }
        resource = self.networks_resource.create_resource("network-123", resource_data)

        self.mock_client.post.assert_called_once_with(
            "networks/network-123/resources", data=resource_data
        )
        assert isinstance(resource, dict)

    def test_update_resource(self):
        """Test updating a network resource."""
        mock_resource_data = {
            "id": "resource-123",
            "name": "updated-resource",
            "address": "192.168.1.0/24",
            "enabled": False,
            "groups": [],
        }
        self.mock_client.put.return_value = mock_resource_data

        resource_data = {"enabled": False}
        resource = self.networks_resource.update_resource(
            "network-123", "resource-123", resource_data
        )

        self.mock_client.put.assert_called_once_with(
            "networks/network-123/resources/resource-123", data=resource_data
        )
        assert isinstance(resource, dict)

    def test_delete_resource(self):
        """Test deleting a network resource."""
        self.networks_resource.delete_resource("network-123", "resource-123")

        self.mock_client.delete.assert_called_once_with(
            "networks/network-123/resources/resource-123"
        )

    def test_create_router(self):
        """Test creating a network router."""
        mock_router_data = {
            "id": "router-123",
            "name": "test-router",
            "peer": "peer-123",
            "metric": 100,
            "masquerade": False,
            "enabled": True,
        }
        self.mock_client.post.return_value = mock_router_data

        router_data = {
            "name": "test-router",
            "peer": "peer-123",
            "metric": 100,
        }
        router = self.networks_resource.create_router("network-123", router_data)

        self.mock_client.post.assert_called_once_with(
            "networks/network-123/routers", data=router_data
        )
        assert isinstance(router, dict)

    def test_get_router(self):
        """Test getting a network router."""
        mock_router_data = {
            "id": "router-123",
            "name": "test-router",
            "peer": "peer-123",
            "metric": 100,
            "masquerade": False,
            "enabled": True,
        }
        self.mock_client.get.return_value = mock_router_data

        router = self.networks_resource.get_router("network-123", "router-123")

        self.mock_client.get.assert_called_once_with(
            "networks/network-123/routers/router-123"
        )
        assert isinstance(router, dict)

    def test_update_router(self):
        """Test updating a network router."""
        mock_router_data = {
            "id": "router-123",
            "name": "updated-router",
            "peer": "peer-123",
            "metric": 200,
            "masquerade": True,
            "enabled": True,
        }
        self.mock_client.put.return_value = mock_router_data

        router_data = {"metric": 200, "masquerade": True}
        router = self.networks_resource.update_router(
            "network-123", "router-123", router_data
        )

        self.mock_client.put.assert_called_once_with(
            "networks/network-123/routers/router-123", data=router_data
        )
        assert isinstance(router, dict)

    def test_delete_router(self):
        """Test deleting a network router."""
        self.networks_resource.delete_router("network-123", "router-123")

        self.mock_client.delete.assert_called_once_with(
            "networks/network-123/routers/router-123"
        )


class TestPeersResourceCompleteCode:
    """Test remaining peers resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.peers import PeersResource

        self.peers_resource = PeersResource(self.mock_client)

    def test_delete_peer(self):
        """Test deleting a peer."""
        self.peers_resource.delete("peer-123")

        self.mock_client.delete.assert_called_once_with("peers/peer-123")


class TestSetupKeysResourceCompleteCode:
    """Test remaining setup keys resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.setup_keys import SetupKeysResource

        self.setup_keys_resource = SetupKeysResource(self.mock_client)

    def test_get_setup_key(self):
        """Test getting a specific setup key."""

        mock_key_data = {
            "id": "key-123",
            "key": "test-key-value",
            "name": "test-key",
            "type": "reusable",
            "valid": True,
            "revoked": False,
            "used_times": 0,
            "state": "valid",
            "updated_at": "2023-01-01T00:00:00Z",
            "ephemeral": False,
        }
        self.mock_client.get.return_value = mock_key_data

        key = self.setup_keys_resource.get("key-123")

        self.mock_client.get.assert_called_once_with("setup-keys/key-123")
        assert isinstance(key, dict)
        assert key["id"] == "key-123"

    def test_update_setup_key(self):
        """Test updating a setup key."""
        from netbird.models import SetupKeyUpdate

        mock_key_data = {
            "id": "key-123",
            "key": "test-key-value",
            "name": "test-key",
            "type": "reusable",
            "valid": False,
            "revoked": True,
            "used_times": 5,
            "state": "revoked",
            "updated_at": "2023-01-01T00:00:00Z",
            "ephemeral": False,
        }
        self.mock_client.put.return_value = mock_key_data

        update_data = SetupKeyUpdate(revoked=True)
        key = self.setup_keys_resource.update("key-123", update_data)

        self.mock_client.put.assert_called_once_with(
            "setup-keys/key-123",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert key["revoked"]

    def test_delete_setup_key(self):
        """Test deleting a setup key."""
        self.setup_keys_resource.delete("key-123")

        self.mock_client.delete.assert_called_once_with("setup-keys/key-123")


class TestTokensResourceCompleteCode:
    """Test remaining tokens resource code paths."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        from netbird.resources.tokens import TokensResource

        self.tokens_resource = TokensResource(self.mock_client)

    def test_get_token(self):
        """Test getting a specific token."""

        mock_token_data = {
            "id": "token-123",
            "name": "test-token",
            "creation_date": "2023-01-01T00:00:00Z",
            "expiration_date": "2023-12-31T23:59:59Z",
            "created_by": "user-123",
        }
        self.mock_client.get.return_value = mock_token_data

        token = self.tokens_resource.get("user-123", "token-123")

        self.mock_client.get.assert_called_once_with("users/user-123/tokens/token-123")
        assert isinstance(token, dict)
        assert token["id"] == "token-123"

    def test_delete_token(self):
        """Test deleting a token."""
        self.tokens_resource.delete("user-123", "token-123")

        self.mock_client.delete.assert_called_once_with(
            "users/user-123/tokens/token-123"
        )
