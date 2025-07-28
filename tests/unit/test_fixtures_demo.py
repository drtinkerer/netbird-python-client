"""
Demonstration of industry-standard fixtures usage.

This file shows how to use fixture files instead of inline test data.
Industry standard approach for professional test suites.
"""

import pytest
from unittest.mock import Mock

from netbird import APIClient
from tests.fixtures import load_api_response, load_sample_data, load_mock_config


class TestFixturesDemo:
    """Demonstrate industry-standard fixture usage."""
    
    def test_user_dictionary_with_fixture_file(self):
        """Test User dictionary data from fixture file (API responses are now dictionaries)."""
        # Load test data from fixture file
        user_data = load_sample_data("user")
        
        # API responses are now dictionaries, not Pydantic models
        assert user_data["id"] == "user-123"
        assert user_data["email"] == "test@example.com"
        assert user_data["role"] == "user"
        assert user_data["is_current"] is True
    
    def test_peer_dictionary_with_fixture_file(self):
        """Test Peer dictionary data from fixture file (API responses are now dictionaries)."""
        peer_data = load_sample_data("peer")
        
        # API responses are now dictionaries, not Pydantic models
        assert peer_data["id"] == "peer-123"
        assert peer_data["name"] == "test-peer"
        assert peer_data["city_name"] == "San Francisco"
        assert peer_data["country_code"] == "US"
        assert len(peer_data["groups"]) == 1
    
    def test_api_response_fixture(self):
        """Test using API response fixtures (API responses are now dictionaries)."""
        users_response = load_api_response("users")
        
        assert isinstance(users_response, list)
        assert len(users_response) == 2
        
        # Test first user (dictionary)
        assert users_response[0]["role"] == "user"
        
        # Test second user (admin)
        assert users_response[1]["role"] == "admin"
    
    def test_config_fixtures(self):
        """Test using configuration fixtures."""
        client_config = load_mock_config("client")
        auth_config = load_mock_config("auth")
        
        # Test client configuration
        assert "default_client" in client_config
        default = client_config["default_client"]
        assert default["host"] == "api.netbird.io"
        assert default["timeout"] == 30.0
        
        # Test auth configuration
        assert "token_auth" in auth_config
        tokens = auth_config["token_auth"]
        assert "valid_token" in tokens
        assert "invalid_token" in tokens
    
    def test_pytest_fixtures_integration(self, mock_users_response, client_configs):
        """Test integration with pytest fixtures (API responses are now dictionaries)."""
        # These fixtures are loaded from files via conftest.py
        assert len(mock_users_response) == 2
        assert "environments" in client_configs
        
        # Can directly use dictionaries in tests
        assert mock_users_response[0]["email"] == "user1@example.com"


class TestFixtureVsInlineComparison:
    """Compare fixture approach vs inline data approach."""
    
    def test_old_approach_inline_data(self):
        """OLD: Inline test data (harder to maintain)."""
        # Hard to maintain - data scattered across test files
        user_data = {
            "id": "user-123",
            "email": "test@example.com", 
            "name": "Test User",
            "role": "user",
            "status": "active",
            "is_service_user": False,
            "is_blocked": False,
            "auto_groups": ["group-1"],
            "issued": "2023-01-01T00:00:00Z",
            "permissions": {"view_groups": True, "manage_peers": False},
            "is_current": True,
            "last_login": "2023-01-01T10:00:00Z"
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert user_data["email"] == "test@example.com"
    
    def test_new_approach_fixture_files(self):
        """NEW: Fixture files (industry standard)."""
        # Clean, maintainable - data centralized in fixture files
        user_data = load_sample_data("user")
        
        # API responses are now dictionaries, not Pydantic models
        assert user_data["email"] == "test@example.com"


class TestAdvancedFixtureUsage:
    """Advanced fixture usage patterns."""
    
    def test_multiple_fixture_files(self):
        """Use multiple fixture files in one test."""
        users = load_api_response("users")
        groups = load_api_response("groups")
        peers = load_api_response("peers")
        
        # Test relationships between resources
        assert len(users) >= 1
        assert len(groups) >= 1
        assert len(peers) >= 1
        
        # Validate each resource type (dictionaries)
        for user_data in users:
            assert user_data["id"] is not None
        
        for group_data in groups:
            assert group_data["id"] is not None
    
    def test_environment_specific_config(self):
        """Test environment-specific configurations."""
        client_config = load_mock_config("client")
        
        # Test different environments
        envs = client_config["environments"]
        
        dev_config = envs["development"]
        assert dev_config["host"] == "dev.netbird.io"
        assert dev_config["timeout"] == 30.0
        
        prod_config = envs["production"]
        assert prod_config["host"] == "api.netbird.io"
        assert prod_config["timeout"] == 10.0
    
    def test_auth_scenarios(self):
        """Test authentication scenarios from fixtures."""
        auth_config = load_mock_config("auth")
        scenarios = auth_config["auth_scenarios"]
        
        # Test successful authentication scenario
        success_scenario = scenarios["successful_auth"]
        assert success_scenario["expected_status"] == 200
        
        # Test invalid authentication scenario
        invalid_scenario = scenarios["invalid_auth"]
        assert invalid_scenario["expected_status"] == 401
        assert "authentication failed" in invalid_scenario["expected_error"]