"""
Events resource handler for NetBird API.
"""

from typing import List, Optional

from ..models import AuditEvent, NetworkTrafficEvent
from .base import BaseResource


class EventsResource(BaseResource):
    """Handler for NetBird events API endpoints.
    
    Provides methods to retrieve audit events and network traffic events.
    """
    
    def get_audit_events(self) -> List[AuditEvent]:
        """Retrieve all audit events.
        
        Returns:
            List of AuditEvent objects
            
        Example:
            >>> events = client.events.get_audit_events()
            >>> for event in events:
            ...     print(f"{event.timestamp}: {event.activity}")
        """
        data = self.client.get("events/audit")
        return self._parse_list_response(data, AuditEvent)
    
    def get_network_traffic_events(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        user_id: Optional[str] = None,
        reporter_id: Optional[str] = None,
        protocol: Optional[str] = None,
        event_type: Optional[str] = None,
        connection_type: Optional[str] = None,
        direction: Optional[str] = None,
        search: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[NetworkTrafficEvent]:
        """Retrieve network traffic events with optional filtering.
        
        This endpoint is marked as "cloud-only experimental" in the API.
        
        Args:
            page: Page number for pagination
            page_size: Number of events per page
            user_id: Filter by user ID
            reporter_id: Filter by reporter peer ID
            protocol: Filter by protocol (tcp, udp, icmp)
            event_type: Filter by event type
            connection_type: Filter by connection type (relay, p2p)
            direction: Filter by traffic direction (sent, received)
            search: Search term
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            List of NetworkTrafficEvent objects
            
        Example:
            >>> # Get all traffic events
            >>> events = client.events.get_network_traffic_events()
            >>> 
            >>> # Filter by protocol and user
            >>> events = client.events.get_network_traffic_events(
            ...     protocol="tcp",
            ...     user_id="user-123",
            ...     page_size=50
            ... )
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if user_id:
            params["user_id"] = user_id
        if reporter_id:
            params["reporter_id"] = reporter_id
        if protocol:
            params["protocol"] = protocol
        if event_type:
            params["type"] = event_type
        if connection_type:
            params["connection_type"] = connection_type
        if direction:
            params["direction"] = direction
        if search:
            params["search"] = search
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        data = self.client.get("events/network-traffic", params=params or None)
        return self._parse_list_response(data, NetworkTrafficEvent)
