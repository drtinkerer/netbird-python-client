"""
Geo locations resource handler for NetBird API.
"""

from typing import Any, Dict, List

from .base import BaseResource


class GeoLocationsResource(BaseResource):
    """Handler for NetBird geo locations API endpoints."""

    def list_countries(self) -> List[str]:
        """List all country codes (ISO 3166-1 alpha-2).

        The official API returns a bare list of 2-letter code strings, but
        some NetBird deployments return country objects
        (``{"country_code": ..., "country_name": ...}``). Both shapes are
        normalised to a list of code strings.

        Returns:
            List of 2-letter country code strings
        """
        data = self.client.get("locations/countries")
        if not isinstance(data, list):
            raise ValueError("Expected list response")
        countries: List[str] = []
        for country in data:
            if isinstance(country, dict):
                code = country.get("country_code")
                if code is not None:
                    countries.append(str(code))
            else:
                countries.append(str(country))
        return countries

    def list_cities(self, country_code: str) -> List[Dict[str, Any]]:
        """List cities for a given country code.

        Args:
            country_code: 2-letter ISO country code

        Returns:
            List of city dictionaries with geoname_id and city_name
        """
        data = self.client.get(f"locations/countries/{country_code}/cities")
        return self._parse_list_response(data)
