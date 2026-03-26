"""Tests for model updates in Phase 1."""

import pytest

from netbird.models.common import BaseModel
from netbird.models.account import AccountSettings, Account
from netbird.models.peer import PeerUpdate
from netbird.models.policy import PolicyRule
from netbird.models.user import UserInviteCreate, UserInvite


@pytest.mark.unit
class TestBaseModelExtraAllow:
    def test_extra_fields_accepted(self):
        """BaseModel with extra='allow' should accept unknown fields."""

        class TestModel(BaseModel):
            name: str

        model = TestModel(name="test", unknown_field="value")
        assert model.name == "test"
        assert model.model_extra == {"unknown_field": "value"}

    def test_extra_fields_in_dump(self):
        """Extra fields should be included in model_dump."""

        class TestModel(BaseModel):
            name: str

        model = TestModel(name="test", future_field=42)
        dumped = model.model_dump()
        assert dumped["name"] == "test"
        assert dumped["future_field"] == 42


@pytest.mark.unit
class TestAccountSettingsNewFields:
    def test_extra_settings_field_with_alias(self):
        settings = AccountSettings(
            extra_settings={"peer_approval": True, "traffic_logs": False}
        )
        assert settings.extra_settings == {
            "peer_approval": True,
            "traffic_logs": False,
        }
        # Verify alias serialization
        dumped = settings.model_dump(by_alias=True, exclude_unset=True)
        assert "extra" in dumped
        assert dumped["extra"]["peer_approval"] is True

    def test_extra_settings_from_alias(self):
        """Should accept 'extra' key via alias."""
        settings = AccountSettings.model_validate({"extra": {"user_approval": True}})
        assert settings.extra_settings == {"user_approval": True}

    def test_new_optional_fields(self):
        settings = AccountSettings(
            peer_inactivity_expiration=3600,
            routing_peer_dns_resolution_enabled=True,
            network_range="100.64.0.0/10",
            peer_expose_enabled=True,
            peer_expose_groups=["group-1"],
            auto_update_version="0.28.0",
            embedded_idp_enabled=False,
            local_auth_disabled=False,
        )
        assert settings.peer_inactivity_expiration == 3600
        assert settings.routing_peer_dns_resolution_enabled is True
        assert settings.network_range == "100.64.0.0/10"
        assert settings.peer_expose_enabled is True
        assert settings.peer_expose_groups == ["group-1"]
        assert settings.auto_update_version == "0.28.0"
        assert settings.embedded_idp_enabled is False
        assert settings.local_auth_disabled is False

    def test_defaults_are_none(self):
        settings = AccountSettings()
        assert settings.peer_inactivity_expiration is None
        assert settings.routing_peer_dns_resolution_enabled is None
        assert settings.extra_settings is None


@pytest.mark.unit
class TestAccountOnboarding:
    def test_onboarding_field(self):
        account = Account(
            id="acc-1",
            domain="example.com",
            onboarding={"signup_form_pending": True},
        )
        assert account.onboarding == {"signup_form_pending": True}


@pytest.mark.unit
class TestPeerUpdateIp:
    def test_ip_field(self):
        update = PeerUpdate(ip="10.0.0.5")
        assert update.ip == "10.0.0.5"
        dumped = update.model_dump(exclude_unset=True)
        assert dumped["ip"] == "10.0.0.5"


@pytest.mark.unit
class TestPolicyRuleNewFields:
    def test_port_ranges(self):
        rule = PolicyRule(
            name="test",
            action="accept",
            protocol="tcp",
            port_ranges=[{"start": 8000, "end": 9000}],
        )
        assert rule.port_ranges == [{"start": 8000, "end": 9000}]

    def test_source_resource_alias(self):
        rule = PolicyRule(
            name="test",
            action="accept",
            protocol="tcp",
            source_resource={"id": "res-1", "type": "host"},
        )
        assert rule.source_resource == {"id": "res-1", "type": "host"}
        dumped = rule.model_dump(by_alias=True, exclude_unset=True)
        assert "sourceResource" in dumped

    def test_destination_resource_alias(self):
        rule = PolicyRule(
            name="test",
            action="accept",
            protocol="tcp",
            destination_resource={"id": "res-2", "type": "subnet"},
        )
        assert rule.destination_resource == {"id": "res-2", "type": "subnet"}
        dumped = rule.model_dump(by_alias=True, exclude_unset=True)
        assert "destinationResource" in dumped

    def test_from_camel_case_json(self):
        """Should accept camelCase keys from API response."""
        rule = PolicyRule.model_validate(
            {
                "name": "test",
                "action": "accept",
                "protocol": "tcp",
                "sourceResource": {"id": "res-1"},
                "destinationResource": {"id": "res-2"},
            }
        )
        assert rule.source_resource == {"id": "res-1"}
        assert rule.destination_resource == {"id": "res-2"}


@pytest.mark.unit
class TestUserInviteModels:
    def test_user_invite_create(self):
        invite = UserInviteCreate(
            email="test@example.com",
            name="Test User",
            role="user",
            auto_groups=["group-1"],
            expires_in=86400,
        )
        dumped = invite.model_dump(exclude_unset=True)
        assert dumped["email"] == "test@example.com"
        assert dumped["expires_in"] == 86400

    def test_user_invite(self):
        invite = UserInvite(
            id="inv-1",
            email="test@example.com",
            name="Test User",
            role="user",
            expires_at="2026-04-01T00:00:00Z",
            token="abc123",
            invited_by="admin-1",
            valid=True,
        )
        assert invite.id == "inv-1"
        assert invite.token == "abc123"
        assert invite.valid is True
