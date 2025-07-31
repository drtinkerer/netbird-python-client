"""
Additional tests to improve code coverage for specific edge cases and uncovered code paths.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from netbird.client import APIClient
from netbird.models.common import NetworkType, Protocol, PolicyAction
from netbird.network_map import generate_full_network_map, get_network_topology_data
from netbird.resources.base import BaseResource
from netbird.exceptions import NetBirdAPIError


class TestEnumMissingMethods:
    """Test _missing_ methods in enum classes for better coverage."""
    
    def test_network_type_missing_string_match(self):
        """Test NetworkType enum _missing_ method with string values."""
        # Test exact match
        result = NetworkType._missing_("ipv4")
        assert result == NetworkType.IPV4
        
        # Test case insensitive match
        result = NetworkType._missing_("IPV4")
        assert result == NetworkType.IPV4
        
        # Test non-existent value
        result = NetworkType._missing_("invalid")
        assert result is None
        
        # Test non-string value
        result = NetworkType._missing_(123)
        assert result is None
    
    def test_protocol_missing_string_match(self):
        """Test Protocol enum _missing_ method with string values."""
        # Test exact match
        result = Protocol._missing_("tcp")
        assert result == Protocol.TCP
        
        # Test case insensitive match
        result = Protocol._missing_("TCP")
        assert result == Protocol.TCP
        
        # Test non-existent value
        result = Protocol._missing_("invalid")
        assert result is None
        
        # Test non-string value
        result = Protocol._missing_(123)
        assert result is None
    
    def test_policy_action_missing_string_match(self):
        """Test PolicyAction enum _missing_ method with string values."""
        # Test exact match
        result = PolicyAction._missing_("accept")
        assert result == PolicyAction.ACCEPT
        
        # Test case insensitive match
        result = PolicyAction._missing_("ACCEPT")
        assert result == PolicyAction.ACCEPT
        
        # Test non-existent value
        result = PolicyAction._missing_("invalid")
        assert result is None


class TestClientDiagramEdgeCases:
    """Test edge cases in client diagram generation for better coverage."""
    
    @pytest.fixture
    def test_client(self):
        return APIClient(host="test.example.com", api_token="test-token")
    
    def test_mermaid_generation_with_string_groups(self, test_client):
        """Test mermaid generation when groups are strings instead of dicts."""
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            # Mock network data with string groups instead of dict groups
            mock_generate.return_value = [{
                'name': 'test-network',
                'resources': [{
                    'name': 'test-resource',
                    'address': '10.0.0.1',
                    'type': 'host',
                    'groups': ['string-group-1', 'string-group-2']  # String groups instead of dicts
                }],
                'policies': [],
                'routers': []
            }]
            
            # This should cover line 448 in client.py
            result = test_client.generate_diagram(format="mermaid")
            assert result is not None
            assert "string-group-1" in result
            assert "string-group-2" in result


class TestNetworkMapErrorHandling:
    """Test error handling in network map generation."""
    
    def test_generate_full_network_map_resource_fetch_error(self):
        """Test network map generation when resource fetching fails."""
        mock_client = Mock()
        
        # Mock successful network listing
        mock_client.networks.list.return_value = [{
            'id': 'net-1', 
            'name': 'Test Network',
            'resources': ['res-1'],
            'routers': [],
            'policies': []
        }]
        
        # Mock resource fetching to raise an exception (covers line 74-76)
        mock_client.networks.list_resources.side_effect = Exception("Resource fetch failed")
        mock_client.networks.list_routers.return_value = []
        mock_client.policies.get.return_value = None
        
        result = generate_full_network_map(mock_client)
        
        # Should still return results but with empty resources
        assert len(result) == 1
        assert result[0]['resources'] == []
    
    def test_generate_full_network_map_policy_fetch_error(self):
        """Test network map generation when policy fetching fails."""
        mock_client = Mock()
        
        # Mock successful network listing with policies
        mock_client.networks.list.return_value = [{
            'id': 'net-1', 
            'name': 'Test Network',
            'resources': [],
            'routers': [],
            'policies': ['pol-1']
        }]
        
        mock_client.networks.list_resources.return_value = []
        mock_client.networks.list_routers.return_value = []
        
        # Mock policy fetching to raise an exception (covers line 87-89)
        mock_client.policies.get.side_effect = Exception("Policy fetch failed")
        
        result = generate_full_network_map(mock_client)
        
        # Should still return results but with error policy entries
        assert len(result) == 1
        assert len(result[0]['policies']) == 1
        assert 'error' in result[0]['policies'][0]
    
    def test_generate_full_network_map_router_fetch_error(self):
        """Test network map generation when router fetching fails."""
        mock_client = Mock()
        
        # Mock successful network listing with routers
        mock_client.networks.list.return_value = [{
            'id': 'net-1', 
            'name': 'Test Network',
            'resources': [],
            'routers': ['rtr-1'],
            'policies': []
        }]
        
        mock_client.networks.list_resources.return_value = []
        mock_client.policies.get.return_value = None
        
        # Mock router fetching to raise an exception (covers line 114-116)
        mock_client.networks.list_routers.side_effect = Exception("Router fetch failed")
        
        result = generate_full_network_map(mock_client)
        
        # Should still return results but with empty routers
        assert len(result) == 1
        assert result[0]['routers'] == []
    
    def test_generate_full_network_map_authentication_error(self):
        """Test network map generation with authentication error."""
        mock_client = Mock()
        
        # Mock authentication error
        from netbird.exceptions import NetBirdAuthenticationError
        mock_client.networks.list.side_effect = NetBirdAuthenticationError("Auth failed")
        
        # Should re-raise as NetBirdAuthenticationError (covers line 125)
        with pytest.raises(NetBirdAuthenticationError, match="Authentication failed"):
            generate_full_network_map(mock_client)
    
    def test_generate_full_network_map_api_error(self):
        """Test network map generation with API error."""
        mock_client = Mock()
        
        # Mock API error
        from netbird.exceptions import NetBirdAPIError
        mock_client.networks.list.side_effect = NetBirdAPIError("API failed", status_code=500)
        
        # Should re-raise as NetBirdAPIError (covers line 128-129)
        with pytest.raises(NetBirdAPIError, match="API Error"):
            generate_full_network_map(mock_client)
    
    def test_get_topology_data_without_optimization(self):
        """Test topology data generation without optimization."""
        mock_client = Mock()
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            mock_generate.return_value = []
            
            # Test without optimization (covers line 171)
            result = get_network_topology_data(mock_client, optimize_connections=False)
            
            assert 'networks' in result
            assert 'all_source_groups' in result
            assert result['all_source_groups'] == set()


class TestBaseResourceEdgeCases:
    """Test edge cases in base resource class."""
    
    def test_base_resource_instantiation_success(self):
        """Test that BaseResource can be instantiated with a client."""
        # This should cover line 17-18 in base.py
        from unittest.mock import Mock
        mock_client = Mock()
        resource = BaseResource(mock_client)
        assert resource.client == mock_client
    
    def test_base_resource_parse_response_edge_cases(self):
        """Test _parse_response method with edge cases."""
        from unittest.mock import Mock
        resource = BaseResource(Mock())
        
        # Test with None (line 22-23)
        result = resource._parse_response(None)
        assert result == {}
        
        # Test with empty data
        result = resource._parse_response({})
        assert result == {}
        
        # Test with invalid data type that can't be converted (line 27-30)
        result = resource._parse_response(object())
        assert result == {}


class TestClientTypeCheckingImports:
    """Test imports that are only executed during TYPE_CHECKING."""
    
    def test_type_checking_imports(self):
        """Test that TYPE_CHECKING imports are handled correctly."""
        # This test helps ensure the TYPE_CHECKING imports are recognized
        # even though they're not executed at runtime
        
        from netbird import client
        
        # Verify the module loaded successfully
        assert hasattr(client, 'APIClient')
        
        # The TYPE_CHECKING imports (lines 17-27) are covered by this import
        # since they're part of the module definition
        
        # Create client instance to ensure all imports work
        test_client = client.APIClient(host="test.example.com", api_token="test-token")
        assert test_client is not None


class TestDiagramGenerationErrorCases:
    """Test specific error cases in diagram generation."""
    
    def test_diagram_with_empty_network_name(self):
        """Test diagram generation with empty network names."""
        from netbird.client import APIClient
        
        client = APIClient(host="test.example.com", api_token="test-token")
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            # Mock data with empty network name
            mock_generate.return_value = [{
                'name': '',  # Empty name
                'resources': [],
                'policies': [],
                'routers': []
            }]
            
            result = client.generate_diagram(format="mermaid")
            assert result is not None
            # Should handle empty names gracefully


class TestAdditionalCoverage:
    """Additional tests to catch remaining uncovered lines."""
    
    def test_diagram_with_complex_resource_groups(self):
        """Test diagram generation with complex resource group structures."""
        from netbird.client import APIClient
        
        client = APIClient(host="test.example.com", api_token="test-token")
        
        with patch('netbird.network_map.generate_full_network_map') as mock_generate:
            # Mock data that exercises different group handling paths
            mock_generate.return_value = [{
                'name': 'test-network',
                'resources': [{
                    'name': 'test-resource',
                    'address': '10.0.0.1',
                    'type': 'host',
                    'groups': [
                        {'name': 'group1', 'id': 'g1'},  # Dict with name
                        {'id': 'g2'},  # Dict without name  
                        'string-group',  # String group
                        None  # None group (should be handled gracefully)
                    ]
                }],
                'policies': [],
                'routers': []
            }]
            
            result = client.generate_diagram(format="mermaid")
            assert result is not None