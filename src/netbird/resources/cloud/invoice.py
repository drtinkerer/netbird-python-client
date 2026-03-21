"""
Invoice resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..base import BaseResource


class InvoiceResource(BaseResource):
    """Handler for NetBird billing invoice API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all paid invoices."""
        data = self.client.get("integrations/billing/invoices")
        return self._parse_list_response(data)

    def get_pdf_url(self, invoice_id: str) -> Dict[str, Any]:
        """Get PDF URL for an invoice."""
        data = self.client.get(f"integrations/billing/invoices/{invoice_id}/pdf")
        return self._parse_response(data)

    def get_csv(self, invoice_id: str) -> Dict[str, Any]:
        """Get CSV data for an invoice."""
        data = self.client.get(f"integrations/billing/invoices/{invoice_id}/csv")
        return self._parse_response(data)
