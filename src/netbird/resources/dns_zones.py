"""
DNS zones resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models.dns_zone import DNSRecordCreate, DNSRecordUpdate, DNSZoneCreate, DNSZoneUpdate
from .base import BaseResource


class DNSZonesResource(BaseResource):
    """Handler for NetBird DNS zones API endpoints.

    This resource manages DNS zones and records. It is separate from the
    DNSResource which manages nameserver groups and DNS settings.
    """

    # Zone CRUD

    def list(self) -> List[Dict[str, Any]]:
        """List all DNS zones.

        Returns:
            List of DNS zone dictionaries
        """
        data = self.client.get("dns/zones")
        return self._parse_list_response(data)

    def create(self, zone_data: DNSZoneCreate) -> Dict[str, Any]:
        """Create a new DNS zone.

        Args:
            zone_data: DNS zone creation data

        Returns:
            Created DNS zone dictionary
        """
        data = self.client.post(
            "dns/zones", data=zone_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def get(self, zone_id: str) -> Dict[str, Any]:
        """Retrieve a specific DNS zone.

        Args:
            zone_id: Unique zone identifier

        Returns:
            DNS zone dictionary
        """
        data = self.client.get(f"dns/zones/{zone_id}")
        return self._parse_response(data)

    def update(self, zone_id: str, zone_data: DNSZoneUpdate) -> Dict[str, Any]:
        """Update a DNS zone.

        Args:
            zone_id: Unique zone identifier
            zone_data: DNS zone update data

        Returns:
            Updated DNS zone dictionary
        """
        data = self.client.put(
            f"dns/zones/{zone_id}", data=zone_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def delete(self, zone_id: str) -> None:
        """Delete a DNS zone.

        Args:
            zone_id: Unique zone identifier
        """
        self.client.delete(f"dns/zones/{zone_id}")

    # Record CRUD

    def list_records(self, zone_id: str) -> List[Dict[str, Any]]:
        """List all records in a DNS zone.

        Args:
            zone_id: Unique zone identifier

        Returns:
            List of DNS record dictionaries
        """
        data = self.client.get(f"dns/zones/{zone_id}/records")
        return self._parse_list_response(data)

    def create_record(
        self, zone_id: str, record_data: DNSRecordCreate
    ) -> Dict[str, Any]:
        """Create a DNS record in a zone.

        Args:
            zone_id: Unique zone identifier
            record_data: DNS record creation data

        Returns:
            Created DNS record dictionary
        """
        data = self.client.post(
            f"dns/zones/{zone_id}/records",
            data=record_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get_record(self, zone_id: str, record_id: str) -> Dict[str, Any]:
        """Retrieve a specific DNS record.

        Args:
            zone_id: Unique zone identifier
            record_id: Unique record identifier

        Returns:
            DNS record dictionary
        """
        data = self.client.get(f"dns/zones/{zone_id}/records/{record_id}")
        return self._parse_response(data)

    def update_record(
        self, zone_id: str, record_id: str, record_data: DNSRecordUpdate
    ) -> Dict[str, Any]:
        """Update a DNS record.

        Args:
            zone_id: Unique zone identifier
            record_id: Unique record identifier
            record_data: DNS record update data

        Returns:
            Updated DNS record dictionary
        """
        data = self.client.put(
            f"dns/zones/{zone_id}/records/{record_id}",
            data=record_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete_record(self, zone_id: str, record_id: str) -> None:
        """Delete a DNS record.

        Args:
            zone_id: Unique zone identifier
            record_id: Unique record identifier
        """
        self.client.delete(f"dns/zones/{zone_id}/records/{record_id}")
