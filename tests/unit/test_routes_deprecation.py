"""Tests for RoutesResource deprecation warnings."""

import warnings

import pytest
from unittest.mock import MagicMock

from netbird.resources.routes import RoutesResource
from netbird.models.route import RouteCreate, RouteUpdate


@pytest.mark.unit
class TestRoutesDeprecation:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = RoutesResource(self.mock_client)

    def test_list_emits_deprecation_warning(self):
        self.mock_client.get.return_value = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.resource.list()
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()

    def test_create_emits_deprecation_warning(self):
        self.mock_client.post.return_value = {"id": "route-1"}
        route_data = RouteCreate(
            description="test",
            network_id="net-1",
            network_type="ipv4",
            metric=100,
            enabled=True,
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.resource.create(route_data)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)

    def test_get_emits_deprecation_warning(self):
        self.mock_client.get.return_value = {"id": "route-1"}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.resource.get("route-1")
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)

    def test_update_emits_deprecation_warning(self):
        self.mock_client.put.return_value = {"id": "route-1"}
        update_data = RouteUpdate(description="updated")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.resource.update("route-1", update_data)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)

    def test_delete_emits_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.resource.delete("route-1")
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
