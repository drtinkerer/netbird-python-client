"""
DNS resource handler for NetBird API.
"""

from typing import List

from ..models import DNSNameserverGroup, DNSSettings
from .base import BaseResource


class DNSResource(BaseResource):
    """Handler for NetBird DNS API endpoints.
    
    Provides methods to manage NetBird DNS settings including
    nameserver groups and DNS configuration.
    """
    
    # Nameserver Groups
    
    def list_nameserver_groups(self) -> List[DNSNameserverGroup]:
        """List all nameserver groups.
        
        Returns:
            List of DNSNameserverGroup objects
            
        Example:
            >>> nameservers = client.dns.list_nameserver_groups()
            >>> for ns in nameservers:
            ...     print(f"Nameserver Group: {ns.name}")
        """
        data = self.client.get("dns/nameservers")
        return self._parse_list_response(data, DNSNameserverGroup)
    
    def create_nameserver_group(self, nameserver_data: dict) -> DNSNameserverGroup:
        """Create a new nameserver group.
        
        Args:
            nameserver_data: Nameserver group creation data
            
        Returns:
            Created DNSNameserverGroup object
            
        Example:
            >>> nameserver_data = {
            ...     "name": "Corporate DNS",
            ...     "description": "Internal corporate nameservers",
            ...     "nameservers": ["10.0.0.10", "10.0.0.11"],
            ...     "enabled": True
            ... }
            >>> ns_group = client.dns.create_nameserver_group(nameserver_data)
        """
        data = self.client.post("dns/nameservers", data=nameserver_data)
        return self._parse_response(data, DNSNameserverGroup)
    
    def get_nameserver_group(self, group_id: str) -> DNSNameserverGroup:
        """Retrieve a specific nameserver group.
        
        Args:
            group_id: Unique nameserver group identifier
            
        Returns:
            DNSNameserverGroup object
            
        Example:
            >>> ns_group = client.dns.get_nameserver_group("ns-group-123")
            >>> print(f"Nameservers: {ns_group.nameservers}")
        """
        data = self.client.get(f"dns/nameservers/{group_id}")
        return self._parse_response(data, DNSNameserverGroup)
    
    def update_nameserver_group(self, group_id: str, nameserver_data: dict) -> DNSNameserverGroup:
        """Update a nameserver group.
        
        Args:
            group_id: Unique nameserver group identifier
            nameserver_data: Nameserver group update data
            
        Returns:
            Updated DNSNameserverGroup object
            
        Example:
            >>> nameserver_data = {
            ...     "enabled": False,
            ...     "description": "Disabled for maintenance"
            ... }
            >>> ns_group = client.dns.update_nameserver_group("ns-group-123", nameserver_data)
        """
        data = self.client.put(f"dns/nameservers/{group_id}", data=nameserver_data)
        return self._parse_response(data, DNSNameserverGroup)
    
    def delete_nameserver_group(self, group_id: str) -> None:
        """Delete a nameserver group.
        
        Args:
            group_id: Unique nameserver group identifier
            
        Example:
            >>> client.dns.delete_nameserver_group("ns-group-123")
        """
        self.client.delete(f"dns/nameservers/{group_id}")
    
    # DNS Settings
    
    def get_settings(self) -> DNSSettings:
        """Retrieve DNS settings.
        
        Returns:
            DNSSettings object
            
        Example:
            >>> settings = client.dns.get_settings()
            >>> print(f"Disabled groups: {settings.disabled_management_groups}")
        """
        data = self.client.get("dns/settings")
        return self._parse_response(data, DNSSettings)
    
    def update_settings(self, settings_data: dict) -> DNSSettings:
        """Update DNS settings.
        
        Args:
            settings_data: DNS settings update data
            
        Returns:
            Updated DNSSettings object
            
        Example:
            >>> settings_data = {
            ...     "disabled_management_groups": ["group-123"]
            ... }
            >>> settings = client.dns.update_settings(settings_data)
        """
        data = self.client.put("dns/settings", data=settings_data)
        return self._parse_response(data, DNSSettings)
