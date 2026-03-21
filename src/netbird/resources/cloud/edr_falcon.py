"""
EDR Falcon resource handler for NetBird API.
"""

from typing import Any, Dict

from ...models.cloud.edr import EDRFalconConfig
from ..base import BaseResource


class EDRFalconResource(BaseResource):
    """Handler for CrowdStrike Falcon EDR integration endpoints."""

    def create(self, config: EDRFalconConfig) -> Dict[str, Any]:
        """Create Falcon EDR integration."""
        data = self.client.post(
            "integrations/edr/falcon",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self) -> Dict[str, Any]:
        """Get Falcon EDR integration."""
        data = self.client.get("integrations/edr/falcon")
        return self._parse_response(data)

    def update(self, config: EDRFalconConfig) -> Dict[str, Any]:
        """Update Falcon EDR integration."""
        data = self.client.put(
            "integrations/edr/falcon",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self) -> None:
        """Delete Falcon EDR integration."""
        self.client.delete("integrations/edr/falcon")
