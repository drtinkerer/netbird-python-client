"""
Peers resource handler for NetBird API.
"""

from typing import Any, Dict, List, Optional

from ..models import PeerUpdate
from .base import BaseResource


class PeersResource(BaseResource):
    """Handler for NetBird peers API endpoints.

    Provides methods to manage NetBird peers including listing,
    retrieving, updating, and deleting peers.
    """

    def list(
        self, name: Optional[str] = None, ip: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all peers with optional filtering.

        Args:
            name: Filter peers by name (optional)
            ip: Filter peers by IP address (optional)

        Returns:
            List of peer dictionaries

        Example:
            >>> # List all peers
            >>> peers = client.peers.list()
            >>>
            >>> # Filter by name
            >>> peers = client.peers.list(name="server-01")
            >>>
            >>> # Filter by IP
            >>> peers = client.peers.list(ip="10.0.0.1")
        """
        params = {}
        if name:
            params["name"] = name
        if ip:
            params["ip"] = ip

        data = self.client.get("peers", params=params or None)
        return self._parse_list_response(data)

    def get(self, peer_id: str) -> Dict[str, Any]:
        """Retrieve a specific peer.

        Args:
            peer_id: Unique peer identifier

        Returns:
            Peer dictionary

        Example:
            >>> peer = client.peers.get("peer-123")
            >>> print(f"Peer: {peer['name']} ({peer['ip']})")
        """
        data = self.client.get(f"peers/{peer_id}")
        return self._parse_response(data)

    def update(self, peer_id: str, peer_data: PeerUpdate) -> Dict[str, Any]:
        """Update a peer.

        Args:
            peer_id: Unique peer identifier
            peer_data: Peer update data

        Returns:
            Updated peer dictionary

        Example:
            >>> peer_data = PeerUpdate(
            ...     name="updated-server",
            ...     ssh_enabled=True
            ... )
            >>> peer = client.peers.update("peer-123", peer_data)
        """
        data = self.client.put(
            f"peers/{peer_id}", data=peer_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def delete(self, peer_id: str) -> None:
        """Delete a peer.

        Args:
            peer_id: Unique peer identifier

        Example:
            >>> client.peers.delete("peer-123")
        """
        self.client.delete(f"peers/{peer_id}")

    def get_accessible_peers(self, peer_id: str) -> List[Dict[str, Any]]:
        """List peers that a specific peer can connect to.

        Args:
            peer_id: Unique peer identifier

        Returns:
            List of accessible peer dictionaries

        Example:
            >>> accessible = client.peers.get_accessible_peers("peer-123")
            >>> print(f"Can connect to {len(accessible)} peers")
        """
        data = self.client.get(f"peers/{peer_id}/accessible-peers")
        return self._parse_list_response(data)

    def create_temporary_access(
        self, peer_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a temporary access peer.

        Args:
            peer_id: Unique peer identifier
            data: Temporary access data (name, wg_pub_key, rules)

        Returns:
            Created temporary access peer dictionary
        """
        result = self.client.post(f"peers/{peer_id}/temporary-access", data=data)
        return self._parse_response(result)

    # Jobs (scoped under peers)

    def list_jobs(self, peer_id: str) -> List[Dict[str, Any]]:
        """List all jobs for a peer.

        Args:
            peer_id: Unique peer identifier

        Returns:
            List of job dictionaries
        """
        data = self.client.get(f"peers/{peer_id}/jobs")
        return self._parse_list_response(data)

    def create_job(self, peer_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a job for a peer.

        Args:
            peer_id: Unique peer identifier
            job_data: Job creation data (workload)

        Returns:
            Created job dictionary
        """
        data = self.client.post(f"peers/{peer_id}/jobs", data=job_data)
        return self._parse_response(data)

    def get_job(self, peer_id: str, job_id: str) -> Dict[str, Any]:
        """Retrieve a specific job for a peer.

        Args:
            peer_id: Unique peer identifier
            job_id: Unique job identifier

        Returns:
            Job dictionary
        """
        data = self.client.get(f"peers/{peer_id}/jobs/{job_id}")
        return self._parse_response(data)
