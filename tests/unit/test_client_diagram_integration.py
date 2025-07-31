"""
Integration tests for client diagram generation methods.
"""

import os
import tempfile
from unittest.mock import Mock, patch, mock_open

import pytest

from netbird import APIClient


class TestClientDiagramIntegration:
    """Test diagram generation integration with APIClient."""

    def test_client_has_diagram_method(self, test_client):
        """Test that client has generate_diagram method."""
        assert hasattr(test_client, 'generate_diagram')
        assert callable(test_client.generate_diagram)

    def test_client_has_helper_methods(self, test_client):
        """Test that client has all diagram helper methods."""
        helper_methods = [
            '_get_source_group_colors',
            '_format_policy_label', 
            '_sanitize_id',
            '_create_mermaid_diagram',
            '_create_graphviz_diagram',
            '_create_diagrams_diagram'
        ]
        
        for method in helper_methods:
            assert hasattr(test_client, method)
            assert callable(getattr(test_client, method))

    def test_client_diagram_method_signature(self, test_client):
        """Test generate_diagram method signature and defaults."""
        import inspect
        
        sig = inspect.signature(test_client.generate_diagram)
        params = sig.parameters
        
        # Check parameter names
        expected_params = ['format', 'output_file', 'include_routers', 'include_policies', 'include_resources']
        for param in expected_params:
            assert param in params
        
        # Check default values
        assert params['format'].default == "mermaid"
        assert params['output_file'].default is None
        assert params['include_routers'].default is True
        assert params['include_policies'].default is True
        assert params['include_resources'].default is True

    def test_mermaid_diagram_end_to_end(self, test_client):
        """Test complete mermaid diagram generation flow."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'Test Network',
                'resources': [
                    {
                        'id': 'res-1',
                        'name': 'test-resource',
                        'address': '10.0.1.1',
                        'type': 'host',
                        'groups': [{'id': 'grp-1', 'name': 'test-group'}]
                    }
                ],
                'routers': [{'id': 'rtr-1', 'name': 'test-router', 'peer': 'peer-1'}],
                'policies': [
                    {
                        'id': 'pol-1',
                        'name': 'test-policy',
                        'rules': [
                            {
                                'sources': [{'id': 'grp-2', 'name': 'source-group'}],
                                'destinations': [{'id': 'grp-1', 'name': 'test-group'}],
                                'destinationResource': {}
                            }
                        ]
                    }
                ]
            }
        ]
        
        sample_topology = {
            'group_connections': {('source-group', 'test-group'): ['test-policy']},
            'direct_connections': {},
            'all_source_groups': {'source-group'},
            'resource_id_to_node': {'res-1': 'res_0_0'},
            'group_name_to_nodes': {'test-group': ['res_0_0']}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            result = test_client.generate_diagram(format="mermaid")
            
            assert result is not None
            assert isinstance(result, str)
            
            # Verify key components are present
            assert "graph LR" in result
            assert "Test Network" in result
            assert "test-resource" in result
            assert "test-router" in result
            assert "source-group" in result
            assert "test-policy" in result

    def test_mermaid_diagram_with_file_output_end_to_end(self, test_client):
        """Test mermaid diagram generation with file output."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'File Test Network',
                'resources': [
                    {
                        'id': 'res-1',
                        'name': 'file-test-resource',
                        'address': '10.0.1.1',
                        'type': 'host',
                        'groups': []
                    }
                ],
                'routers': [],
                'policies': []
            }
        ]
        
        sample_topology = {
            'group_connections': {},
            'direct_connections': {},
            'all_source_groups': set(),
            'resource_id_to_node': {},
            'group_name_to_nodes': {}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology, \
             patch('builtins.open', mock_open()) as mock_file:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            result = test_client.generate_diagram(format="mermaid", output_file="test_output")
            
            assert result is not None
            assert isinstance(result, str)
            assert "File Test Network" in result
            
            # Verify files were written
            mock_file.assert_any_call("test_output.mmd", 'w')
            mock_file.assert_any_call("test_output.md", 'w')

    def test_diagram_generation_with_all_options(self, test_client):
        """Test diagram generation with all include options."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'Options Test Network',
                'resources': [
                    {
                        'id': 'res-1',
                        'name': 'options-resource',
                        'address': '10.0.1.1',
                        'type': 'host',
                        'groups': []
                    }
                ],
                'routers': [{'id': 'rtr-1', 'name': 'options-router'}],
                'policies': []
            }
        ]
        
        sample_topology = {
            'group_connections': {},
            'direct_connections': {},
            'all_source_groups': set(),
            'resource_id_to_node': {},
            'group_name_to_nodes': {}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            # Test with specific options
            result = test_client.generate_diagram(
                format="mermaid",
                include_routers=True,
                include_policies=False,
                include_resources=True
            )
            
            assert result is not None
            mock_generate.assert_called_once_with(test_client, True, False, True)

    def test_color_generation_consistency(self, test_client):
        """Test that color generation is consistent and deterministic."""
        groups1 = ['alpha', 'beta', 'gamma']
        groups2 = ['gamma', 'alpha', 'beta']  # Different order
        
        colors1 = test_client._get_source_group_colors(groups1)
        colors2 = test_client._get_source_group_colors(groups2)
        
        # Should be the same because they're sorted internally
        assert colors1 == colors2
        
        # Should have all groups
        for group in groups1:
            assert group in colors1
            assert group in colors2
        
        # Colors should be valid hex colors
        for color in colors1.values():
            assert color.startswith('#')
            assert len(color) == 7

    def test_policy_label_formatting_comprehensive(self, test_client):
        """Test comprehensive policy label formatting scenarios."""
        test_cases = [
            # (policies, connection_type, check_function)
            ([], "Test", lambda r: r == "Test: "),
            (['single'], "Group", lambda r: r == "Group: single"),
            (['policy1', 'policy2'], "Direct", lambda r: r.startswith("Direct:") and "policy1" in r and "policy2" in r),
            (['p1', 'p2', 'p3'], "Group", lambda r: r == "Group: 3 policies"),
            (['p1', 'p2', 'p3', 'p4', 'p5'], "Direct", lambda r: r == "Direct: 5 policies"),
            (['dup', 'dup', 'unique'], "Test", lambda r: r.startswith("Test:") and "dup" in r and "unique" in r),
        ]
        
        for policies, conn_type, check_func in test_cases:
            result = test_client._format_policy_label(policies, conn_type)
            assert check_func(result), f"Failed for {policies}, got: {result}"

    def test_id_sanitization_comprehensive(self, test_client):
        """Test comprehensive ID sanitization scenarios."""
        test_cases = [
            ("simple", "simple"),
            ("with-dashes", "with_dashes"),
            ("with.dots", "with_dots"),
            ("with/slashes", "with_slashes"),
            ("with spaces", "with_spaces"),
            ("complex-test.group/name with spaces", "complex_test_group_name_with_spaces"),
            ("UPPER-case.Test", "UPPER_case_Test"),
            ("123-numeric.start", "123_numeric_start"),
            ("special!@#$%chars", "special_____chars"),
            ("", ""),  # Empty string
        ]
        
        for input_id, expected in test_cases:
            result = test_client._sanitize_id(input_id)
            assert result == expected

    def test_diagram_error_handling(self, test_client):
        """Test error handling in diagram generation."""
        # Mock the generate_full_network_map to avoid authentication issues
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = [{'name': 'test', 'resources': [], 'policies': [], 'routers': []}]
            
            # Test with invalid format
            with pytest.raises(ValueError, match="Unsupported format"):
                test_client.generate_diagram(format="invalid_format")
        
        # Test with network generation failure
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.side_effect = Exception("Network generation failed")
            
            with pytest.raises(Exception, match="Network generation failed"):
                test_client.generate_diagram(format="mermaid")

    def test_mermaid_styling_generation(self, test_client):
        """Test that mermaid diagram includes proper styling."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'Styled Network',
                'resources': [
                    {
                        'id': 'res-1',
                        'name': 'styled-resource',
                        'address': '10.0.1.1',
                        'type': 'host',
                        'groups': [{'id': 'grp-1', 'name': 'styled-group'}]
                    }
                ],
                'routers': [],
                'policies': []
            }
        ]
        
        sample_topology = {
            'group_connections': {},
            'direct_connections': {},
            'all_source_groups': {'source-group'},
            'resource_id_to_node': {'res-1': 'res_0_0'},
            'group_name_to_nodes': {'styled-group': ['res_0_0']}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            result = test_client.generate_diagram(format="mermaid")
            
            # Check for styling section
            assert "%% Styling" in result
            assert "classDef" in result
            assert "class " in result
            assert "fill:" in result
            assert "stroke:" in result

    def test_resource_type_icons(self, test_client):
        """Test that different resource types get appropriate icons."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'Icon Test Network',
                'resources': [
                    {
                        'id': 'res-1',
                        'name': 'host-resource',
                        'address': '10.0.1.1',
                        'type': 'host',
                        'groups': []
                    },
                    {
                        'id': 'res-2',
                        'name': 'subnet-resource',
                        'address': '10.0.1.0/24',
                        'type': 'subnet',
                        'groups': []
                    },
                    {
                        'id': 'res-3',
                        'name': 'unknown-resource',
                        'address': '10.0.1.2',
                        'type': 'unknown',
                        'groups': []
                    }
                ],
                'routers': [],
                'policies': []
            }
        ]
        
        sample_topology = {
            'group_connections': {},
            'direct_connections': {},
            'all_source_groups': set(),
            'resource_id_to_node': {},
            'group_name_to_nodes': {}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            result = test_client.generate_diagram(format="mermaid")
            
            # Check for appropriate icons
            assert "🖥️ host-resource" in result  # Host icon
            assert "🌐 subnet-resource" in result  # Subnet icon  
            assert "📁 unknown-resource" in result  # Default icon

    def test_router_representation(self, test_client):
        """Test that routers are properly represented in diagrams."""
        sample_networks = [
            {
                'id': 'net-1',
                'name': 'Router Test Network',
                'resources': [],
                'routers': [
                    {
                        'id': 'rtr-1',
                        'name': 'main-router',
                        'peer': 'peer-123'
                    },
                    {
                        'id': 'rtr-2',
                        'name': 'backup-router',
                        'peer': 'peer-456'
                    }
                ],
                'policies': []
            }
        ]
        
        sample_topology = {
            'group_connections': {},
            'direct_connections': {},
            'all_source_groups': set(),
            'resource_id_to_node': {},
            'group_name_to_nodes': {}
        }
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate, \
             patch('netbird.network_map.get_network_topology_data') as mock_topology:
            
            mock_generate.return_value = sample_networks
            mock_topology.return_value = sample_topology
            
            result = test_client.generate_diagram(format="mermaid")
            
            # Check for router representation
            assert "🔀 main-router" in result
            assert "🔀 backup-router" in result
            assert "router_0_0" in result
            assert "router_0_1" in result