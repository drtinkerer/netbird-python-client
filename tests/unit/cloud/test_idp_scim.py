"""
Unit tests for IDPScimResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.idp_scim import IDPScimResource
from netbird.models.cloud.idp_scim import SCIMIntegrationCreate, SCIMIntegrationUpdate


@pytest.mark.unit
class TestIDPScimResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = IDPScimResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "scim-1", "provider": "okta"},
            {"id": "scim-2", "provider": "azure-ad"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("integrations/scim-idp")
        assert len(result) == 2
        assert result[0]["provider"] == "okta"

    def test_create(self):
        create_data = SCIMIntegrationCreate(
            prefix="nb-okta",
            provider="okta",
            group_prefixes=["engineering-*"],
            user_group_prefixes=["user-*"],
        )
        self.mock_client.post.return_value = {"id": "scim-1", "provider": "okta"}
        result = self.resource.create(create_data)
        self.mock_client.post.assert_called_once_with(
            "integrations/scim-idp",
            data=create_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "scim-1"

    def test_get(self):
        self.mock_client.get.return_value = {
            "id": "scim-1",
            "provider": "okta",
            "enabled": True,
        }
        result = self.resource.get("scim-1")
        self.mock_client.get.assert_called_once_with("integrations/scim-idp/scim-1")
        assert result["provider"] == "okta"

    def test_update(self):
        update_data = SCIMIntegrationUpdate(enabled=False)
        self.mock_client.put.return_value = {"id": "scim-1", "enabled": False}
        result = self.resource.update("scim-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "integrations/scim-idp/scim-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["enabled"] is False

    def test_delete(self):
        self.resource.delete("scim-1")
        self.mock_client.delete.assert_called_once_with("integrations/scim-idp/scim-1")

    def test_regenerate_token(self):
        self.mock_client.post.return_value = {"token": "new-scim-token-xyz"}
        result = self.resource.regenerate_token("scim-1")
        self.mock_client.post.assert_called_once_with(
            "integrations/scim-idp/scim-1/token"
        )
        assert "token" in result

    def test_get_logs(self):
        self.mock_client.get.return_value = [
            {
                "timestamp": "2026-03-21T10:00:00Z",
                "action": "sync",
                "status": "success",
            },
            {"timestamp": "2026-03-21T09:00:00Z", "action": "sync", "status": "error"},
        ]
        result = self.resource.get_logs("scim-1")
        self.mock_client.get.assert_called_once_with(
            "integrations/scim-idp/scim-1/logs"
        )
        assert len(result) == 2
        assert result[0]["status"] == "success"
