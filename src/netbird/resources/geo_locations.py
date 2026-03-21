"""
Geo locations resource handler for NetBird API.
"""

from typing import Any, Dict, List

from .base import BaseResource


class GeoLocationsResource(BaseResource):
    """Handler for NetBird geo locations API endpoints."""

    def list_countries(self) -> List[str]:
        """List all country codes (ISO 3166-1 alpha-2).

        Returns:
            List of 2-letter country code strings
        """
        data = self.client.get("locations/countries")
        return data

    def list_cities(self, country_code: str) -> List[Dict[str, Any]]:
        """List cities for a given country code.

        Args:
            country_code: 2-letter ISO country code

        Returns:
            List of city dictionaries with geoname_id and city_name
        """
        data = self.client.get(f"locations/countries/{country_code}/cities")
        return self._parse_list_response(data)
