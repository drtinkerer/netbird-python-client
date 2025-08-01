"""
Tests for network mapping functionality.
"""

from unittest.mock import Mock, patch

import pytest

from netbird.network_map import generate_full_network_map, get_network_topology_data
from tests.fixtures import load_sample_data


@pytest.fixture
def mock_api_responses():
    """Mock API responses for network mapping tests."""
    return {
        "networks": [
            {
                "id": "net-1",
                "name": "Network 1",
                "resources": ["res-1"],
                "routers": ["rtr-1"],
                "policies": ["pol-1"],
            },
            {
                "id": "net-2",
                "name": "Network 2",
                "resources": ["res-2"],
                "routers": [],
                "policies": [],
            },
        ],
        "resources": {
            "net-1": [
                {
                    "id": "res-1",
                    "name": "Resource 1",
                    "address": "10.0.1.1",
                    "type": "host",
                    "groups": [{"id": "grp-1", "name": "group1"}],
                }
            ],
            "net-2": [
                {
                    "id": "res-2",
                    "name": "Resource 2",
                    "address": "10.0.2.1",
                    "type": "host",
                    "groups": [{"id": "grp-2", "name": "group2"}],
                }
            ],
        },
        "routers": {
            "net-1": [{"id": "rtr-1", "name": "Router 1", "peer": "peer-1"}],
            "net-2": [],
        },
        "policies": [
            {
                "id": "pol-1",
                "name": "Policy 1",
                "rules": [
                    {
                        "sources": [{"id": "grp-3", "name": "developers"}],
                        "destinations": [{"id": "grp-1", "name": "group1"}],
                        "destinationResource": {},
                    }
                ],
            }
        ],
    }


class TestGenerateFullNetworkMap:
    """Test cases for generate_full_network_map function."""

    def test_generate_full_network_map_success(self, mock_api_responses):
        """Test successful network map generation."""

        # Create a proper mock client
        mock_client = Mock()
        mock_client.networks.list.return_value = mock_api_responses["networks"]
        mock_client.networks.list_resources.side_effect = (
            lambda net_id: mock_api_responses["resources"].get(net_id, [])
        )
        mock_client.networks.list_routers.side_effect = (
            lambda net_id: mock_api_responses["routers"].get(net_id, [])
        )
        mock_client.policies.list.return_value = mock_api_responses["policies"]
        mock_client.policies.get.side_effect = lambda pol_id: next(
            (p for p in mock_api_responses["policies"] if p["id"] == pol_id), None
        )

        result = generate_full_network_map(mock_client)

        assert len(result) == 2
        assert result[0]["name"] == "Network 1"
        assert result[1]["name"] == "Network 2"
        assert "resources" in result[0]
        assert "routers" in result[0]
        assert "policies" in result[0]

    def test_generate_full_network_map_with_options(
        self, mock_client, mock_api_responses
    ):
        """Test network map generation with specific options."""
        mock_client.networks.list.return_value = mock_api_responses["networks"]
        mock_client.networks.list_resources.side_effect = (
            lambda net_id: mock_api_responses["resources"].get(net_id, [])
        )
        mock_client.networks.list_routers.side_effect = (
            lambda net_id: mock_api_responses["routers"].get(net_id, [])
        )
        mock_client.policies.list.return_value = mock_api_responses["policies"]
        mock_client.policies.get.side_effect = lambda pol_id: next(
            (p for p in mock_api_responses["policies"] if p["id"] == pol_id), None
        )

        # Test with routers disabled
        result = generate_full_network_map(mock_client, include_routers=False)

        for network in result:
            assert network.get("routers") == []

        # Test with policies disabled
        result = generate_full_network_map(mock_client, include_policies=False)

        for network in result:
            assert network.get("policies") == []

    def test_generate_full_network_map_no_networks(self, mock_client):
        """Test network map generation when no networks exist."""
        mock_client.networks.list.return_value = []

        result = generate_full_network_map(mock_client)

        assert result == []

    def test_generate_full_network_map_api_error(self, mock_client):
        """Test network map generation when API call fails."""
        from netbird.exceptions import NetBirdAPIError

        mock_client.networks.list.side_effect = NetBirdAPIError("API Error", 500)

        with pytest.raises(NetBirdAPIError):
            generate_full_network_map(mock_client)

    def test_generate_full_network_map_empty_resources(self):
        """Test network map generation with networks that have no resources."""

        mock_client = Mock()
        mock_client.networks.list.return_value = [
            {
                "id": "net-1",
                "name": "Empty Network",
                "resources": [],
                "routers": [],
                "policies": [],
            }
        ]
        mock_client.networks.list_resources.return_value = []
        mock_client.networks.list_routers.return_value = []
        mock_client.policies.list.return_value = []
        mock_client.policies.get.return_value = None

        result = generate_full_network_map(mock_client)

        assert len(result) == 1
        assert result[0]["resources"] == []
        assert result[0]["routers"] == []
        assert result[0]["policies"] == []


