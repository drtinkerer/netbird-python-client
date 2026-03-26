"""Tests for IdentityProvidersResource."""

from unittest.mock import MagicMock

import pytest

from netbird.models.identity_provider import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from netbird.resources.identity_providers import IdentityProvidersResource


@pytest.mark.unit
class TestIdentityProvidersResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = IdentityProvidersResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [{"id": "idp-1", "name": "Okta"}]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("identity-providers")
        assert len(result) == 1

    def test_create(self):
        self.mock_client.post.return_value = {"id": "idp-1", "name": "Okta"}
        provider_data = IdentityProviderCreate(
            type="oidc",
            name="Okta",
            issuer="https://okta.example.com",
            client_id="client-123",
            client_secret="secret-456",
        )
        result = self.resource.create(provider_data)
        self.mock_client.post.assert_called_once_with(
            "identity-providers",
            data=provider_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "idp-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "idp-1", "name": "Okta"}
        result = self.resource.get("idp-1")
        self.mock_client.get.assert_called_once_with("identity-providers/idp-1")
        assert result["name"] == "Okta"

    def test_update(self):
        self.mock_client.put.return_value = {"id": "idp-1", "name": "Updated Okta"}
        update_data = IdentityProviderUpdate(name="Updated Okta")
        result = self.resource.update("idp-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "identity-providers/idp-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["name"] == "Updated Okta"

    def test_delete(self):
        self.resource.delete("idp-1")
        self.mock_client.delete.assert_called_once_with("identity-providers/idp-1")
