"""
Unit tests for resource handlers.
"""

import pytest
from unittest.mock import Mock, MagicMock

from netbird import APIClient
from netbird.models import (
    UserCreate, UserUpdate,
    PeerUpdate,
    GroupCreate,
    TokenCreate,
    SetupKeyCreate,
)
from netbird.resources.users import UsersResource
from netbird.resources.peers import PeersResource
from netbird.resources.groups import GroupsResource
from netbird.resources.accounts import AccountsResource
from netbird.resources.tokens import TokensResource
from netbird.resources.setup_keys import SetupKeysResource


class TestUsersResource:
    """Test UsersResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.users_resource = UsersResource(self.mock_client)
    
    def test_list_users(self):
        """Test listing users."""
        # Mock response data
        mock_users_data = [
            {
                "id": "user-1",
                "email": "user1@example.com",
                "name": "User One",
                "role": "user",
                "status": "active"
            },
            {
                "id": "user-2", 
                "email": "user2@example.com",
                "name": "User Two",
                "role": "admin",
                "status": "active"
            }
        ]
        
        self.mock_client.get.return_value = mock_users_data
        
        # Call the method
        users = self.users_resource.list()
        
        # Verify
        self.mock_client.get.assert_called_once_with("users")
        assert len(users) == 2
        assert all(isinstance(user, dict) for user in users)
        assert users[0]["email"] == "user1@example.com"
        assert users[1]["role"] == "admin"
    
    def test_create_user(self):
        """Test creating a user."""
        # Mock response
        mock_user_data = {
            "id": "user-123",
            "email": "new@example.com",
            "name": "New User",
            "role": "user",
            "status": "active"
        }
        self.mock_client.post.return_value = mock_user_data
        
        # Create user data
        user_data = UserCreate(
            email="new@example.com",
            name="New User",
            role="user"
        )
        
        # Call the method
        user = self.users_resource.create(user_data)
        
        # Verify
        self.mock_client.post.assert_called_once_with(
            "users",
            data=user_data.model_dump(exclude_unset=True)
        )
        assert isinstance(user, dict)
        assert user["email"] == "new@example.com"
    
    def test_get_user(self):
        """Test getting a specific user."""
        mock_user_data = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "user",
            "status": "active"
        }
        self.mock_client.get.return_value = mock_user_data
        
        user = self.users_resource.get("user-123")
        
        self.mock_client.get.assert_called_once_with("users/user-123")
        assert isinstance(user, dict)
        assert user["id"] == "user-123"
    
    def test_update_user(self):
        """Test updating a user."""
        mock_user_data = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Updated User",
            "role": "admin",
            "status": "active"
        }
        self.mock_client.put.return_value = mock_user_data
        
        update_data = UserUpdate(name="Updated User", role="admin")
        user = self.users_resource.update("user-123", update_data)
        
        self.mock_client.put.assert_called_once_with(
            "users/user-123",
            data=update_data.model_dump(exclude_unset=True)
        )
        assert user["name"] == "Updated User"
        assert user["role"] == "admin"
    
    def test_delete_user(self):
        """Test deleting a user."""
        self.users_resource.delete("user-123")
        
        self.mock_client.delete.assert_called_once_with("users/user-123")
    
    def test_invite_user(self):
        """Test inviting a user."""
        self.users_resource.invite("user-123")
        
        self.mock_client.post.assert_called_once_with("users/user-123/invite")
    
    def test_get_current_user(self):
        """Test getting current user."""
        mock_user_data = {
            "id": "current-user",
            "email": "current@example.com",
            "name": "Current User",
            "role": "admin",
            "status": "active"
        }
        self.mock_client.get.return_value = mock_user_data
        
        user = self.users_resource.get_current()
        
        self.mock_client.get.assert_called_once_with("users/current")
        assert user["id"] == "current-user"


class TestPeersResource:
    """Test PeersResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.peers_resource = PeersResource(self.mock_client)
    
    def test_list_peers_no_filters(self):
        """Test listing peers without filters."""
        mock_peers_data = [
            {
                "id": "peer-1",
                "name": "peer-one",
                "ip": "10.0.0.1",
                "connected": True,
                "ssh_enabled": False,
                "approval_required": True
            }
        ]
        self.mock_client.get.return_value = mock_peers_data
        
        peers = self.peers_resource.list()
        
        self.mock_client.get.assert_called_once_with("peers", params=None)
        assert len(peers) == 1
        assert isinstance(peers[0], dict)
    
    def test_list_peers_with_filters(self):
        """Test listing peers with name and IP filters."""
        mock_peers_data = []
        self.mock_client.get.return_value = mock_peers_data
        
        peers = self.peers_resource.list(name="test-peer", ip="10.0.0.1")
        
        expected_params = {"name": "test-peer", "ip": "10.0.0.1"}
        self.mock_client.get.assert_called_once_with("peers", params=expected_params)
    
    def test_get_peer(self):
        """Test getting a specific peer."""
        mock_peer_data = {
            "id": "peer-123",
            "name": "test-peer",
            "ip": "10.0.0.1",
            "connected": True,
            "ssh_enabled": True,
            "approval_required": True
        }
        self.mock_client.get.return_value = mock_peer_data
        
        peer = self.peers_resource.get("peer-123")
        
        self.mock_client.get.assert_called_once_with("peers/peer-123")
        assert peer["name"] == "test-peer"
    
    def test_update_peer(self):
        """Test updating a peer."""
        mock_peer_data = {
            "id": "peer-123",
            "name": "updated-peer",
            "ip": "10.0.0.1",
            "connected": True,
            "ssh_enabled": True,
            "approval_required": True
        }
        self.mock_client.put.return_value = mock_peer_data
        
        update_data = PeerUpdate(name="updated-peer", ssh_enabled=True)
        peer = self.peers_resource.update("peer-123", update_data)
        
        self.mock_client.put.assert_called_once_with(
            "peers/peer-123",
            data=update_data.model_dump(exclude_unset=True)
        )
        assert peer["name"] == "updated-peer"
    
    def test_get_accessible_peers(self):
        """Test getting accessible peers."""
        mock_peers_data = [
            {
                "id": "peer-2",
                "name": "accessible-peer",
                "ip": "10.0.0.2",
                "connected": True,
                "ssh_enabled": False,
                "approval_required": True
            }
        ]
        self.mock_client.get.return_value = mock_peers_data
        
        peers = self.peers_resource.get_accessible_peers("peer-123")
        
        self.mock_client.get.assert_called_once_with("peers/peer-123/accessible-peers")
        assert len(peers) == 1
        assert isinstance(peers[0], dict)


