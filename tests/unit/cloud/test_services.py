"""
Unit tests for ServicesResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.services import ServicesResource
from netbird.models.cloud.service import (
    ServiceCreate,
    ServiceDomainCreate,
    ServiceUpdate,
)


@pytest.mark.unit
class TestServicesResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = ServicesResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "svc-1", "name": "web-app"},
            {"id": "svc-2", "name": "api-gateway"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("reverse-proxies/services")
        assert len(result) == 2
        assert result[0]["id"] == "svc-1"

    def test_create(self):
        service_data = ServiceCreate(
            name="web-app",
            domain="app.example.com",
            targets=[{"url": "http://10.0.0.1:8080"}],
            enabled=True,
            auth={"type": "none"},
        )
        self.mock_client.post.return_value = {"id": "svc-1", "name": "web-app"}
        result = self.resource.create(service_data)
        self.mock_client.post.assert_called_once_with(
            "reverse-proxies/services",
            data=service_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "svc-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "svc-1", "name": "web-app"}
        result = self.resource.get("svc-1")
        self.mock_client.get.assert_called_once_with("reverse-proxies/services/svc-1")
        assert result["name"] == "web-app"

    def test_update(self):
        update_data = ServiceUpdate(name="updated-app", enabled=False)
        self.mock_client.put.return_value = {
            "id": "svc-1",
            "name": "updated-app",
            "enabled": False,
        }
        result = self.resource.update("svc-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "reverse-proxies/services/svc-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["name"] == "updated-app"

    def test_delete(self):
        self.resource.delete("svc-1")
        self.mock_client.delete.assert_called_once_with(
            "reverse-proxies/services/svc-1"
        )

    def test_list_clusters(self):
        self.mock_client.get.return_value = [
            {"id": "cluster-1", "region": "us-east-1"},
        ]
        result = self.resource.list_clusters()
        self.mock_client.get.assert_called_once_with("reverse-proxies/clusters")
        assert len(result) == 1
        assert result[0]["region"] == "us-east-1"

    def test_list_domains(self):
        self.mock_client.get.return_value = [
            {"id": "domain-1", "domain": "app.example.com"},
        ]
        result = self.resource.list_domains()
        self.mock_client.get.assert_called_once_with("reverse-proxies/domains")
        assert len(result) == 1

    def test_create_domain(self):
        domain_data = ServiceDomainCreate(
            domain="custom.example.com",
            target_cluster="cluster-1",
        )
        self.mock_client.post.return_value = {
            "id": "domain-1",
            "domain": "custom.example.com",
        }
        result = self.resource.create_domain(domain_data)
        self.mock_client.post.assert_called_once_with(
            "reverse-proxies/domains",
            data=domain_data.model_dump(exclude_unset=True),
        )
        assert result["domain"] == "custom.example.com"

    def test_delete_domain(self):
        self.resource.delete_domain("domain-1")
        self.mock_client.delete.assert_called_once_with(
            "reverse-proxies/domains/domain-1"
        )

    def test_validate_domain(self):
        self.mock_client.get.return_value = {"valid": True, "status": "verified"}
        result = self.resource.validate_domain("domain-1")
        self.mock_client.get.assert_called_once_with(
            "reverse-proxies/domains/domain-1/validate"
        )
        assert result["valid"] is True
