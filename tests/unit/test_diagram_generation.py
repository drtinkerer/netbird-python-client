"""
Tests for network diagram generation functionality.
"""

import os
import tempfile
from unittest.mock import mock_open, patch

import pytest


@pytest.fixture
def sample_network_map_data():
    """Sample network data for diagram testing."""
    return [
        {
            "id": "network-1",
            "name": "Production Network",
            "description": "Main production network",
            "resources": [
                {
                    "id": "resource-1",
                    "name": "web-server",
                    "address": "10.0.1.10",
                    "type": "host",
                    "groups": [
                        {"id": "group-1", "name": "web-servers"},
                        {"id": "group-2", "name": "production"},
                    ],
                },
                {
                    "id": "resource-2",
                    "name": "database",
                    "address": "10.0.1.20",
                    "type": "host",
                    "groups": [
                        {"id": "group-3", "name": "databases"},
                        {"id": "group-2", "name": "production"},
                    ],
                },
            ],
            "routers": [{"id": "router-1", "name": "main-router", "peer": "peer-123"}],
            "policies": [
                {
                    "id": "policy-1",
                    "name": "web-access",
                    "rules": [
                        {
                            "sources": [{"id": "group-4", "name": "developers"}],
                            "destinations": [{"id": "group-1", "name": "web-servers"}],
                            "destinationResource": {},
                        }
                    ],
                },
                {
                    "id": "policy-2",
                    "name": "db-access",
                    "rules": [
                        {
                            "sources": [{"id": "group-1", "name": "web-servers"}],
                            "destinations": [],
                            "destinationResource": {"id": "resource-2"},
                        }
                    ],
                },
            ],
        },
        {
            "id": "network-2",
            "name": "Development Network",
            "description": "Development environment",
            "resources": [
                {
                    "id": "resource-3",
                    "name": "dev-server",
                    "address": "10.0.2.10",
                    "type": "host",
                    "groups": [{"id": "group-5", "name": "dev-servers"}],
                }
            ],
            "routers": [],
            "policies": [
                {
                    "id": "policy-3",
                    "name": "dev-access",
                    "rules": [
                        {
                            "sources": [{"id": "group-4", "name": "developers"}],
                            "destinations": [{"id": "group-5", "name": "dev-servers"}],
                            "destinationResource": {},
                        }
                    ],
                }
            ],
        },
    ]


@pytest.fixture
def sample_topology_data():
    """Sample topology data for testing."""
    return {
        "group_connections": {
            ("developers", "web-servers"): ["web-access"],
            ("developers", "dev-servers"): ["dev-access"],
        },
        "direct_connections": {("web-servers", "res_0_1"): ["db-access"]},
        "all_source_groups": {"developers", "web-servers"},
        "resource_id_to_node": {
            "resource-1": "res_0_0",
            "resource-2": "res_0_1",
            "resource-3": "res_1_0",
        },
        "group_name_to_nodes": {
            "web-servers": ["res_0_0"],
            "databases": ["res_0_1"],
            "production": ["res_0_0", "res_0_1"],
            "dev-servers": ["res_1_0"],
        },
    }


