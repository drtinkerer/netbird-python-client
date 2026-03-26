"""
Unit tests for EventStreamingResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.event_streaming import EventStreamingResource
from netbird.models.cloud.event_streaming import EventStreamingCreate, EventStreamingUpdate


@pytest.mark.unit
class TestEventStreamingResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EventStreamingResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "es-1", "platform": "datadog"},
            {"id": "es-2", "platform": "s3"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("integrations/event-streaming")
        assert len(result) == 2
        assert result[0]["platform"] == "datadog"

    def test_create(self):
        create_data = EventStreamingCreate(
            platform="datadog",
            config={"api_key": "dd-key", "site": "datadoghq.com"},
            enabled=True,
        )
        self.mock_client.post.return_value = {"id": "es-1", "platform": "datadog"}
        result = self.resource.create(create_data)
        self.mock_client.post.assert_called_once_with(
            "integrations/event-streaming",
            data=create_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "es-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "es-1", "platform": "datadog", "enabled": True}
        result = self.resource.get("es-1")
        self.mock_client.get.assert_called_once_with("event-streaming/es-1")
        assert result["enabled"] is True

    def test_update(self):
        update_data = EventStreamingUpdate(enabled=False)
        self.mock_client.put.return_value = {"id": "es-1", "enabled": False}
        result = self.resource.update("es-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "event-streaming/es-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["enabled"] is False

    def test_delete(self):
        self.resource.delete("es-1")
        self.mock_client.delete.assert_called_once_with("event-streaming/es-1")
