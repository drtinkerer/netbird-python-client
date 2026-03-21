"""Tests for DNSZonesResource."""

import pytest
from unittest.mock import MagicMock

from netbird.resources.dns_zones import DNSZonesResource
from netbird.models.dns_zone import (
    DNSZoneCreate,
    DNSZoneUpdate,
    DNSRecordCreate,
    DNSRecordUpdate,
)


@pytest.mark.unit
class TestDNSZonesResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = DNSZonesResource(self.mock_client)

    # Zone CRUD

    def test_list(self):
        self.mock_client.get.return_value = [{"id": "zone-1", "name": "internal"}]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("dns/zones")
        assert len(result) == 1

    def test_create(self):
        self.mock_client.post.return_value = {"id": "zone-1", "name": "internal"}
        zone_data = DNSZoneCreate(
            name="internal",
            domain="internal.example.com",
            enable_search_domain=True,
            distribution_groups=["group-1"],
        )
        result = self.resource.create(zone_data)
        self.mock_client.post.assert_called_once_with(
            "dns/zones", data=zone_data.model_dump(exclude_unset=True)
        )
        assert result["id"] == "zone-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "zone-1"}
        result = self.resource.get("zone-1")
        self.mock_client.get.assert_called_once_with("dns/zones/zone-1")
        assert result["id"] == "zone-1"

    def test_update(self):
        self.mock_client.put.return_value = {"id": "zone-1", "name": "updated"}
        update_data = DNSZoneUpdate(name="updated")
        result = self.resource.update("zone-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "dns/zones/zone-1", data=update_data.model_dump(exclude_unset=True)
        )
        assert result["name"] == "updated"

    def test_delete(self):
        self.resource.delete("zone-1")
        self.mock_client.delete.assert_called_once_with("dns/zones/zone-1")

    # Record CRUD

    def test_list_records(self):
        self.mock_client.get.return_value = [
            {"id": "rec-1", "name": "app.internal.example.com"}
        ]
        result = self.resource.list_records("zone-1")
        self.mock_client.get.assert_called_once_with("dns/zones/zone-1/records")
        assert len(result) == 1

    def test_create_record(self):
        self.mock_client.post.return_value = {"id": "rec-1", "name": "app.example.com"}
        record_data = DNSRecordCreate(
            name="app.example.com", type="A", content="10.0.0.1", ttl=300
        )
        result = self.resource.create_record("zone-1", record_data)
        self.mock_client.post.assert_called_once_with(
            "dns/zones/zone-1/records",
            data=record_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "rec-1"

    def test_get_record(self):
        self.mock_client.get.return_value = {"id": "rec-1"}
        result = self.resource.get_record("zone-1", "rec-1")
        self.mock_client.get.assert_called_once_with("dns/zones/zone-1/records/rec-1")
        assert result["id"] == "rec-1"

    def test_update_record(self):
        self.mock_client.put.return_value = {"id": "rec-1", "ttl": 600}
        update_data = DNSRecordUpdate(ttl=600)
        result = self.resource.update_record("zone-1", "rec-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "dns/zones/zone-1/records/rec-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["ttl"] == 600

    def test_delete_record(self):
        self.resource.delete_record("zone-1", "rec-1")
        self.mock_client.delete.assert_called_once_with(
            "dns/zones/zone-1/records/rec-1"
        )
