"""
EDR SentinelOne resource handler for NetBird API.
"""

from typing import Any, Dict

from ...models.cloud.edr import EDRSentinelOneConfig
from ..base import BaseResource


class EDRSentinelOneResource(BaseResource):
    """Handler for SentinelOne EDR integration endpoints."""

    def create(self, config: EDRSentinelOneConfig) -> Dict[str, Any]:
        """Create SentinelOne EDR integration."""
        data = self.client.post(
            "integrations/edr/sentinelone",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self) -> Dict[str, Any]:
        """Get SentinelOne EDR integration."""
        data = self.client.get("integrations/edr/sentinelone")
        return self._parse_response(data)

    def update(self, config: EDRSentinelOneConfig) -> Dict[str, Any]:
        """Update SentinelOne EDR integration."""
        data = self.client.put(
            "integrations/edr/sentinelone",
            data=config.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self) -> None:
        """Delete SentinelOne EDR integration."""
        self.client.delete("integrations/edr/sentinelone")