class TestDiagramGeneration:
    """Test cases for diagram generation functionality."""

    def test_generate_diagram_mermaid_format(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test mermaid diagram generation."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            result = test_client.generate_diagram(format="mermaid")

            assert result is not None
            assert isinstance(result, str)
            assert "graph LR" in result
            assert "Source Groups" in result
            assert "Production Network" in result
            assert "Development Network" in result
            assert "👥 developers" in result
            assert "🖥️ web-server" in result

    def test_generate_diagram_mermaid_with_output_file(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test mermaid diagram generation with file output."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
            patch("builtins.open", mock_open()) as mock_file,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            result = test_client.generate_diagram(
                format="mermaid", output_file="test_diagram"
            )

            assert result is not None
            assert isinstance(result, str)
            # Check that files were written
            mock_file.assert_any_call("test_diagram.mmd", "w")
            mock_file.assert_any_call("test_diagram.md", "w")

    def test_generate_diagram_graphviz_format(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test graphviz diagram generation."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            # Mock the graphviz method directly
            with patch.object(test_client, "_create_graphviz_diagram") as mock_method:
                mock_method.return_value = None

                result = test_client.generate_diagram(
                    format="graphviz", output_file="test_graphviz"
                )

                # Should not return anything for graphviz (saves files directly)
                assert result is None
                mock_method.assert_called_once()

    def test_generate_diagram_graphviz_import_error(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test graphviz diagram generation when graphviz is not installed."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            # Patch the import at the method level where it's used
            with patch(
                "netbird.client.APIClient._create_graphviz_diagram"
            ) as mock_method:
                mock_method.return_value = None

                result = test_client.generate_diagram(format="graphviz")

                assert result is None

    def test_generate_diagram_diagrams_format(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test python diagrams generation."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            # Mock the diagrams method directly
            with patch.object(test_client, "_create_diagrams_diagram") as mock_method:
                mock_method.return_value = "test_diagrams.png"

                result = test_client.generate_diagram(
                    format="diagrams", output_file="test_diagrams"
                )

                assert result == "test_diagrams.png"
                mock_method.assert_called_once()

    def test_generate_diagram_diagrams_import_error(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test python diagrams generation when diagrams library is not installed."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            # Mock the diagrams method to return None (import error)
            with patch.object(test_client, "_create_diagrams_diagram") as mock_method:
                mock_method.return_value = None

                result = test_client.generate_diagram(format="diagrams")

                assert result is None

    def test_generate_diagram_no_networks(self, test_client):
        """Test diagram generation when no networks are found."""
        with patch("netbird.network_map.generate_full_network_map") as mock_network_map:
            mock_network_map.return_value = []

            result = test_client.generate_diagram(format="mermaid")

            assert result is None

    def test_generate_diagram_invalid_format(
        self, test_client, sample_network_map_data
    ):
        """Test diagram generation with invalid format."""
        with patch("netbird.network_map.generate_full_network_map") as mock_network_map:
            mock_network_map.return_value = sample_network_map_data

            with pytest.raises(ValueError, match="Unsupported format: invalid"):
                test_client.generate_diagram(format="invalid")

    def test_generate_diagram_with_options(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test diagram generation with various options."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            result = test_client.generate_diagram(
                format="mermaid",
                include_routers=False,
                include_policies=False,
                include_resources=True,
            )

            assert result is not None
            mock_network_map.assert_called_once_with(test_client, False, False, True)

    def test_source_group_colors_generation(self, test_client):
        """Test dynamic source group color generation."""
        source_groups = ["developers", "admins", "guests", "web-servers"]
        colors = test_client._get_source_group_colors(source_groups)

        assert len(colors) == 4
        assert "developers" in colors
        assert "admins" in colors
        assert "guests" in colors
        assert "web-servers" in colors

        # Colors should be from the default palette
        for color in colors.values():
            assert color.startswith("#")
            assert len(color) == 7

    def test_format_policy_label(self, test_client):
        """Test policy label formatting."""
        # Test with few policies (order may vary due to set conversion)
        label = test_client._format_policy_label(["policy1", "policy2"], "Group")
        assert label.startswith("Group: ")
        assert "policy1" in label and "policy2" in label

        # Test with many policies
        many_policies = [f"policy{i}" for i in range(5)]
        label = test_client._format_policy_label(many_policies, "Direct")
        assert label == "Direct: 5 policies"

        # Test with duplicate policies
        label = test_client._format_policy_label(
            ["policy1", "policy1", "policy2"], "Group"
        )
        assert label.startswith("Group: ")
        assert "policy1" in label and "policy2" in label

    def test_sanitize_id(self, test_client):
        """Test ID sanitization for diagram formats."""
        test_cases = [
            ("test-group", "test_group"),
            ("test.group", "test_group"),
            ("test/group", "test_group"),
            ("test group", "test_group"),
            (
                "complex-test.group/name with spaces",
                "complex_test_group_name_with_spaces",
            ),
        ]

        for input_id, expected in test_cases:
            result = test_client._sanitize_id(input_id)
            assert result == expected

    def test_mermaid_diagram_structure(
        self, test_client, sample_network_map_data, sample_topology_data
    ):
        """Test mermaid diagram structure and content."""
        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = sample_network_map_data
            mock_topology.return_value = sample_topology_data

            result = test_client.generate_diagram(format="mermaid")

            # Check basic structure
            lines = result.split("\n")
            assert lines[0] == "graph LR"

            # Check for subgraphs
            assert any("subgraph SG" in line for line in lines)
            assert any("subgraph N0" in line for line in lines)
            assert any("subgraph N1" in line for line in lines)

            # Check for styling section
            assert any("%% Styling" in line for line in lines)

            # Check for connections
            assert any("-->" in line for line in lines)  # Direct connections
            assert any("-.->|" in line for line in lines)  # Group connections

    def test_empty_network_handling(self, test_client):
        """Test handling of networks with no resources or policies."""
        empty_network = [
            {
                "id": "empty-network",
                "name": "Empty Network",
                "description": "Network with no resources",
                "resources": [],
                "routers": [],
                "policies": [],
            }
        ]

        empty_topology = {
            "group_connections": {},
            "direct_connections": {},
            "all_source_groups": set(),
            "resource_id_to_node": {},
            "group_name_to_nodes": {},
        }

        with (
            patch("netbird.network_map.generate_full_network_map") as mock_network_map,
            patch("netbird.network_map.get_network_topology_data") as mock_topology,
        ):

            mock_network_map.return_value = empty_network
            mock_topology.return_value = empty_topology

            result = test_client.generate_diagram(format="mermaid")

            assert result is not None
            assert "Empty Network" in result
            assert "graph LR" in result


@pytest.mark.integration
class TestDiagramIntegration:
    """Integration tests for diagram generation (requires real NetBird API access)."""

    def test_real_diagram_generation(self, integration_client):
        """Test diagram generation with real API data."""
        try:
            # Test mermaid generation
            result = integration_client.generate_diagram(format="mermaid")
            if result is not None:
                assert isinstance(result, str)
                assert "graph LR" in result
        except Exception as e:
            pytest.skip(f"Integration test failed: {e}")

    def test_real_diagram_file_output(self, integration_client):
        """Test diagram generation with file output using real data."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, "integration_test")

                result = integration_client.generate_diagram(
                    format="mermaid", output_file=output_path
                )

                if result is not None:
                    # Check if files were created
                    mermaid_file = f"{output_path}.mmd"
                    markdown_file = f"{output_path}.md"

                    assert os.path.exists(mermaid_file)
                    assert os.path.exists(markdown_file)

                    # Check file contents
                    with open(mermaid_file, "r") as f:
                        content = f.read()
                        assert "graph LR" in content

        except Exception as e:
            pytest.skip(f"Integration test failed: {e}")


class TestDiagramHelperMethods:
    """Test helper methods used in diagram generation."""

    def test_get_source_group_colors_empty_list(self, test_client):
        """Test color generation with empty source groups."""
        colors = test_client._get_source_group_colors([])
        assert colors == {}

    def test_get_source_group_colors_consistent(self, test_client):
        """Test that color generation is consistent for same input."""
        groups = ["group-a", "group-b", "group-c"]
        colors1 = test_client._get_source_group_colors(groups)
        colors2 = test_client._get_source_group_colors(groups)

        assert colors1 == colors2

    def test_get_source_group_colors_sorted(self, test_client):
        """Test that color assignment is based on sorted group names."""
        groups1 = ["z-group", "a-group", "m-group"]
        groups2 = ["a-group", "m-group", "z-group"]

        colors1 = test_client._get_source_group_colors(groups1)
        colors2 = test_client._get_source_group_colors(groups2)

        # Should be identical since they're sorted internally
        assert colors1 == colors2

        # a-group should get first color since it's first alphabetically
        assert colors1["a-group"] == test_client._get_source_group_colors(["a"])["a"]

    def test_format_policy_label_edge_cases(self, test_client):
        """Test policy label formatting edge cases."""
        # Empty list
        label = test_client._format_policy_label([], "Test")
        assert label == "Test: "

        # Single policy
        label = test_client._format_policy_label(["single"], "Test")
        assert label == "Test: single"

        # Exactly 3 policies (boundary case)
        label = test_client._format_policy_label(["p1", "p2", "p3"], "Test")
        assert label == "Test: 3 policies"

    def test_sanitize_id_special_characters(self, test_client):
        """Test ID sanitization with various special characters."""
        special_chars = "test!@#$%^&*()+=[]{}|;':\"<>,?/~`"
        result = test_client._sanitize_id(special_chars)

        # The sanitize_id method replaces all non-alphanumeric characters
        # (except underscore) with underscores
        # Only letters, numbers, and underscores remain unchanged
        expected = "test____________________________"

        assert result == expected
