"""
Unit tests for UsageResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.usage import UsageResource


@pytest.mark.unit
class TestUsageResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = UsageResource(self.mock_client)

    def test_get(self):
        self.mock_client.get.return_value = {
            "peers": 15,
            "users": 5,
            "plan": "business",
            "billing_period_start": "2026-03-01T00:00:00Z",
            "billing_period_end": "2026-03-31T23:59:59Z",
        }
        result = self.resource.get()
        self.mock_client.get.assert_called_once_with("integrations/billing/usage")
        assert result["peers"] == 15
        assert result["plan"] == "business"
