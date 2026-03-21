"""
EDR peer bypass resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..base import BaseResource


class EDRPeersResource(BaseResource):
    """Handler for NetBird EDR peer bypass API endpoints."""

    def bypass(self, peer_id: str) -> Dict[str, Any]:
        """Bypass compliance for a non-compliant peer."""
        data = self.client.post(f"peers/{peer_id}/edr/bypass")
        return self._parse_response(data)

    def revoke_bypass(self, peer_id: str) -> None:
        """Revoke compliance bypass for a peer."""
        self.client.delete(f"peers/{peer_id}/edr/bypass")

    def list_bypassed(self) -> List[Dict[str, Any]]:
        """List all bypassed peers."""
        data = self.client.get("peers/edr/bypassed")
        return self._parse_list_response(data)
