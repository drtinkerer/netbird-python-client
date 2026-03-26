"""
Unit tests for MSPResource.
"""

from unittest.mock import MagicMock

import pytest

from netbird.models.cloud.msp import MSPTenantCreate, MSPTenantUpdate
from netbird.resources.cloud.msp import MSPResource


@pytest.mark.unit
class TestMSPResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = MSPResource(self.mock_client)

    def test_list_tenants(self):
        self.mock_client.get.return_value = [
            {"id": "tenant-1", "name": "Acme Corp"},
            {"id": "tenant-2", "name": "Globex Inc"},
        ]
        result = self.resource.list_tenants()
        self.mock_client.get.assert_called_once_with("integrations/msp/tenants")
        assert len(result) == 2
        assert result[0]["name"] == "Acme Corp"

    def test_create_tenant(self):
        tenant_data = MSPTenantCreate(
            name="Acme Corp",
            domain="acme.com",
            groups=[{"name": "admins", "role": "admin"}],
        )
        self.mock_client.post.return_value = {"id": "tenant-1", "name": "Acme Corp"}
        result = self.resource.create_tenant(tenant_data)
        self.mock_client.post.assert_called_once_with(
            "integrations/msp/tenants",
            data=tenant_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "tenant-1"

    def test_get_tenant(self):
        self.mock_client.get.return_value = {"id": "tenant-1", "name": "Acme Corp"}
        result = self.resource.get_tenant("tenant-1")
        self.mock_client.get.assert_called_once_with(
            "integrations/msp/tenants/tenant-1"
        )
        assert result["name"] == "Acme Corp"

    def test_update_tenant(self):
        update_data = MSPTenantUpdate(name="Acme Corp Updated")
        self.mock_client.put.return_value = {
            "id": "tenant-1",
            "name": "Acme Corp Updated",
        }
        result = self.resource.update_tenant("tenant-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "integrations/msp/tenants/tenant-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["name"] == "Acme Corp Updated"

    def test_unlink_tenant(self):
        self.mock_client.post.return_value = {"id": "tenant-1", "status": "unlinked"}
        result = self.resource.unlink_tenant("tenant-1", "owner@example.com")
        self.mock_client.post.assert_called_once_with(
            "integrations/msp/tenants/tenant-1/unlink",
            data={"owner": "owner@example.com"},
        )
        assert result["status"] == "unlinked"

    def test_verify_domain(self):
        self.mock_client.post.return_value = {"verified": True}
        result = self.resource.verify_domain("tenant-1")
        self.mock_client.post.assert_called_once_with(
            "integrations/msp/tenants/tenant-1/dns"
        )
        assert result["verified"] is True

    def test_create_subscription(self):
        self.mock_client.post.return_value = {"id": "sub-1", "price_id": "price-123"}
        result = self.resource.create_subscription("tenant-1", "price-123")
        self.mock_client.post.assert_called_once_with(
            "integrations/msp/tenants/tenant-1/subscription",
            data={"priceID": "price-123"},
        )
        assert result["id"] == "sub-1"

    def test_invite_tenant(self):
        self.mock_client.post.return_value = {"id": "tenant-1", "status": "invited"}
        result = self.resource.invite_tenant("tenant-1")
        self.mock_client.post.assert_called_once_with(
            "integrations/msp/tenants/tenant-1/invite"
        )
        assert result["status"] == "invited"

    def test_respond_to_invite(self):
        self.mock_client.put.return_value = {"id": "tenant-1", "status": "accepted"}
        result = self.resource.respond_to_invite("tenant-1", "accept")
        self.mock_client.put.assert_called_once_with(
            "integrations/msp/tenants/tenant-1/invite",
            data={"value": "accept"},
        )
        assert result["status"] == "accepted"
