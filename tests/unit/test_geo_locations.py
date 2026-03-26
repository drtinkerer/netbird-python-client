"""Tests for GeoLocationsResource."""

import pytest
from unittest.mock import MagicMock

from netbird.resources.geo_locations import GeoLocationsResource


@pytest.mark.unit
class TestGeoLocationsResource:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = GeoLocationsResource(self.mock_client)

    def test_list_countries(self):
        self.mock_client.get.return_value = ["DE", "US", "GB"]
        result = self.resource.list_countries()
        self.mock_client.get.assert_called_once_with("locations/countries")
        assert len(result) == 3
        assert "DE" in result

    def test_list_cities(self):
        self.mock_client.get.return_value = [
            {"geoname_id": 2950159, "city_name": "Berlin"},
            {"geoname_id": 2867714, "city_name": "Munich"},
        ]
        result = self.resource.list_cities("DE")
        self.mock_client.get.assert_called_once_with("locations/countries/DE/cities")
        assert len(result) == 2
        assert result[0]["city_name"] == "Berlin"
