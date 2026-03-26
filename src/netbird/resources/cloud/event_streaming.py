"""
Event streaming resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ...models.cloud.event_streaming import EventStreamingCreate, EventStreamingUpdate
from ..base import BaseResource


class EventStreamingResource(BaseResource):
    """Handler for NetBird event streaming integration API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all event streaming integrations."""
        data = self.client.get("integrations/event-streaming")
        return self._parse_list_response(data)

    def create(self, integration_data: EventStreamingCreate) -> Dict[str, Any]:
        """Create an event streaming integration."""
        data = self.client.post(
            "integrations/event-streaming",
            data=integration_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self, integration_id: str) -> Dict[str, Any]:
        """Retrieve a specific event streaming integration."""
        data = self.client.get(f"event-streaming/{integration_id}")
        return self._parse_response(data)

    def update(
        self, integration_id: str, integration_data: EventStreamingUpdate
    ) -> Dict[str, Any]:
        """Update an event streaming integration."""
        data = self.client.put(
            f"event-streaming/{integration_id}",
            data=integration_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, integration_id: str) -> None:
        """Delete an event streaming integration."""
        self.client.delete(f"event-streaming/{integration_id}")
