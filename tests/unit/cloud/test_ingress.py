"""
Unit tests for IngressResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.ingress import IngressResource
from netbird.models.cloud.ingress import (
    IngressPeerCreate,
    IngressPeerUpdate,
    PortAllocationCreate,
    PortAllocationUpdate,
)


@pytest.mark.unit
class TestIngressResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = IngressResource(self.mock_client)

    # Port allocation tests

    def test_list_ports(self):
        self.mock_client.get.return_value = [
            {"id": "port-1", "name": "http"},
            {"id": "port-2", "name": "https"},
        ]
        result = self.resource.list_ports("peer-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1/ingress/ports")
        assert len(result) == 2
        assert result[0]["name"] == "http"

    def test_create_port(self):
        port_data = PortAllocationCreate(
            name="http",
            enabled=True,
            port_ranges=[{"start": 80, "end": 80}],
        )
        self.mock_client.post.return_value = {"id": "port-1", "name": "http"}
        result = self.resource.create_port("peer-1", port_data)
        self.mock_client.post.assert_called_once_with(
            "peers/peer-1/ingress/ports",
            data=port_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "port-1"

    def test_get_port(self):
        self.mock_client.get.return_value = {"id": "port-1", "name": "http"}
        result = self.resource.get_port("peer-1", "port-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1/ingress/ports/port-1")
        assert result["name"] == "http"

    def test_update_port(self):
        update_data = PortAllocationUpdate(name="http-updated", enabled=False)
        self.mock_client.put.return_value = {"id": "port-1", "name": "http-updated", "enabled": False}
        result = self.resource.update_port("peer-1", "port-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "peers/peer-1/ingress/ports/port-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["enabled"] is False

    def test_delete_port(self):
        self.resource.delete_port("peer-1", "port-1")
        self.mock_client.delete.assert_called_once_with("peers/peer-1/ingress/ports/port-1")

    # Ingress peer tests

    def test_list_peers(self):
        self.mock_client.get.return_value = [
            {"id": "ingress-1", "peer_id": "peer-1"},
        ]
        result = self.resource.list_peers()
        self.mock_client.get.assert_called_once_with("ingress/peers")
        assert len(result) == 1

    def test_create_peer(self):
        peer_data = IngressPeerCreate(
            peer_id="peer-1",
            enabled=True,
            fallback=False,
        )
        self.mock_client.post.return_value = {"id": "ingress-1", "peer_id": "peer-1"}
        result = self.resource.create_peer(peer_data)
        self.mock_client.post.assert_called_once_with(
            "ingress/peers",
            data=peer_data.model_dump(exclude_unset=True),
        )
        assert result["peer_id"] == "peer-1"

    def test_get_peer(self):
        self.mock_client.get.return_value = {"id": "ingress-1", "peer_id": "peer-1"}
        result = self.resource.get_peer("ingress-1")
        self.mock_client.get.assert_called_once_with("ingress/peers/ingress-1")
        assert result["id"] == "ingress-1"

    def test_update_peer(self):
        update_data = IngressPeerUpdate(enabled=False, fallback=True)
        self.mock_client.put.return_value = {"id": "ingress-1", "enabled": False, "fallback": True}
        result = self.resource.update_peer("ingress-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "ingress/peers/ingress-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["fallback"] is True

    def test_delete_peer(self):
        self.resource.delete_peer("ingress-1")
        self.mock_client.delete.assert_called_once_with("ingress/peers/ingress-1")
