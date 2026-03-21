"""
Usage resource handler for NetBird API.
"""

from typing import Any, Dict

from ..base import BaseResource


class UsageResource(BaseResource):
    """Handler for NetBird billing usage API endpoints."""

    def get(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        data = self.client.get("integrations/billing/usage")
        return self._parse_response(data)