class TestGroupsResource:
    """Test GroupsResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.groups_resource = GroupsResource(self.mock_client)
    
    def test_list_groups(self):
        """Test listing groups."""
        mock_groups_data = [
            {
                "id": "group-1",
                "name": "developers",
                "peers_count": 5,
                "peers": [{"id": "peer-1"}, {"id": "peer-2"}]
            }
        ]
        self.mock_client.get.return_value = mock_groups_data
        
        groups = self.groups_resource.list()
        
        self.mock_client.get.assert_called_once_with("groups")
        assert len(groups) == 1
        assert isinstance(groups[0], dict)
    
    def test_create_group(self):
        """Test creating a group."""
        mock_group_data = {
            "id": "group-123",
            "name": "new-group",
            "peers_count": 0,
            "peers": []
        }
        self.mock_client.post.return_value = mock_group_data
        
        group_data = GroupCreate(name="new-group", peers=[])
        group = self.groups_resource.create(group_data)
        
        self.mock_client.post.assert_called_once_with(
            "groups",
            data=group_data.model_dump(exclude_unset=True)
        )
        assert group["name"] == "new-group"


class TestAccountsResource:
    """Test AccountsResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.accounts_resource = AccountsResource(self.mock_client)
    
    def test_list_accounts(self):
        """Test listing accounts."""
        mock_accounts_data = [
            {
                "id": "account-1",
                "domain": "example.com"
            }
        ]
        self.mock_client.get.return_value = mock_accounts_data
        
        accounts = self.accounts_resource.list()
        
        self.mock_client.get.assert_called_once_with("accounts")
        assert len(accounts) == 1
        assert isinstance(accounts[0], dict)