class TestGetNetworkTopologyData:
    """Test cases for get_network_topology_data function."""

    def test_get_topology_data_basic(self, mock_client):
        """Test basic topology data extraction."""
        networks = load_sample_data("network_map")

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = networks

            result = get_network_topology_data(mock_client)

            assert "group_connections" in result
            assert "direct_connections" in result
            assert "all_source_groups" in result
            assert "resource_id_to_node" in result
            assert "group_name_to_nodes" in result

    def test_get_topology_data_optimized(self, mock_client):
        """Test topology data with connection optimization."""
        networks = load_sample_data("network_map")

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = networks

            result = get_network_topology_data(mock_client, optimize_connections=True)

            # Should have optimized connection data
            assert isinstance(result["group_connections"], dict)
            assert isinstance(result["direct_connections"], dict)
            assert isinstance(result["all_source_groups"], set)

    def test_get_topology_data_no_networks(self, mock_client):
        """Test topology data extraction with no networks."""
        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = []

            result = get_network_topology_data(mock_client)

            assert result["group_connections"] == {}
            assert result["direct_connections"] == {}
            assert result["all_source_groups"] == set()
            assert result["resource_id_to_node"] == {}
            assert result["group_name_to_nodes"] == {}

    def test_get_topology_data_complex_policies(self, mock_client):
        """Test topology data extraction with complex policy rules."""
        complex_networks = [
            {
                "id": "net-1",
                "name": "Complex Network",
                "resources": [
                    {
                        "id": "res-1",
                        "name": "Resource 1",
                        "address": "10.0.1.1",
                        "type": "host",
                        "groups": [
                            {"id": "grp-1", "name": "web-servers"},
                            {"id": "grp-2", "name": "production"},
                        ],
                    }
                ],
                "routers": [],
                "policies": [
                    {
                        "id": "pol-1",
                        "name": "Multi-rule Policy",
                        "rules": [
                            {
                                "sources": [{"id": "grp-3", "name": "developers"}],
                                "destinations": [
                                    {"id": "grp-1", "name": "web-servers"}
                                ],
                                "destinationResource": {},
                            },
                            {
                                "sources": [{"id": "grp-3", "name": "developers"}],
                                "destinations": [],
                                "destinationResource": {"id": "res-1"},
                            },
                        ],
                    }
                ],
            }
        ]

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = complex_networks

            result = get_network_topology_data(mock_client, optimize_connections=True)

            # Should have both group and direct connections
            assert len(result["group_connections"]) > 0
            assert len(result["direct_connections"]) > 0
            assert "developers" in result["all_source_groups"]

    def test_get_topology_data_include_options(self):
        """Test topology data with include options."""

        mock_client = Mock()
        networks = load_sample_data("network_map")

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = networks

            # Test with optimization enabled
            get_network_topology_data(mock_client, optimize_connections=True)

            mock_generate.assert_called_once_with(mock_client)

    def test_get_topology_data_malformed_policies(self, mock_client):
        """Test topology data extraction with malformed policy data."""
        malformed_networks = [
            {
                "id": "net-1",
                "name": "Network with Bad Policies",
                "resources": [
                    {
                        "id": "res-1",
                        "name": "Resource 1",
                        "address": "10.0.1.1",
                        "type": "host",
                        "groups": [{"id": "grp-1", "name": "group1"}],
                    }
                ],
                "routers": [],
                "policies": [
                    {
                        "id": "pol-1",
                        "name": "Bad Policy",
                        "rules": [
                            {
                                # Missing sources
                                "destinations": [{"id": "grp-1", "name": "group1"}],
                                "destinationResource": {},
                            },
                            {
                                "sources": [{"id": "grp-2", "name": "group2"}],
                                # Missing destinations and destinationResource
                            },
                        ],
                    },
                    # Non-dict policy
                    "invalid-policy",
                ],
            }
        ]

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = malformed_networks

            # Should not raise an exception, but handle gracefully
            result = get_network_topology_data(mock_client, optimize_connections=True)

            assert isinstance(result, dict)
            assert "group_connections" in result
            assert "direct_connections" in result

    def test_get_topology_data_string_groups(self, mock_client):
        """Test topology data extraction with string-based group references."""
        string_group_networks = [
            {
                "id": "net-1",
                "name": "Network with String Groups",
                "resources": [
                    {
                        "id": "res-1",
                        "name": "Resource 1",
                        "address": "10.0.1.1",
                        "type": "host",
                        "groups": ["string-group-1", "string-group-2"],
                    }
                ],
                "routers": [],
                "policies": [
                    {
                        "id": "pol-1",
                        "name": "String Policy",
                        "rules": [
                            {
                                "sources": ["source-group"],
                                "destinations": ["string-group-1"],
                                "destinationResource": {},
                            }
                        ],
                    }
                ],
            }
        ]

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = string_group_networks

            result = get_network_topology_data(mock_client, optimize_connections=True)

            # Should handle string groups correctly
            assert "source-group" in result["all_source_groups"]
            assert "string-group-1" in result["group_name_to_nodes"]


