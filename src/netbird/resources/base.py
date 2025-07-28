"""
Base resource class for NetBird API resources.
"""

from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from ..client import APIClient


class BaseResource:
    """Base class for all API resource handlers.

    Provides common functionality for CRUD operations and API interaction.
    """

    def __init__(self, client: "APIClient") -> None:
        self.client = client

    def _parse_response(self, data: Any) -> Dict[str, Any]:
        """Parse API response data and return as dictionary (boto3 style)."""
        if not data:
            return {}
        if isinstance(data, dict):
            return data
        # For non-dict types, try to convert to dict or return empty dict
        try:
            return dict(data)
        except (TypeError, ValueError):
            return {}

    def _parse_list_response(self, data: Any) -> List[Dict[str, Any]]:
        """Parse API response data and return as list of dictionaries (boto3 style)."""
        if not isinstance(data, list):
            raise ValueError("Expected list response")
        return data
