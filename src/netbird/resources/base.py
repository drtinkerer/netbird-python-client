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
        if data is None:
            return []
        if not isinstance(data, list):
            raise ValueError("Expected list response")
        return data

    def _parse_paginated_list_response(self, data: Any) -> List[Dict[str, Any]]:
        """Return items from either a legacy list or a paginated response.

        NetBird's event endpoints historically returned a bare list and now
        return an object containing a ``data`` list plus pagination metadata.
        Resource methods retain their list-returning API while accepting both
        response shapes.
        """
        if isinstance(data, dict):
            data = data.get("data", [])
        return self._parse_list_response(data)
