"""
Unit tests for PeersResource.
"""

from unittest.mock import MagicMock

import pytest

from netbird.models import PeerUpdate
from netbird.resources.peers import PeersResource


@pytest.mark.unit
class TestPeersResource:
    """Test cases for PeersResource methods."""

    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = PeersResource(self.mock_client)

    # --- Existing CRUD ---

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "peer-1", "name": "server-01", "ip": "10.0.0.1"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("peers", params=None)
        assert len(result) == 1
        assert result[0]["name"] == "server-01"

    def test_list_with_name_filter(self):
        self.mock_client.get.return_value = [
            {"id": "peer-1", "name": "server-01"},
        ]
        result = self.resource.list(name="server-01")
        self.mock_client.get.assert_called_once_with(
            "peers", params={"name": "server-01"}
        )
        assert len(result) == 1

    def test_list_with_ip_filter(self):
        self.mock_client.get.return_value = [
            {"id": "peer-1", "ip": "10.0.0.1"},
        ]
        result = self.resource.list(ip="10.0.0.1")
        self.mock_client.get.assert_called_once_with("peers", params={"ip": "10.0.0.1"})
        assert len(result) == 1

    def test_get(self):
        self.mock_client.get.return_value = {
            "id": "peer-1",
            "name": "server-01",
            "ip": "10.0.0.1",
        }
        result = self.resource.get("peer-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1")
        assert result["ip"] == "10.0.0.1"

    def test_update(self):
        peer_data = PeerUpdate(name="updated-server", ssh_enabled=True)
        self.mock_client.put.return_value = {
            "id": "peer-1",
            "name": "updated-server",
            "ssh_enabled": True,
        }
        result = self.resource.update("peer-1", peer_data)
        self.mock_client.put.assert_called_once_with(
            "peers/peer-1", data=peer_data.model_dump(exclude_unset=True)
        )
        assert result["name"] == "updated-server"
        assert result["ssh_enabled"] is True

    def test_delete(self):
        self.resource.delete("peer-1")
        self.mock_client.delete.assert_called_once_with("peers/peer-1")

    def test_get_accessible_peers(self):
        self.mock_client.get.return_value = [
            {"id": "peer-2", "name": "server-02"},
            {"id": "peer-3", "name": "server-03"},
        ]
        result = self.resource.get_accessible_peers("peer-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1/accessible-peers")
        assert len(result) == 2

    # --- New: Temporary Access ---

    def test_create_temporary_access(self):
        access_data = {
            "name": "temp-peer",
            "wg_pub_key": "key123",
            "rules": [],
        }
        self.mock_client.post.return_value = {
            "id": "temp-1",
            "name": "temp-peer",
        }
        result = self.resource.create_temporary_access("peer-1", access_data)
        self.mock_client.post.assert_called_once_with(
            "peers/peer-1/temporary-access", data=access_data
        )
        assert result["id"] == "temp-1"

    # --- New: Jobs ---

    def test_list_jobs(self):
        self.mock_client.get.return_value = [
            {"id": "job-1", "status": "running"},
        ]
        result = self.resource.list_jobs("peer-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1/jobs")
        assert len(result) == 1
        assert result[0]["status"] == "running"

    def test_create_job(self):
        job_data = {"workload": "script.sh"}
        self.mock_client.post.return_value = {
            "id": "job-1",
            "status": "pending",
        }
        result = self.resource.create_job("peer-1", job_data)
        self.mock_client.post.assert_called_once_with(
            "peers/peer-1/jobs", data=job_data
        )
        assert result["status"] == "pending"

    def test_get_job(self):
        self.mock_client.get.return_value = {
            "id": "job-1",
            "status": "completed",
        }
        result = self.resource.get_job("peer-1", "job-1")
        self.mock_client.get.assert_called_once_with("peers/peer-1/jobs/job-1")
        assert result["status"] == "completed"
