"""
EDR Huntress resource handler for NetBird API.
"""

from typing import Any, Dict

from ...models.cloud.edr import EDRHuntressConfig
from ..base import BaseResource


class EDRHuntressResource(BaseResource):
    """Handler for Huntress EDR integration endpoints."""

    def create(self, config: EDRHuntressConfig) -> Dict[str, Any]:
        """Create Huntress EDR integration."""
        data = self.client.post(
            "integrations/edr/huntress",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self) -> Dict[str, Any]:
        """Get Huntress EDR integration."""
        data = self.client.get("integrations/edr/huntress")
        return self._parse_response(data)

    def update(self, config: EDRHuntressConfig) -> Dict[str, Any]:
        """Update Huntress EDR integration."""
        data = self.client.put(
            "integrations/edr/huntress",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self) -> None:
        """Delete Huntress EDR integration."""
        self.client.delete("integrations/edr/huntress")
