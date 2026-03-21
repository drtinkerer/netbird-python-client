"""
Unit tests for all EDR resources.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.edr_peers import EDRPeersResource
from netbird.resources.cloud.edr_falcon import EDRFalconResource
from netbird.resources.cloud.edr_huntress import EDRHuntressResource
from netbird.resources.cloud.edr_intune import EDRIntuneResource
from netbird.resources.cloud.edr_sentinelone import EDRSentinelOneResource
from netbird.models.cloud.edr import (
    EDRFalconConfig,
    EDRHuntressConfig,
    EDRIntuneConfig,
    EDRSentinelOneConfig,
)


@pytest.mark.unit
class TestEDRPeersResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EDRPeersResource(self.mock_client)

    def test_bypass(self):
        self.mock_client.post.return_value = {"peer_id": "peer-1", "bypassed": True}
        result = self.resource.bypass("peer-1")
        self.mock_client.post.assert_called_once_with("peers/peer-1/edr/bypass")
        assert result["bypassed"] is True

    def test_revoke_bypass(self):
        self.resource.revoke_bypass("peer-1")
        self.mock_client.delete.assert_called_once_with("peers/peer-1/edr/bypass")

    def test_list_bypassed(self):
        self.mock_client.get.return_value = [
            {"peer_id": "peer-1", "bypassed": True},
            {"peer_id": "peer-2", "bypassed": True},
        ]
        result = self.resource.list_bypassed()
        self.mock_client.get.assert_called_once_with("peers/edr/bypassed")
        assert len(result) == 2


@pytest.mark.unit
class TestEDRFalconResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EDRFalconResource(self.mock_client)

    def _make_config(self):
        return EDRFalconConfig(
            client_id="falcon-client-id",
            secret="falcon-secret",
            cloud_id="us-1",
            groups=["group-1"],
            zta_score_threshold=50,
            enabled=True,
        )

    def test_create(self):
        config = self._make_config()
        self.mock_client.post.return_value = {"id": "falcon-1", "client_id": "falcon-client-id"}
        result = self.resource.create(config)
        self.mock_client.post.assert_called_once_with(
            "integrations/edr/falcon",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["id"] == "falcon-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "falcon-1", "cloud_id": "us-1"}
        result = self.resource.get()
        self.mock_client.get.assert_called_once_with("integrations/edr/falcon")
        assert result["cloud_id"] == "us-1"

    def test_update(self):
        config = self._make_config()
        self.mock_client.put.return_value = {"id": "falcon-1", "zta_score_threshold": 50}
        result = self.resource.update(config)
        self.mock_client.put.assert_called_once_with(
            "integrations/edr/falcon",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["zta_score_threshold"] == 50

    def test_delete(self):
        self.resource.delete()
        self.mock_client.delete.assert_called_once_with("integrations/edr/falcon")


@pytest.mark.unit
class TestEDRHuntressResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EDRHuntressResource(self.mock_client)

    def _make_config(self):
        return EDRHuntressConfig(
            api_key="huntress-key",
            api_secret="huntress-secret",
            groups=["group-1"],
            last_synced_interval=24,
            enabled=True,
        )

    def test_create(self):
        config = self._make_config()
        self.mock_client.post.return_value = {"id": "huntress-1", "api_key": "huntress-key"}
        result = self.resource.create(config)
        self.mock_client.post.assert_called_once_with(
            "integrations/edr/huntress",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["id"] == "huntress-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "huntress-1", "api_key": "huntress-key"}
        result = self.resource.get()
        self.mock_client.get.assert_called_once_with("integrations/edr/huntress")
        assert result is not None

    def test_update(self):
        config = self._make_config()
        self.mock_client.put.return_value = {"id": "huntress-1", "last_synced_interval": 24}
        result = self.resource.update(config)
        self.mock_client.put.assert_called_once_with(
            "integrations/edr/huntress",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["last_synced_interval"] == 24

    def test_delete(self):
        self.resource.delete()
        self.mock_client.delete.assert_called_once_with("integrations/edr/huntress")


@pytest.mark.unit
class TestEDRIntuneResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EDRIntuneResource(self.mock_client)

    def _make_config(self):
        return EDRIntuneConfig(
            client_id="azure-client-id",
            tenant_id="azure-tenant-id",
            secret="azure-secret",
            groups=["group-1"],
            last_synced_interval=24,
            enabled=True,
        )

    def test_create(self):
        config = self._make_config()
        self.mock_client.post.return_value = {"id": "intune-1", "client_id": "azure-client-id"}
        result = self.resource.create(config)
        self.mock_client.post.assert_called_once_with(
            "integrations/edr/intune",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["id"] == "intune-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "intune-1", "tenant_id": "azure-tenant-id"}
        result = self.resource.get()
        self.mock_client.get.assert_called_once_with("integrations/edr/intune")
        assert result["tenant_id"] == "azure-tenant-id"

    def test_update(self):
        config = self._make_config()
        self.mock_client.put.return_value = {"id": "intune-1", "enabled": True}
        result = self.resource.update(config)
        self.mock_client.put.assert_called_once_with(
            "integrations/edr/intune",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["enabled"] is True

    def test_delete(self):
        self.resource.delete()
        self.mock_client.delete.assert_called_once_with("integrations/edr/intune")


@pytest.mark.unit
class TestEDRSentinelOneResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = EDRSentinelOneResource(self.mock_client)

    def _make_config(self):
        return EDRSentinelOneConfig(
            api_token="s1-token",
            api_url="https://s1.example.com",
            groups=["group-1"],
            last_synced_interval=48,
            enabled=True,
        )

    def test_create(self):
        config = self._make_config()
        self.mock_client.post.return_value = {"id": "s1-1", "api_url": "https://s1.example.com"}
        result = self.resource.create(config)
        self.mock_client.post.assert_called_once_with(
            "integrations/edr/sentinelone",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["id"] == "s1-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "s1-1", "api_url": "https://s1.example.com"}
        result = self.resource.get()
        self.mock_client.get.assert_called_once_with("integrations/edr/sentinelone")
        assert result["api_url"] == "https://s1.example.com"

    def test_update(self):
        config = self._make_config()
        self.mock_client.put.return_value = {"id": "s1-1", "last_synced_interval": 48}
        result = self.resource.update(config)
        self.mock_client.put.assert_called_once_with(
            "integrations/edr/sentinelone",
            data=config.model_dump(exclude_unset=True),
        )
        assert result["last_synced_interval"] == 48

    def test_delete(self):
        self.resource.delete()
        self.mock_client.delete.assert_called_once_with("integrations/edr/sentinelone")
