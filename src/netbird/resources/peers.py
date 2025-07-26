"""
Peers resource handler for NetBird API.
"""

from typing import List, Optional

from ..models import Peer, PeerUpdate
from .base import BaseResource


class PeersResource(BaseResource):
    """Handler for NetBird peers API endpoints.
    
    Provides methods to manage NetBird peers including listing,
    retrieving, updating, and deleting peers.
    """
    
    def list(self, name: Optional[str] = None, ip: Optional[str] = None) -> List[Peer]:
        """List all peers with optional filtering.
        
        Args:
            name: Filter peers by name (optional)
            ip: Filter peers by IP address (optional)
            
        Returns:
            List of Peer objects
            
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
        return self._parse_list_response(data, Peer)
    
    def get(self, peer_id: str) -> Peer:
        """Retrieve a specific peer.
        
        Args:
            peer_id: Unique peer identifier
            
        Returns:
            Peer object
            
        Example:
            >>> peer = client.peers.get("peer-123")
            >>> print(f"Peer: {peer.name} ({peer.ip})")
        """
        data = self.client.get(f"peers/{peer_id}")
        return self._parse_response(data, Peer)
    
    def update(self, peer_id: str, peer_data: PeerUpdate) -> Peer:
        """Update a peer.
        
        Args:
            peer_id: Unique peer identifier
            peer_data: Peer update data
            
        Returns:
            Updated Peer object
            
        Example:
            >>> peer_data = PeerUpdate(
            ...     name="updated-server",
            ...     ssh_enabled=True
            ... )
            >>> peer = client.peers.update("peer-123", peer_data)
        """
        data = self.client.put(
            f"peers/{peer_id}",
            data=peer_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data, Peer)
    
    def delete(self, peer_id: str) -> None:
        """Delete a peer.
        
        Args:
            peer_id: Unique peer identifier
            
        Example:
            >>> client.peers.delete("peer-123")
        """
        self.client.delete(f"peers/{peer_id}")
    
    def get_accessible_peers(self, peer_id: str) -> List[Peer]:
        """List peers that a specific peer can connect to.
        
        Args:
            peer_id: Unique peer identifier
            
        Returns:
            List of accessible Peer objects
            
        Example:
            >>> accessible = client.peers.get_accessible_peers("peer-123")
            >>> print(f"Can connect to {len(accessible)} peers")
        """
        data = self.client.get(f"peers/{peer_id}/accessible-peers")
        return self._parse_list_response(data, Peer)
