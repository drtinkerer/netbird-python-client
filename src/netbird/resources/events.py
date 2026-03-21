"""
Events resource handler for NetBird API.
"""

from typing import Any, Dict, List, Optional

from .base import BaseResource


class EventsResource(BaseResource):
    """Handler for NetBird events API endpoints.

    Provides methods to retrieve audit events and network traffic events.
    """

    def get_audit_events(self) -> List[Dict[str, Any]]:
        """Retrieve all audit events.

        Returns:
            List of audit event dictionaries

        Example:
            >>> events = client.events.get_audit_events()
            >>> for event in events:
            ...     print(f"{event['timestamp']}: {event['activity']}")
        """
        data = self.client.get("events/audit")
        return self._parse_list_response(data)

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
    ) -> List[Dict[str, Any]]:
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
            List of network traffic event dictionaries

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
        params: Dict[str, Any] = {}
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
        return self._parse_list_response(data)

    def get_proxy_events(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        search: Optional[str] = None,
        source_ip: Optional[str] = None,
        host: Optional[str] = None,
        path: Optional[str] = None,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        user_name: Optional[str] = None,
        method: Optional[str] = None,
        status: Optional[str] = None,
        status_code: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve reverse proxy access log events.

        Args:
            page: Page number for pagination
            page_size: Number of events per page
            sort_by: Sort field
            sort_order: Sort direction
            search: Search term
            source_ip: Filter by source IP
            host: Filter by host
            path: Filter by path
            user_id: Filter by user ID
            user_email: Filter by user email
            user_name: Filter by user name
            method: Filter by HTTP method
            status: Filter by status
            status_code: Filter by status code
            start_date: Start date filter (RFC3339)
            end_date: End date filter (RFC3339)

        Returns:
            List of proxy event dictionaries
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort_by:
            params["sort_by"] = sort_by
        if sort_order:
            params["sort_order"] = sort_order
        if search:
            params["search"] = search
        if source_ip:
            params["source_ip"] = source_ip
        if host:
            params["host"] = host
        if path:
            params["path"] = path
        if user_id:
            params["user_id"] = user_id
        if user_email:
            params["user_email"] = user_email
        if user_name:
            params["user_name"] = user_name
        if method:
            params["method"] = method
        if status:
            params["status"] = status
        if status_code is not None:
            params["status_code"] = status_code
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        data = self.client.get("events/proxy", params=params or None)
        return self._parse_list_response(data)
