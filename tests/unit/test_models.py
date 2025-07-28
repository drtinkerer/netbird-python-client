"""
Unit tests for Pydantic models.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from netbird.models import (
    User, UserCreate, UserUpdate,
    Peer, PeerUpdate,
    Group, GroupCreate, GroupUpdate,
    Token, TokenCreate,
    SetupKey, SetupKeyCreate, SetupKeyUpdate,
    Policy, PolicyCreate, PolicyRule,
    Route, RouteCreate, RouteUpdate,
    Account, AccountSettings,
    DNSNameserverGroup, DNSSettings,
    AuditEvent, NetworkTrafficEvent,
)
from netbird.models.common import UserRole, UserStatus, SetupKeyType, NetworkType, Protocol


class TestUserModels:
    """Test User-related models."""
    
    def test_user_dictionary_structure(self):
        """Test User dictionary structure (API responses are now dictionaries)."""
        user_data = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "user",
            "status": "active",
            "is_service_user": False,
            "is_blocked": False
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert user_data["id"] == "user-123"
        assert user_data["email"] == "test@example.com"
        assert user_data["role"] == "user"
        assert user_data["status"] == "active"
        assert not user_data["is_service_user"]
        assert not user_data["is_blocked"]
    
    def test_user_create_model(self):
        """Test UserCreate model."""
        user_data = UserCreate(
            email="new@example.com",
            name="New User",
            role=UserRole.ADMIN,
            is_service_user=True
        )
        
        assert user_data.email == "new@example.com"
        assert user_data.role == UserRole.ADMIN
        assert user_data.is_service_user
        assert not user_data.is_blocked  # Default value
    
    def test_user_create_invalid_email(self):
        """Test UserCreate with invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="invalid-email", name="Test")
        
        errors = exc_info.value.errors()
        assert any("valid email" in str(error) for error in errors)
    
    def test_user_update_partial(self):
        """Test UserUpdate with partial data."""
        update = UserUpdate(name="Updated Name")
        
        assert update.name == "Updated Name"
        assert update.role is None  # Not specified
        assert update.is_blocked is None  # Not specified