class TestNetworkMapEdgeCases:
    """Test edge cases and error conditions for network mapping."""

    def test_network_map_with_none_values(self, mock_client):
        """Test network map generation with None values in data."""
        networks_with_nones = [
            {
                "id": "net-1",
                "name": "Network with Nones",
                "resources": [
                    {
                        "id": None,
                        "name": None,
                        "address": "10.0.1.1",
                        "type": "host",
                        "groups": None,
                    }
                ],
                "routers": None,
                "policies": [
                    {
                        "id": "pol-1",
                        "name": "Policy with Nones",
                        "rules": [
                            {
                                "sources": None,
                                "destinations": None,
                                "destinationResource": None,
                            }
                        ],
                    }
                ],
            }
        ]

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = networks_with_nones

            # Should handle None values gracefully
            result = get_network_topology_data(mock_client, optimize_connections=True)

            assert isinstance(result, dict)

    def test_network_map_missing_fields(self, mock_client):
        """Test network map with missing required fields."""
        incomplete_networks = [
            {
                "id": "net-1",
                "name": "Incomplete Network",
                # Missing resources, routers, policies
            }
        ]

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = incomplete_networks

            result = get_network_topology_data(mock_client, optimize_connections=True)

            # Should use empty defaults for missing fields
            assert result["group_connections"] == {}
            assert result["direct_connections"] == {}
            assert result["all_source_groups"] == set()

    def test_large_network_performance(self, mock_client):
        """Test performance with large network data."""
        # Create a large network with many resources and policies
        large_networks = []
        for net_idx in range(10):
            resources = []
            policies = []

            # Create many resources
            for res_idx in range(100):
                resources.append(
                    {
                        "id": f"res-{net_idx}-{res_idx}",
                        "name": f"Resource {res_idx}",
                        "address": f"10.{net_idx}.{res_idx}.1",
                        "type": "host",
                        "groups": [
                            {"id": f"grp-{res_idx % 5}", "name": f"group-{res_idx % 5}"}
                        ],
                    }
                )

            # Create many policies
            for pol_idx in range(50):
                policies.append(
                    {
                        "id": f"pol-{net_idx}-{pol_idx}",
                        "name": f"Policy {pol_idx}",
                        "rules": [
                            {
                                "sources": [
                                    {
                                        "id": f"grp-src-{pol_idx % 3}",
                                        "name": f"source-{pol_idx % 3}",
                                    }
                                ],
                                "destinations": [
                                    {
                                        "id": f"grp-{pol_idx % 5}",
                                        "name": f"group-{pol_idx % 5}",
                                    }
                                ],
                                "destinationResource": {},
                            }
                        ],
                    }
                )

            large_networks.append(
                {
                    "id": f"net-{net_idx}",
                    "name": f"Large Network {net_idx}",
                    "resources": resources,
                    "routers": [],
                    "policies": policies,
                }
            )

        with patch("netbird.network_map.generate_full_network_map") as mock_generate:
            mock_generate.return_value = large_networks

            # Should handle large datasets without errors
            result = get_network_topology_data(mock_client, optimize_connections=True)

            assert isinstance(result, dict)
            assert len(result["all_source_groups"]) > 0
            assert len(result["group_connections"]) > 0
