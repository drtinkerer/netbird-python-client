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
    
    def test_user_model_valid(self):
        """Test User model with valid data."""
        user_data = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "user",
            "status": "active",
            "is_service_user": False,
            "is_blocked": False
        }
        
        user = User(**user_data)
        assert user.id == "user-123"
        assert user.email == "test@example.com"
        assert user.role == UserRole.USER
        assert user.status == UserStatus.ACTIVE
        assert not user.is_service_user
        assert not user.is_blocked
    
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
    
    def test_peer_model_valid(self):
        """Test Peer model with valid data."""
        peer_data = {
            "id": "peer-123",
            "name": "test-peer",
            "ip": "10.0.0.1",
            "connected": True,
            "ssh_enabled": True,
            "approved": True
        }
        
        peer = Peer(**peer_data)
        assert peer.id == "peer-123"
        assert peer.name == "test-peer"
        assert str(peer.ip) == "10.0.0.1"
        assert peer.connected
        assert peer.ssh_enabled
        assert peer.approved
    
    def test_peer_invalid_ip(self):
        """Test Peer with invalid IP address."""
        with pytest.raises(ValidationError):
            Peer(
                id="peer-123",
                name="test-peer", 
                ip="invalid-ip",
                connected=True,
                ssh_enabled=False,
                approved=True
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
    
    def test_group_model(self):
        """Test Group model."""
        group = Group(
            id="group-123",
            name="developers",
            peers_count=5,
            peers=["peer-1", "peer-2"]
        )
        
        assert group.id == "group-123"
        assert group.name == "developers"
        assert group.peers_count == 5
        assert len(group.peers) == 2
    
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
    
    def test_token_model(self):
        """Test Token model."""
        token = Token(
            id="token-123",
            name="api-token",
            creation_date=datetime(2023, 1, 1),
            expiration_date=datetime(2023, 12, 31),
            created_by="user-123"
        )
        
        assert token.id == "token-123"
        assert token.name == "api-token"
        assert token.created_by == "user-123"
        assert token.last_used is None  # Default
    
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
    
    def test_setup_key_model(self):
        """Test SetupKey model."""
        key = SetupKey(
            id="key-123",
            key="actual-key-value",
            name="dev-key",
            expires_in=86400,
            type="reusable",
            valid=True,
            revoked=False,
            used_times=5,
            state="valid",
            updated_at=datetime.now(),
            ephemeral=False
        )
        
        assert key.id == "key-123"
        assert key.name == "dev-key"
        assert key.type == SetupKeyType.REUSABLE
        assert key.valid
        assert not key.revoked
        assert key.used_times == 5
    
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
    
    def test_policy_rule_model(self):
        """Test PolicyRule model."""
        rule = PolicyRule(
            name="allow-ssh",
            action="accept",
            protocol="tcp",
            ports=["22"],
            sources=["group-1"],
            destinations=["group-2"]
        )
        
        assert rule.name == "allow-ssh"
        assert rule.action == "accept"
        assert rule.protocol == Protocol.TCP
        assert rule.ports == ["22"]
        assert not rule.bidirectional  # Default
    
    def test_policy_create_model(self):
        """Test PolicyCreate model."""
        rule = PolicyRule(
            name="test-rule",
            action="accept",
            protocol="tcp",
            sources=["src"],
            destinations=["dst"]
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
    
    def test_route_model(self):
        """Test Route model."""
        route = Route(
            id="route-123",
            network_id="192.168.1.0/24",
            network_type="ipv4",
            enabled=True,
            metric=100,
            masquerade=False,
            keep_route=True
        )
        
        assert route.id == "route-123"
        assert route.network_id == "192.168.1.0/24"
        assert route.network_type == NetworkType.IPV4
        assert route.enabled
        assert route.metric == 100
        assert not route.masquerade
        assert route.keep_route
    
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
    
    def test_account_settings_model(self):
        """Test AccountSettings model."""
        settings = AccountSettings(
            peer_login_expiration=3600,
            peer_login_expiration_enabled=True,
            group_propagation_enabled=True,
            dns_resolution_enabled=True
        )
        
        assert settings.peer_login_expiration == 3600
        assert settings.peer_login_expiration_enabled
        assert settings.group_propagation_enabled
        assert settings.dns_resolution_enabled
    
    def test_account_model(self):
        """Test Account model."""
        account = Account(
            id="account-123",
            domain="example.com"
        )
        
        assert account.id == "account-123"
        assert account.domain == "example.com"


class TestDNSModels:
    """Test DNS-related models."""
    
    def test_dns_nameserver_group_model(self):
        """Test DNSNameserverGroup model."""
        ns_group = DNSNameserverGroup(
            id="ns-123",
            name="corporate-dns",
            nameservers=["8.8.8.8", "8.8.4.4"],
            enabled=True
        )
        
        assert ns_group.id == "ns-123"
        assert ns_group.name == "corporate-dns"
        assert len(ns_group.nameservers) == 2
        assert ns_group.enabled
    
    def test_dns_settings_model(self):
        """Test DNSSettings model."""
        settings = DNSSettings(
            disabled_management_groups=["group-1", "group-2"]
        )
        
        assert len(settings.disabled_management_groups) == 2


class TestEventModels:
    """Test Event-related models."""
    
    def test_audit_event_model(self):
        """Test AuditEvent model."""
        event = AuditEvent(
            timestamp=datetime.now(),
            activity="user.created",
            initiator_id="user-123"
        )
        
        assert event.activity == "user.created"
        assert event.initiator_id == "user-123"
        assert event.target_id is None  # Optional
    
    def test_network_traffic_event_model(self):
        """Test NetworkTrafficEvent model."""
        event = NetworkTrafficEvent(
            timestamp=datetime.now(),
            source_ip="10.0.0.1",
            destination_ip="10.0.0.2",
            source_port=12345,
            destination_port=80,
            protocol="tcp",
            bytes_sent=1024,
            bytes_received=2048,
            peer_id="peer-123",
            reporter_id="peer-456",
            direction="sent",
            connection_type="p2p",
            allowed=True
        )
        
        assert str(event.source_ip) == "10.0.0.1"
        assert str(event.destination_ip) == "10.0.0.2"
        assert event.protocol == Protocol.TCP
        assert event.bytes_sent == 1024
        assert event.allowed


class TestModelValidation:
    """Test model validation edge cases."""
    
    def test_extra_fields_forbidden(self):
        """Test that extra fields are rejected."""
        with pytest.raises(ValidationError):
            User(
                id="user-123",
                email="test@example.com",
                role="user",
                status="active",
                extra_field="not-allowed"  # This should cause validation error
            )
    
    def test_required_fields_missing(self):
        """Test that missing required fields raise errors."""
        with pytest.raises(ValidationError):
            User()  # Missing required fields
        
        with pytest.raises(ValidationError):
            Peer(id="peer-123")  # Missing required fields
    
    def test_enum_validation(self):
        """Test enum field validation."""
        # Valid enum values
        user = User(
            id="user-123",
            email="test@example.com",
            role="admin",  # Valid role
            status="active"  # Valid status
        )
        assert user.role == UserRole.ADMIN
        assert user.status == UserStatus.ACTIVE
        
        # Invalid enum values should raise validation errors
        with pytest.raises(ValidationError):
            User(
                id="user-123",
                email="test@example.com",
                role="invalid-role",  # Invalid role
                status="active"
            )