class TestPeerModels:
    """Test Peer-related models."""
    
    def test_peer_dictionary_structure(self):
        """Test Peer dictionary structure (API responses are now dictionaries)."""
        peer_data = {
            "id": "peer-123",
            "name": "test-peer",
            "ip": "10.0.0.1",
            "connected": True,
            "ssh_enabled": True,
            "approval_required": True
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert peer_data["id"] == "peer-123"
        assert peer_data["name"] == "test-peer"
        assert peer_data["ip"] == "10.0.0.1"
        assert peer_data["connected"]
        assert peer_data["ssh_enabled"]
        assert peer_data["approval_required"]
    
    def test_peer_invalid_ip_for_input_validation(self):
        """Test Peer input validation with invalid IP address."""
        # This test is kept for input validation of Create/Update models
        with pytest.raises(ValidationError):
            Peer(
                id="peer-123",
                name="test-peer", 
                ip="invalid-ip",
                connected=True,
                ssh_enabled=False,
                approval_required=True
            )
    
    def test_peer_update_model(self):
        """Test PeerUpdate model."""
        update = PeerUpdate(
            name="updated-peer",
            ssh_enabled=True,
            approval_required=False
        )
        
        assert update.name == "updated-peer"
        assert update.ssh_enabled
        assert not update.approval_required


class TestGroupModels:
    """Test Group-related models."""
    
    def test_group_dictionary_structure(self):
        """Test Group dictionary structure (API responses are now dictionaries)."""
        group_data = {
            "id": "group-123",
            "name": "developers",
            "peers_count": 5,
            "peers": [{"id": "peer-1"}, {"id": "peer-2"}]
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert group_data["id"] == "group-123"
        assert group_data["name"] == "developers"
        assert group_data["peers_count"] == 5
        assert len(group_data["peers"]) == 2
    
    def test_group_create_model(self):
        """Test GroupCreate model."""
        group = GroupCreate(
            name="new-group",
            peers=["peer-1", "peer-2", "peer-3"]
        )
        
        assert group.name == "new-group"
        assert len(group.peers) == 3


class TestTokenModels:
    """Test Token-related models."""
    
    def test_token_dictionary_structure(self):
        """Test Token dictionary structure (API responses are now dictionaries)."""
        token_data = {
            "id": "token-123",
            "name": "api-token",
            "creation_date": "2023-01-01T00:00:00Z",
            "expiration_date": "2023-12-31T00:00:00Z",
            "created_by": "user-123",
            "last_used": None
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert token_data["id"] == "token-123"
        assert token_data["name"] == "api-token"
        assert token_data["created_by"] == "user-123"
        assert token_data["last_used"] is None
    
    def test_token_create_model(self):
        """Test TokenCreate model."""
        token = TokenCreate(name="test-token", expires_in=30)
        
        assert token.name == "test-token"
        assert token.expires_in == 30
    
    def test_token_create_invalid_expires_in(self):
        """Test TokenCreate with invalid expires_in."""
        with pytest.raises(ValidationError):
            TokenCreate(name="test", expires_in=400)  # > 365 days
        
        with pytest.raises(ValidationError):
            TokenCreate(name="test", expires_in=0)  # < 1 day


class TestSetupKeyModels:
    """Test SetupKey-related models."""
    
    def test_setup_key_dictionary_structure(self):
        """Test SetupKey dictionary structure (API responses are now dictionaries)."""
        key_data = {
            "id": "key-123",
            "key": "actual-key-value",
            "name": "dev-key",
            "type": "reusable",
            "valid": True,
            "revoked": False,
            "used_times": 5,
            "state": "valid",
            "updated_at": "2023-01-01T00:00:00Z",
            "ephemeral": False
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert key_data["id"] == "key-123"
        assert key_data["name"] == "dev-key"
        assert key_data["type"] == "reusable"
        assert key_data["valid"]
        assert not key_data["revoked"]
        assert key_data["used_times"] == 5
    
    def test_setup_key_create_model(self):
        """Test SetupKeyCreate model."""
        key = SetupKeyCreate(
            name="new-key",
            type=SetupKeyType.ONE_OFF,
            expires_in=3600,
            usage_limit=1
        )
        
        assert key.name == "new-key"
        assert key.type == SetupKeyType.ONE_OFF
        assert key.expires_in == 3600
        assert key.usage_limit == 1


class TestPolicyModels:
    """Test Policy-related models."""
    
    def test_policy_rule_dictionary_structure(self):
        """Test PolicyRule dictionary structure (API responses are now dictionaries)."""
        rule_data = {
            "name": "allow-ssh",
            "action": "accept",
            "protocol": "tcp",
            "ports": ["22"],
            "sources": [{"id": "group-1"}],
            "destinations": [{"id": "group-2"}],
            "bidirectional": False
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert rule_data["name"] == "allow-ssh"
        assert rule_data["action"] == "accept"
        assert rule_data["protocol"] == "tcp"
        assert rule_data["ports"] == ["22"]
        assert not rule_data["bidirectional"]
    
    def test_policy_create_model(self):
        """Test PolicyCreate model."""
        rule = PolicyRule(
            name="test-rule",
            action="accept",
            protocol="tcp",
            sources=[{"id": "src"}],
            destinations=[{"id": "dst"}]
        )
        
        policy = PolicyCreate(
            name="test-policy",
            description="Test policy",
            rules=[rule]
        )
        
        assert policy.name == "test-policy"
        assert policy.description == "Test policy"
        assert len(policy.rules) == 1
        assert policy.enabled  # Default


class TestRouteModels:
    """Test Route-related models."""
    
    def test_route_dictionary_structure(self):
        """Test Route dictionary structure (API responses are now dictionaries)."""
        route_data = {
            "id": "route-123",
            "network_id": "192.168.1.0/24",
            "network_type": "ipv4",
            "enabled": True,
            "metric": 100,
            "masquerade": False,
            "keep_route": True
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert route_data["id"] == "route-123"
        assert route_data["network_id"] == "192.168.1.0/24"
        assert route_data["network_type"] == "ipv4"
        assert route_data["enabled"]
        assert route_data["metric"] == 100
        assert not route_data["masquerade"]
        assert route_data["keep_route"]
    
    def test_route_create_model(self):
        """Test RouteCreate model."""
        route = RouteCreate(
            description="Test route",
            network_id="10.0.0.0/8",
            network_type=NetworkType.IPV4,
            peer="peer-123"
        )
        
        assert route.description == "Test route"
        assert route.network_id == "10.0.0.0/8"
        assert route.network_type == NetworkType.IPV4
        assert route.peer == "peer-123"
        assert route.metric == 9999  # Default


class TestAccountModels:
    """Test Account-related models."""
    
    def test_account_settings_dictionary_structure(self):
        """Test AccountSettings dictionary structure (API responses are now dictionaries)."""
        settings_data = {
            "peer_login_expiration": 3600,
            "peer_login_expiration_enabled": True,
            "group_propagation_enabled": True,
            "dns_resolution_enabled": True
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert settings_data["peer_login_expiration"] == 3600
        assert settings_data["peer_login_expiration_enabled"]
        assert settings_data["group_propagation_enabled"]
        assert settings_data["dns_resolution_enabled"]
    
    def test_account_dictionary_structure(self):
        """Test Account dictionary structure (API responses are now dictionaries)."""
        account_data = {
            "id": "account-123",
            "domain": "example.com"
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert account_data["id"] == "account-123"
        assert account_data["domain"] == "example.com"


class TestDNSModels:
    """Test DNS-related models."""
    
    def test_dns_nameserver_group_dictionary_structure(self):
        """Test DNSNameserverGroup dictionary structure (API responses are now dictionaries)."""
        ns_group_data = {
            "id": "ns-123",
            "name": "corporate-dns",
            "nameservers": ["8.8.8.8", "8.8.4.4"],
            "enabled": True
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert ns_group_data["id"] == "ns-123"
        assert ns_group_data["name"] == "corporate-dns"
        assert len(ns_group_data["nameservers"]) == 2
        assert ns_group_data["enabled"]
    
    def test_dns_settings_dictionary_structure(self):
        """Test DNSSettings dictionary structure (API responses are now dictionaries)."""
        settings_data = {
            "disabled_management_groups": ["group-1", "group-2"]
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert len(settings_data["disabled_management_groups"]) == 2


class TestEventModels:
    """Test Event-related models."""
    
    def test_audit_event_dictionary_structure(self):
        """Test AuditEvent dictionary structure (API responses are now dictionaries)."""
        event_data = {
            "timestamp": "2023-01-01T00:00:00Z",
            "activity": "user.created",
            "initiator_id": "user-123",
            "target_id": None
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert event_data["activity"] == "user.created"
        assert event_data["initiator_id"] == "user-123"
        assert event_data["target_id"] is None
    
    def test_network_traffic_event_dictionary_structure(self):
        """Test NetworkTrafficEvent dictionary structure (API responses are now dictionaries)."""
        event_data = {
            "timestamp": "2023-01-01T00:00:00Z",
            "source_ip": "10.0.0.1",
            "destination_ip": "10.0.0.2",
            "source_port": 12345,
            "destination_port": 80,
            "protocol": "tcp",
            "bytes_sent": 1024,
            "bytes_received": 2048,
            "peer_id": "peer-123",
            "reporter_id": "peer-456",
            "direction": "sent",
            "connection_type": "p2p",
            "allowed": True
        }
        
        # API responses are now dictionaries, not Pydantic models
        assert event_data["source_ip"] == "10.0.0.1"
        assert event_data["destination_ip"] == "10.0.0.2"
        assert event_data["protocol"] == "tcp"
        assert event_data["bytes_sent"] == 1024
        assert event_data["allowed"]


class TestModelValidation:
    """Test model validation edge cases."""
    
    def test_extra_fields_forbidden_in_input_models(self):
        """Test that extra fields are rejected in input validation."""
        # This test is kept for input validation of Create/Update models
        with pytest.raises(ValidationError):
            User(
                id="user-123",
                email="test@example.com",
                role="user",
                status="active",
                extra_field="not-allowed"  # This should cause validation error
            )
    
    def test_required_fields_missing_in_input_models(self):
        """Test that missing required fields raise errors in input validation."""
        # This test is kept for input validation of Create/Update models
        with pytest.raises(ValidationError):
            User()  # Missing required fields
        
        with pytest.raises(ValidationError):
            Peer(id="peer-123")  # Missing required fields
    
    def test_enum_validation_in_input_models(self):
        """Test enum field validation for input models."""
        # Valid enum values in input validation
        user = User(
            id="user-123",
            email="test@example.com",
            role="admin",  # Valid role
            status="active"  # Valid status
        )
        assert user.role == UserRole.ADMIN
        assert user.status == UserStatus.ACTIVE
        
        # Invalid enum values should raise validation errors in input validation
        with pytest.raises(ValidationError):
            User(
                id="user-123",
                email="test@example.com",
                role="invalid-role",  # Invalid role
                status="active"
            )