class TestTokensResource:
    """Test TokensResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.tokens_resource = TokensResource(self.mock_client)
    
    def test_list_tokens(self):
        """Test listing tokens for a user."""
        mock_tokens_data = [
            {
                "id": "token-1",
                "name": "api-token",
                "creation_date": "2023-01-01T00:00:00Z",
                "expiration_date": "2023-12-31T23:59:59Z",
                "created_by": "user-123"
            }
        ]
        self.mock_client.get.return_value = mock_tokens_data
        
        tokens = self.tokens_resource.list("user-123")
        
        self.mock_client.get.assert_called_once_with("users/user-123/tokens")
        assert len(tokens) == 1
        assert isinstance(tokens[0], dict)
    
    def test_create_token(self):
        """Test creating a token."""
        mock_token_data = {
            "id": "token-123",
            "name": "new-token",
            "creation_date": "2023-01-01T00:00:00Z",
            "expiration_date": "2023-01-31T23:59:59Z",
            "created_by": "user-123"
        }
        self.mock_client.post.return_value = mock_token_data
        
        token_data = TokenCreate(name="new-token", expires_in=30)
        token = self.tokens_resource.create("user-123", token_data)
        
        self.mock_client.post.assert_called_once_with(
            "users/user-123/tokens",
            data=token_data.model_dump()
        )
        assert token["name"] == "new-token"


class TestSetupKeysResource:
    """Test SetupKeysResource functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock(spec=APIClient)
        self.setup_keys_resource = SetupKeysResource(self.mock_client)
    
    def test_list_setup_keys(self):
        """Test listing setup keys."""
        mock_keys_data = [
            {
                "id": "key-1",
                "key": "actual-key-value",
                "name": "dev-key",
                "type": "reusable",
                "valid": True,
                "revoked": False,
                "used_times": 0,
                "state": "valid",
                "updated_at": "2023-01-01T00:00:00Z",
                "ephemeral": False
            }
        ]
        self.mock_client.get.return_value = mock_keys_data
        
        keys = self.setup_keys_resource.list()
        
        self.mock_client.get.assert_called_once_with("setup-keys")
        assert len(keys) == 1
        assert isinstance(keys[0], dict)
    
    def test_create_setup_key(self):
        """Test creating a setup key."""
        mock_key_data = {
            "id": "key-123",
            "key": "new-key-value",
            "name": "new-key",
            "type": "one-off",
            "valid": True,
            "revoked": False,
            "used_times": 0,
            "state": "valid",
            "updated_at": "2023-01-01T00:00:00Z",
            "ephemeral": False
        }
        self.mock_client.post.return_value = mock_key_data
        
        key_data = SetupKeyCreate(
            name="new-key",
            type="one-off",
            expires_in=3600
        )
        key = self.setup_keys_resource.create(key_data)
        
        self.mock_client.post.assert_called_once_with(
            "setup-keys",
            data=key_data.model_dump(exclude_unset=True)
        )
        assert key["name"] == "new-key"


class TestBaseResourceParsing:
    """Test base resource parsing functionality."""
    
    def test_parse_response_dict(self):
        """Test parsing dictionary response (should return dict directly)."""
        from netbird.resources.base import BaseResource
        
        mock_client = Mock()
        resource = BaseResource(mock_client)
        
        data = {"id": "test-123", "name": "Test"}
        
        # Mock model class (not used anymore)
        MockModel = Mock()
        
        result = resource._parse_response(data)
        
        # Should return dictionary directly without model validation
        assert result == data
    
    def test_parse_list_response(self):
        """Test parsing list response (should return list of dicts directly)."""
        from netbird.resources.base import BaseResource
        
        mock_client = Mock()
        resource = BaseResource(mock_client)
        
        data = [{"id": "1", "name": "One"}, {"id": "2", "name": "Two"}]
        
        # Mock model class (not used anymore)
        MockModel = Mock()
        
        result = resource._parse_list_response(data)
        
        # Should return list of dictionaries directly without model validation
        assert result == data
    
    def test_parse_list_response_invalid_data(self):
        """Test parsing non-list data (should handle gracefully now)."""
        from netbird.resources.base import BaseResource
        
        mock_client = Mock()
        resource = BaseResource(mock_client)
        
        # This test is no longer relevant since we return dictionaries directly
        # The _parse_list_response method should handle non-list data gracefully
        # The method now raises ValueError for non-list data
        with pytest.raises(ValueError, match="Expected list response"):
            resource._parse_list_response({"not": "a list"})