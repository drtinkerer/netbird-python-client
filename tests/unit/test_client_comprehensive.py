"""
Comprehensive client.py coverage tests to improve coverage from 68% to 80%+.
Focuses on testing the diagram generation methods and other uncovered paths.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, mock_open
from netbird.client import APIClient
from netbird.exceptions import NetBirdAPIError


class TestClientDiagramMethods:
    """Test diagram generation methods to improve client coverage."""
    
    @pytest.fixture
    def client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_generate_diagram_with_all_formats(self, client):
        """Test generate_diagram method with all supported formats."""
        networks_data = [{
            'name': 'Test Network',
            'resources': [{'name': 'Resource1', 'address': '10.0.0.1'}],
            'routers': [{'name': 'Router1'}],
            'policies': [{'name': 'Policy1'}]
        }]
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = networks_data
            
            # Test mermaid format (should work without external dependencies)
            with patch.object(client, '_create_mermaid_diagram', return_value="mermaid content") as mock_mermaid:
                result = client.generate_diagram(format="mermaid")
                assert result == "mermaid content"
                mock_mermaid.assert_called_once_with(networks_data, None)
            
            # Test graphviz format
            with patch.object(client, '_create_graphviz_diagram', return_value=None) as mock_graphviz:
                result = client.generate_diagram(format="graphviz")
                assert result is None
                mock_graphviz.assert_called_once_with(networks_data, None)
            
            # Test diagrams format  
            with patch.object(client, '_create_diagrams_diagram', return_value="diagram.png") as mock_diagrams:
                result = client.generate_diagram(format="diagrams")
                assert result == "diagram.png"
                mock_diagrams.assert_called_once_with(networks_data, None)
    
    def test_graphviz_diagram_method_with_mocked_import(self, client):
        """Test _create_graphviz_diagram method with mocked graphviz import."""
        networks = [{
            'name': 'Graphviz Test',
            'resources': [{'name': 'Res1', 'address': '10.0.0.1', 'groups': [{'name': 'group1'}]}],
            'routers': [{'name': 'Router1'}],
            'policies': []
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': {'src1'},
                'group_connections': {('src1', 'group1'): ['policy1']},
                'direct_connections': {},
                'group_name_to_nodes': {'group1': ['res_0_0']}
            }
            
            # Mock graphviz module and its classes
            mock_graphviz = MagicMock()
            mock_dot = MagicMock()
            mock_subgraph = MagicMock()
            
            # Setup context managers
            mock_subgraph.__enter__ = MagicMock(return_value=mock_subgraph)
            mock_subgraph.__exit__ = MagicMock(return_value=None)
            mock_dot.subgraph.return_value = mock_subgraph
            mock_dot.source = "digraph test { }"  # Mock the source attribute
            mock_graphviz.Digraph.return_value = mock_dot
            
            # Mock file operations
            with patch('builtins.open', mock_open()) as mock_file:
                with patch.dict('sys.modules', {'graphviz': mock_graphviz}):
                    result = client._create_graphviz_diagram(networks)
                    
                    # Verify graphviz methods were called
                    mock_graphviz.Digraph.assert_called_once()
                    mock_dot.render.assert_called()
                    mock_file.assert_called()  # File operations should be called
                    assert result is None  # graphviz render returns None
    
    def test_graphviz_diagram_import_error(self, client):
        """Test _create_graphviz_diagram with ImportError."""
        networks = [{'name': 'test', 'resources': [], 'routers': [], 'policies': []}]
        
        # Mock the import to fail
        with patch('builtins.__import__', side_effect=ImportError("No graphviz")):
            result = client._create_graphviz_diagram(networks)
            assert result is None
    
    def test_python_diagrams_method_with_mocked_import(self, client):
        """Test _create_diagrams_diagram method with mocked imports."""
        networks = [{
            'name': 'Diagrams Test',
            'resources': [{'name': 'Web Server', 'address': '10.0.1.10', 'groups': [{'name': 'web-tier'}]}],
            'routers': [{'name': 'Main Router'}], 
            'policies': []
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': {'external'},
                'group_connections': {('external', 'web-tier'): ['web-policy']},
                'direct_connections': {},
                'group_name_to_nodes': {'web-tier': ['res_0_0']}
            }
            
            # Mock diagrams modules
            mock_diagrams = MagicMock()
            mock_cluster_module = MagicMock()
            mock_blank_module = MagicMock()
            mock_internet_module = MagicMock()
            mock_router_module = MagicMock()
            
            # Setup diagram context manager
            mock_diagram_instance = MagicMock()
            mock_diagram_instance.__enter__ = MagicMock(return_value=mock_diagram_instance)
            mock_diagram_instance.__exit__ = MagicMock(return_value=None)
            mock_diagrams.Diagram.return_value = mock_diagram_instance
            
            # Setup cluster context manager
            mock_cluster_instance = MagicMock()
            mock_cluster_instance.__enter__ = MagicMock(return_value=mock_cluster_instance)
            mock_cluster_instance.__exit__ = MagicMock(return_value=None)
            mock_diagrams.Cluster.return_value = mock_cluster_instance
            
            # Mock node creation
            mock_internet_module.Internet.return_value = MagicMock()
            mock_router_module.Router.return_value = MagicMock()
            mock_blank_module.Blank.return_value = MagicMock()
            
            modules = {
                'diagrams': mock_diagrams,
                'diagrams.Cluster': mock_cluster_module,
                'diagrams.generic.blank': mock_blank_module,
                'diagrams.onprem.network': mock_internet_module,
                'diagrams.generic.network': mock_router_module
            }
            
            with patch.dict('sys.modules', modules):
                result = client._create_diagrams_diagram(networks)
                
                # Should return a filename
                assert result is not None
                assert result.endswith('.png')
                
                # Verify diagram creation was called
                mock_diagrams.Diagram.assert_called_once()
    
    def test_python_diagrams_import_error(self, client):
        """Test _create_diagrams_diagram with ImportError."""
        networks = [{'name': 'test', 'resources': [], 'routers': [], 'policies': []}]
        
        # Mock the import to fail
        with patch('builtins.__import__', side_effect=ImportError("No diagrams")):
            result = client._create_diagrams_diagram(networks)
            assert result is None
    
    def test_mermaid_file_operations(self, client):
        """Test mermaid diagram file operations."""
        networks = [{
            'name': 'File Test Network',
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
                output_file = os.path.join(temp_dir, "test_mermaid")
                
                result = client._create_mermaid_diagram(networks, output_file)
                
                # Check files were created
                assert os.path.exists(f"{output_file}.mmd")
                assert os.path.exists(f"{output_file}.md")
                
                # Check content
                with open(f"{output_file}.mmd", 'r') as f:
                    mmd_content = f.read()
                assert "graph LR" in mmd_content
                assert result is not None
    
    def test_generate_diagram_with_output_file(self, client):
        """Test generate_diagram with output file parameter."""
        networks_data = [{'name': 'Test', 'resources': [], 'routers': [], 'policies': []}]
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = networks_data
            
            with patch.object(client, '_create_mermaid_diagram', return_value="content") as mock_mermaid:
                result = client.generate_diagram(format="mermaid", output_file="test_output")
                assert result == "content"
                mock_mermaid.assert_called_once_with(networks_data, "test_output")


class TestClientHelperMethods:
    """Test client helper methods for coverage."""
    
    @pytest.fixture
    def client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_get_source_group_colors_comprehensive(self, client):
        """Test _get_source_group_colors with various inputs."""
        # Test with no groups
        colors = client._get_source_group_colors([])
        assert colors == {}
        
        # Test with single group
        colors = client._get_source_group_colors(['group1'])
        assert len(colors) == 1
        assert 'group1' in colors
        assert colors['group1'].startswith('#')
        
        # Test with multiple groups
        groups = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
        colors = client._get_source_group_colors(groups)
        assert len(colors) == 5
        assert all(color.startswith('#') for color in colors.values())
        
        # Test color consistency (same input should give same colors)
        colors2 = client._get_source_group_colors(groups)
        assert colors == colors2
        
        # Test with many groups (more than predefined colors)
        many_groups = [f'group{i}' for i in range(20)]
        colors = client._get_source_group_colors(many_groups)
        assert len(colors) == 20
        assert all(color.startswith('#') for color in colors.values())
    
    def test_format_policy_label_edge_cases(self, client):
        """Test _format_policy_label with edge cases."""
        # Test with empty list
        label = client._format_policy_label([], "Test")
        assert "Test" in label
        
        # Test with single policy
        label = client._format_policy_label(['policy1'], "Single")
        assert "policy1" in label
        
        # Test with exactly 2 policies
        label = client._format_policy_label(['p1', 'p2'], "Two")
        assert "p1" in label and "p2" in label
        
        # Test with exactly 3 policies (should show count)
        label = client._format_policy_label(['p1', 'p2', 'p3'], "Three")
        assert "3 policies" in label
        
        # Test with many policies
        policies = [f'policy{i}' for i in range(10)]
        label = client._format_policy_label(policies, "Many")
        assert "10 policies" in label
    
    def test_sanitize_id_comprehensive(self, client):
        """Test _sanitize_id with comprehensive character sets."""
        # Test normal ID
        assert client._sanitize_id("normal_id") == "normal_id"
        
        # Test with hyphens
        assert client._sanitize_id("with-hyphens") == "with_hyphens"
        
        # Test with dots
        assert client._sanitize_id("with.dots.here") == "with_dots_here"
        
        # Test with spaces
        assert client._sanitize_id("with spaces") == "with_spaces"
        
        # Test with mixed special characters
        assert client._sanitize_id("test!@#$%^&*()") == "test__________"
        
        # Test with numbers (should be preserved)
        assert client._sanitize_id("test123") == "test123"
        
        # Test with underscores (should be preserved)
        assert client._sanitize_id("test_123_abc") == "test_123_abc"
        
        # Test empty string
        assert client._sanitize_id("") == ""
        
        # Test only special characters
        assert client._sanitize_id("!@#$") == "____"


class TestClientTypeCheckingImports:
    """Test TYPE_CHECKING imports indirectly."""
    
    def test_client_resource_attribute_access(self):
        """Test that all resource attributes are accessible."""
        client = APIClient(host="test.com", api_token="token")
        
        # Test that all resource attributes exist and are of correct type
        from netbird.resources.accounts import AccountsResource
        from netbird.resources.users import UsersResource
        from netbird.resources.tokens import TokensResource
        from netbird.resources.peers import PeersResource
        from netbird.resources.setup_keys import SetupKeysResource
        from netbird.resources.groups import GroupsResource
        from netbird.resources.networks import NetworksResource
        from netbird.resources.policies import PoliciesResource
        from netbird.resources.routes import RoutesResource
        from netbird.resources.dns import DNSResource
        from netbird.resources.events import EventsResource
        
        assert isinstance(client.accounts, AccountsResource)
        assert isinstance(client.users, UsersResource)
        assert isinstance(client.tokens, TokensResource)
        assert isinstance(client.peers, PeersResource)
        assert isinstance(client.setup_keys, SetupKeysResource)
        assert isinstance(client.groups, GroupsResource)
        assert isinstance(client.networks, NetworksResource)
        assert isinstance(client.policies, PoliciesResource)
        assert isinstance(client.routes, RoutesResource)
        assert isinstance(client.dns, DNSResource)
        assert isinstance(client.events, EventsResource)
    
    def test_client_initialization_with_all_parameters(self):
        """Test client initialization with various parameter combinations."""
        # Test minimal initialization
        client1 = APIClient(host="test1.com", api_token="token1")
        assert client1.host == "test1.com"
        assert client1.timeout == 30.0  # default
        
        # Test with custom timeout
        client2 = APIClient(host="test2.com", api_token="token2", timeout=60.0)
        assert client2.timeout == 60.0
        
        # Test with SSL disabled
        client3 = APIClient(host="test3.com", api_token="token3", use_ssl=False)
        assert "http://" in client3.base_url
        
        # Test with custom base path
        client4 = APIClient(host="test4.com", api_token="token4", base_path="/custom/api")
        assert "/custom/api" in client4.base_url


class TestClientEdgeCases:
    """Test client edge cases and error scenarios."""
    
    @pytest.fixture
    def client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_generate_diagram_empty_networks(self, client):
        """Test generate_diagram with empty networks list."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = []
            
            result = client.generate_diagram()
            assert result is None
    
    def test_generate_diagram_unsupported_format(self, client):
        """Test generate_diagram with unsupported format."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = [{'name': 'test'}]
            
            with pytest.raises(ValueError, match="Unsupported format"):
                client.generate_diagram(format="unsupported")
    
    def test_diagram_methods_with_complex_network_data(self, client):
        """Test diagram methods with complex network structures."""
        complex_networks = [{
            'name': 'Complex Network',
            'resources': [
                {
                    'name': 'Web Server 1',
                    'address': '10.0.1.10/32', 
                    'type': 'server',
                    'groups': [
                        {'name': 'web-servers', 'id': 'ws1'},
                        {'name': 'production', 'id': 'prod'},
                        'string-group'
                    ]
                },
                {
                    'name': 'Database Server',
                    'address': '10.0.2.5/32',
                    'type': 'database',
                    'groups': [{'id': 'db-only-id'}]  # Group without name
                }
            ],
            'routers': [
                {'name': 'Main Router', 'id': 'r1'},
                {'name': 'Backup Router', 'id': 'r2'}
            ],
            'policies': [
                {'name': 'Web Access Policy', 'id': 'p1'},
                {'name': 'DB Access Policy', 'id': 'p2'},
                {'name': 'Admin Access Policy', 'id': 'p3'}
            ]
        }]
        
        with patch('netbird.network_map.get_network_topology_data') as mock_topology:
            mock_topology.return_value = {
                'all_source_groups': {'external-users', 'admin-users'},
                'group_connections': {
                    ('external-users', 'web-servers'): ['p1'],
                    ('admin-users', 'production'): ['p3']
                },
                'direct_connections': {
                    ('admin-users', 'res_0_1'): ['p2']
                },
                'group_name_to_nodes': {
                    'web-servers': ['res_0_0'],
                    'production': ['res_0_0']
                }
            }
            
            # Test mermaid with complex data
            result = client._create_mermaid_diagram(complex_networks)
            assert result is not None
            assert "Complex Network" in result
            assert "Web Server 1" in result
            assert "Database Server" in result