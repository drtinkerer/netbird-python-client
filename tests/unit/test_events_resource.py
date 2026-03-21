"""
Unit tests for EventsResource.
"""

from unittest.mock import MagicMock

import pytest

from netbird.resources.events import EventsResource


@pytest.mark.unit
class TestEventsResource:
    """Test cases for EventsResource methods."""

    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EventsResource(self.mock_client)

    # --- Existing ---

    def test_get_audit_events(self):
        self.mock_client.get.return_value = [
            {"id": "evt-1", "activity": "user.login", "timestamp": "2024-01-01T00:00:00Z"},
        ]
        result = self.resource.get_audit_events()
        self.mock_client.get.assert_called_once_with("events/audit")
        assert len(result) == 1
        assert result[0]["activity"] == "user.login"

    def test_get_network_traffic_events_no_params(self):
        self.mock_client.get.return_value = [
            {"id": "evt-1", "protocol": "tcp"},
        ]
        result = self.resource.get_network_traffic_events()
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic", params=None
        )
        assert len(result) == 1

    def test_get_network_traffic_events_with_filters(self):
        self.mock_client.get.return_value = [
            {"id": "evt-1", "protocol": "tcp"},
        ]
        result = self.resource.get_network_traffic_events(
            page=1,
            page_size=50,
            user_id="user-1",
            protocol="tcp",
            connection_type="p2p",
            direction="sent",
        )
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic",
            params={
                "page": 1,
                "page_size": 50,
                "user_id": "user-1",
                "protocol": "tcp",
                "connection_type": "p2p",
                "direction": "sent",
            },
        )
        assert len(result) == 1

    def test_get_network_traffic_events_with_date_range(self):
        self.mock_client.get.return_value = []
        result = self.resource.get_network_traffic_events(
            start_date="2024-01-01", end_date="2024-01-31"
        )
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic",
            params={"start_date": "2024-01-01", "end_date": "2024-01-31"},
        )
        assert result == []

    def test_get_network_traffic_events_with_reporter_and_type(self):
        self.mock_client.get.return_value = []
        result = self.resource.get_network_traffic_events(
            reporter_id="peer-1", event_type="connection", search="test"
        )
        self.mock_client.get.assert_called_once_with(
            "events/network-traffic",
            params={
                "reporter_id": "peer-1",
                "type": "connection",
                "search": "test",
            },
        )

    # --- New: Proxy events ---

    def test_get_proxy_events_no_params(self):
        self.mock_client.get.return_value = [
            {"id": "evt-1", "method": "GET", "status_code": 200},
        ]
        result = self.resource.get_proxy_events()
        self.mock_client.get.assert_called_once_with("events/proxy", params=None)
        assert len(result) == 1

    def test_get_proxy_events_with_pagination(self):
        self.mock_client.get.return_value = []
        result = self.resource.get_proxy_events(page=2, page_size=25)
        self.mock_client.get.assert_called_once_with(
            "events/proxy", params={"page": 2, "page_size": 25}
        )

    def test_get_proxy_events_with_sorting(self):
        self.mock_client.get.return_value = []
        result = self.resource.get_proxy_events(
            sort_by="timestamp", sort_order="desc"
        )
        self.mock_client.get.assert_called_once_with(
            "events/proxy",
            params={"sort_by": "timestamp", "sort_order": "desc"},
        )

    def test_get_proxy_events_with_filters(self):
        self.mock_client.get.return_value = [
            {"id": "evt-1", "method": "POST", "status_code": 201},
        ]
        result = self.resource.get_proxy_events(
            source_ip="192.168.1.1",
            host="api.example.com",
            path="/v1/users",
            user_id="user-1",
            user_email="alice@example.com",
            user_name="Alice",
            method="POST",
            status="success",
            status_code=201,
            search="create",
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-01-31T23:59:59Z",
        )
        self.mock_client.get.assert_called_once_with(
            "events/proxy",
            params={
                "source_ip": "192.168.1.1",
                "host": "api.example.com",
                "path": "/v1/users",
                "user_id": "user-1",
                "user_email": "alice@example.com",
                "user_name": "Alice",
                "method": "POST",
                "status": "success",
                "status_code": 201,
                "search": "create",
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
            },
        )
        assert len(result) == 1

    def test_get_proxy_events_with_status_code_zero(self):
        """Ensure status_code=0 is still sent (it is not None)."""
        self.mock_client.get.return_value = []
        result = self.resource.get_proxy_events(status_code=0)
        self.mock_client.get.assert_called_once_with(
            "events/proxy", params={"status_code": 0}
        )
