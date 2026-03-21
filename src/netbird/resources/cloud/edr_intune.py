"""
EDR Intune resource handler for NetBird API.
"""

from typing import Any, Dict

from ...models.cloud.edr import EDRIntuneConfig
from ..base import BaseResource


class EDRIntuneResource(BaseResource):
    """Handler for Intune EDR integration endpoints."""

    def create(self, config: EDRIntuneConfig) -> Dict[str, Any]:
        """Create Intune EDR integration."""
        data = self.client.post(
            "integrations/edr/intune",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self) -> Dict[str, Any]:
        """Get Intune EDR integration."""
        data = self.client.get("integrations/edr/intune")
        return self._parse_response(data)

    def update(self, config: EDRIntuneConfig) -> Dict[str, Any]:
        """Update Intune EDR integration."""
        data = self.client.put(
            "integrations/edr/intune",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self) -> None:
        """Delete Intune EDR integration."""
        self.client.delete("integrations/edr/intune")
