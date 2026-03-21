"""
Unit tests for NetworksResource.
"""

from unittest.mock import MagicMock

import pytest

from netbird.models import NetworkCreate, NetworkUpdate
from netbird.resources.networks import NetworksResource


@pytest.mark.unit
class TestNetworksResource:
    """Test cases for NetworksResource methods."""

    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = NetworksResource(self.mock_client)

    # --- Network CRUD ---

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "net-1", "name": "prod-network"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("networks")
        assert len(result) == 1
        assert result[0]["name"] == "prod-network"

    def test_create(self):
        network_data = NetworkCreate(name="new-network", description="A new network")
        self.mock_client.post.return_value = {
            "id": "net-1",
            "name": "new-network",
        }
        result = self.resource.create(network_data)
        self.mock_client.post.assert_called_once_with(
            "networks", data=network_data.model_dump(exclude_unset=True)
        )
        assert result["id"] == "net-1"

    def test_get(self):
        self.mock_client.get.return_value = {
            "id": "net-1",
            "name": "prod-network",
        }
        result = self.resource.get("net-1")
        self.mock_client.get.assert_called_once_with("networks/net-1")
        assert result["name"] == "prod-network"

    def test_update(self):
        network_data = NetworkUpdate(name="updated-network")
        self.mock_client.put.return_value = {
            "id": "net-1",
            "name": "updated-network",
        }
        result = self.resource.update("net-1", network_data)
        self.mock_client.put.assert_called_once_with(
            "networks/net-1", data=network_data.model_dump(exclude_unset=True)
        )
        assert result["name"] == "updated-network"

    def test_delete(self):
        self.resource.delete("net-1")
        self.mock_client.delete.assert_called_once_with("networks/net-1")

    # --- Network Resources ---

    def test_list_resources(self):
        self.mock_client.get.return_value = [
            {"id": "res-1", "name": "web-server", "type": "host"},
        ]
        result = self.resource.list_resources("net-1")
        self.mock_client.get.assert_called_once_with("networks/net-1/resources")
        assert len(result) == 1

    def test_create_resource(self):
        res_data = {"name": "web-server", "address": "10.0.0.5", "type": "host"}
        self.mock_client.post.return_value = {"id": "res-1", **res_data}
        result = self.resource.create_resource("net-1", res_data)
        self.mock_client.post.assert_called_once_with(
            "networks/net-1/resources", data=res_data
        )
        assert result["id"] == "res-1"

    def test_get_resource(self):
        self.mock_client.get.return_value = {
            "id": "res-1",
            "name": "web-server",
        }
        result = self.resource.get_resource("net-1", "res-1")
        self.mock_client.get.assert_called_once_with("networks/net-1/resources/res-1")
        assert result["name"] == "web-server"

    def test_update_resource(self):
        res_data = {"name": "updated-server"}
        self.mock_client.put.return_value = {
            "id": "res-1",
            "name": "updated-server",
        }
        result = self.resource.update_resource("net-1", "res-1", res_data)
        self.mock_client.put.assert_called_once_with(
            "networks/net-1/resources/res-1", data=res_data
        )
        assert result["name"] == "updated-server"

    def test_delete_resource(self):
        self.resource.delete_resource("net-1", "res-1")
        self.mock_client.delete.assert_called_once_with(
            "networks/net-1/resources/res-1"
        )

    # --- Network Routers ---

    def test_list_routers(self):
        self.mock_client.get.return_value = [
            {"id": "router-1", "name": "main-router"},
        ]
        result = self.resource.list_routers("net-1")
        self.mock_client.get.assert_called_once_with("networks/net-1/routers")
        assert len(result) == 1

    def test_create_router(self):
        router_data = {"name": "main-router", "peer": "peer-1"}
        self.mock_client.post.return_value = {"id": "router-1", **router_data}
        result = self.resource.create_router("net-1", router_data)
        self.mock_client.post.assert_called_once_with(
            "networks/net-1/routers", data=router_data
        )
        assert result["id"] == "router-1"

    def test_get_router(self):
        self.mock_client.get.return_value = {
            "id": "router-1",
            "name": "main-router",
        }
        result = self.resource.get_router("net-1", "router-1")
        self.mock_client.get.assert_called_once_with(
            "networks/net-1/routers/router-1"
        )
        assert result["name"] == "main-router"

    def test_update_router(self):
        router_data = {"name": "updated-router"}
        self.mock_client.put.return_value = {
            "id": "router-1",
            "name": "updated-router",
        }
        result = self.resource.update_router("net-1", "router-1", router_data)
        self.mock_client.put.assert_called_once_with(
            "networks/net-1/routers/router-1", data=router_data
        )
        assert result["name"] == "updated-router"

    def test_delete_router(self):
        self.resource.delete_router("net-1", "router-1")
        self.mock_client.delete.assert_called_once_with(
            "networks/net-1/routers/router-1"
        )

    # --- New: list_all_routers ---

    def test_list_all_routers(self):
        self.mock_client.get.return_value = [
            {"id": "router-1", "name": "router-a"},
            {"id": "router-2", "name": "router-b"},
        ]
        result = self.resource.list_all_routers()
        self.mock_client.get.assert_called_once_with("networks/routers")
        assert len(result) == 2
