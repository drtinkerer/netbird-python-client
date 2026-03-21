"""Tests for PostureChecksResource."""

import pytest
from unittest.mock import MagicMock

from netbird.resources.posture_checks import PostureChecksResource
from netbird.models.posture_check import PostureCheckCreate, PostureCheckUpdate


@pytest.mark.unit
class TestPostureChecksResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = PostureChecksResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "check-1", "name": "Version Check"}
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("posture-checks")
        assert len(result) == 1
        assert result[0]["id"] == "check-1"

    def test_create(self):
        self.mock_client.post.return_value = {
            "id": "check-1",
            "name": "Version Check",
        }
        check_data = PostureCheckCreate(
            name="Version Check",
            description="Minimum version requirement",
            checks={"nb_version_check": {"min_version": "0.25.0"}},
        )
        result = self.resource.create(check_data)
        self.mock_client.post.assert_called_once_with(
            "posture-checks",
            data=check_data.model_dump(exclude_unset=True),
        )
        assert result["id"] == "check-1"

    def test_get(self):
        self.mock_client.get.return_value = {"id": "check-1", "name": "Version Check"}
        result = self.resource.get("check-1")
        self.mock_client.get.assert_called_once_with("posture-checks/check-1")
        assert result["id"] == "check-1"

    def test_update(self):
        self.mock_client.put.return_value = {"id": "check-1", "name": "Updated"}
        update_data = PostureCheckUpdate(name="Updated")
        result = self.resource.update("check-1", update_data)
        self.mock_client.put.assert_called_once_with(
            "posture-checks/check-1",
            data=update_data.model_dump(exclude_unset=True),
        )
        assert result["name"] == "Updated"

    def test_delete(self):
        self.resource.delete("check-1")
        self.mock_client.delete.assert_called_once_with("posture-checks/check-1")
