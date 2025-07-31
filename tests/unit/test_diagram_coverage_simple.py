"""
Simplified tests for diagram coverage that focus on achievable coverage improvements.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from netbird.client import APIClient


class TestDiagramCoverage:
    """Focus on diagram paths that can be tested without complex import mocking."""
    
    @pytest.fixture
    def test_client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_generate_diagram_empty_networks(self, test_client):
        """Test generate_diagram when no networks are returned."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = []  # Empty networks
            
            result = test_client.generate_diagram(format="mermaid")
            assert result is None  # Should return None for empty networks (lines 365-366)
    
    def test_generate_diagram_unsupported_format(self, test_client):
        """Test generate_diagram with unsupported format."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = [{'name': 'test', 'resources': [], 'routers': [], 'policies': []}]
            
            with pytest.raises(ValueError, match="Unsupported format"):
                test_client.generate_diagram(format="invalid_format")  # Line 375
    
    def test_mermaid_diagram_with_file_output(self, test_client):
        """Test _create_mermaid_diagram with file output to cover file writing code."""
        networks = [{
            'name': 'File Test',
            'resources': [],
            'routers': [],
            'policies': []
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': set(),
                'group_connections': {},
                'direct_connections': {},
                'group_name_to_nodes': {}
            }
            
            with tempfile.TemporaryDirectory() as temp_dir:
                output_file = os.path.join(temp_dir, "test_output")
                result = test_client._create_mermaid_diagram(networks, output_file)
                
                assert result is not None
                # This covers lines 508-520 (file writing code)
                assert os.path.exists(f"{output_file}.mmd")
                assert os.path.exists(f"{output_file}.md")
    
    def test_helper_methods_coverage(self, test_client):
        """Test diagram helper methods for coverage."""
        # Test _get_source_group_colors with various inputs
        colors = test_client._get_source_group_colors(['group1', 'group2', 'group3'])
        assert len(colors) == 3
        assert all(color.startswith('#') for color in colors.values())
        
        # Test with empty list (line 387-388)
        empty_colors = test_client._get_source_group_colors([])
        assert empty_colors == {}
        
        # Test _format_policy_label with short list (line 396)
        short_label = test_client._format_policy_label(['p1', 'p2'], "Test")
        assert "p1" in short_label and "p2" in short_label
        
        # Test _format_policy_label with long list (>2 items) (line 398)  
        long_label = test_client._format_policy_label(['p1', 'p2', 'p3', 'p4'], "Test")
        assert "4 policies" in long_label
        
        # Test _sanitize_id with various inputs (lines 402-404)
        assert test_client._sanitize_id("normal_id") == "normal_id"
        assert test_client._sanitize_id("with-dashes") == "with_dashes"
        assert test_client._sanitize_id("with.dots") == "with_dots"
        assert test_client._sanitize_id("with spaces") == "with_spaces"
        assert test_client._sanitize_id("special!@#") == "special___"
    
    def test_mermaid_diagram_with_string_groups(self, test_client):
        """Test mermaid generation with string groups."""
        networks = [{
            'name': 'String Group Test',
            'resources': [{
                'name': 'Resource1',
                'address': '10.0.0.1',
                'type': 'host',
                'groups': ['string-group-1', 'string-group-2']  # String groups (line 448)
            }],
            'routers': [],
            'policies': []
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': set(),
                'group_connections': {},
                'direct_connections': {},
                'group_name_to_nodes': {}
            }
            
            result = test_client._create_mermaid_diagram(networks)
            assert "string-group-1" in result
            assert "string-group-2" in result
    
    def test_mermaid_diagram_complex_groups(self, test_client):
        """Test mermaid generation with mixed group types."""
        networks = [{
            'name': 'Mixed Groups',
            'resources': [{
                'name': 'Resource1',
                'address': '10.0.0.1',
                'type': 'host',
                'groups': [
                    {'name': 'dict-group', 'id': 'dg1'},  # Dict with name (line 445)
                    {'id': 'dg2'},  # Dict without name (line 445) 
                    'string-group'  # String group (line 448)
                ]
            }],
            'routers': [],
            'policies': []
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': set(),
                'group_connections': {},
                'direct_connections': {},
                'group_name_to_nodes': {}
            }
            
            result = test_client._create_mermaid_diagram(networks)
            assert "dict-group" in result
            assert "dg2" in result  # Should use ID when no name
            assert "string-group" in result
    
    def test_generate_diagram_include_options(self, test_client):
        """Test generate_diagram with different include options."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = [{
                'name': 'test-network',
                'resources': [],
                'routers': [],
                'policies': []
            }]
            
            with patch.object(test_client, '_create_mermaid_diagram', return_value="test") as mock_mermaid:
                # Test various combinations to cover different parameter paths
                test_client.generate_diagram(
                    format="mermaid",
                    include_routers=False,
                    include_policies=True,
                    include_resources=True
                )
                mock_generate.assert_called_with(test_client, False, True, True)
                
                test_client.generate_diagram(
                    format="mermaid", 
                    include_routers=True,
                    include_policies=False,
                    include_resources=True
                )
                mock_generate.assert_called_with(test_client, True, False, True)
                
                test_client.generate_diagram(
                    format="mermaid",
                    include_routers=True,
                    include_policies=True,
                    include_resources=False
                )
                mock_generate.assert_called_with(test_client, True, True, False)


class TestSimpleImportErrors:
    """Test import error handling in a simple way."""
    
    @pytest.fixture
    def test_client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_graphviz_import_error_handling(self, test_client):
        """Test graphviz import error by mocking the try/except block."""
        networks = [{'name': 'test', 'resources': [], 'routers': [], 'policies': []}]
        
        # Mock the import to raise ImportError
        with patch('builtins.__import__') as mock_import:
            def side_effect(name, *args, **kwargs):
                if name == 'graphviz':
                    raise ImportError("No module named 'graphviz'")
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            # This should handle the import error and return None (lines 526-530)
            result = test_client._create_graphviz_diagram(networks)
            assert result is None
    
    def test_diagrams_import_error_handling(self, test_client):
        """Test diagrams import error by mocking the try/except block."""
        networks = [{'name': 'test', 'resources': [], 'routers': [], 'policies': []}]
        
        # Mock the import to raise ImportError
        with patch('builtins.__import__') as mock_import:
            def side_effect(name, *args, **kwargs):
                if name == 'diagrams':
                    raise ImportError("No module named 'diagrams'")
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            # This should handle the import error and return None (lines 662-664)
            result = test_client._create_diagrams_diagram(networks)
            assert result is None