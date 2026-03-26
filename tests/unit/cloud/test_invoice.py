"""
Unit tests for InvoiceResource.
"""

import pytest
from unittest.mock import MagicMock

from netbird.resources.cloud.invoice import InvoiceResource


@pytest.mark.unit
class TestInvoiceResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = InvoiceResource(self.mock_client)

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "inv-1", "amount": 9900, "status": "paid"},
            {"id": "inv-2", "amount": 19900, "status": "paid"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("integrations/billing/invoices")
        assert len(result) == 2
        assert result[0]["amount"] == 9900

    def test_get_pdf_url(self):
        self.mock_client.get.return_value = {
            "url": "https://billing.example.com/inv-1.pdf"
        }
        result = self.resource.get_pdf_url("inv-1")
        self.mock_client.get.assert_called_once_with(
            "integrations/billing/invoices/inv-1/pdf"
        )
        assert "url" in result

    def test_get_csv(self):
        self.mock_client.get.return_value = {"data": "id,amount\ninv-1,9900"}
        result = self.resource.get_csv("inv-1")
        self.mock_client.get.assert_called_once_with(
            "integrations/billing/invoices/inv-1/csv"
        )
        assert result is not None
