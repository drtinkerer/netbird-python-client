"""Tests for InstanceResource."""

import pytest
from unittest.mock import MagicMock

from netbird.resources.instance import InstanceResource


@pytest.mark.unit
class TestInstanceResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = InstanceResource(self.mock_client)

    def test_get_status(self):
        self.mock_client.get.return_value = {"setup_required": False}
        result = self.resource.get_status()
        self.mock_client.get.assert_called_once_with("instance")
        assert result["setup_required"] is False

    def test_get_version(self):
        self.mock_client.get.return_value = {"version": "0.28.0"}
        result = self.resource.get_version()
        self.mock_client.get.assert_called_once_with("instance/version")
        assert result["version"] == "0.28.0"

    def test_setup(self):
        self.mock_client.post.return_value = {"status": "ok"}
        result = self.resource.setup(
            email="admin@example.com",
            password="SecurePass123!",
            name="Admin User",
        )
        self.mock_client.post.assert_called_once_with(
            "setup",
            data={
                "email": "admin@example.com",
                "password": "SecurePass123!",
                "name": "Admin User",
            },
        )
        assert result["status"] == "ok"
