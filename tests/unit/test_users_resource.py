"""
Unit tests for UsersResource.
"""

from unittest.mock import MagicMock

import pytest

from netbird.models import UserCreate, UserInviteCreate, UserUpdate
from netbird.resources.users import UsersResource


@pytest.mark.unit
class TestUsersResource:
    """Test cases for UsersResource methods."""

    def setup_method(self):
        self.mock_client = MagicMock()
        self.resource = UsersResource(self.mock_client)

    # --- Existing CRUD ---

    def test_list(self):
        self.mock_client.get.return_value = [
            {"id": "user-1", "email": "alice@example.com"},
            {"id": "user-2", "email": "bob@example.com"},
        ]
        result = self.resource.list()
        self.mock_client.get.assert_called_once_with("users")
        assert len(result) == 2
        assert result[0]["id"] == "user-1"

    def test_create(self):
        user_data = UserCreate(email="alice@example.com", role="user")
        self.mock_client.post.return_value = {
            "id": "user-1",
            "email": "alice@example.com",
        }
        result = self.resource.create(user_data)
        self.mock_client.post.assert_called_once_with(
            "users", data=user_data.model_dump(exclude_unset=True)
        )
        assert result["id"] == "user-1"

    def test_get(self):
        self.mock_client.get.return_value = {
            "id": "user-1",
            "email": "alice@example.com",
        }
        result = self.resource.get("user-1")
        self.mock_client.get.assert_called_once_with("users/user-1")
        assert result["email"] == "alice@example.com"

    def test_update(self):
        user_data = UserUpdate(name="Alice Smith")
        self.mock_client.put.return_value = {
            "id": "user-1",
            "name": "Alice Smith",
        }
        result = self.resource.update("user-1", user_data)
        self.mock_client.put.assert_called_once_with(
            "users/user-1", data=user_data.model_dump(exclude_unset=True)
        )
        assert result["name"] == "Alice Smith"

    def test_delete(self):
        self.resource.delete("user-1")
        self.mock_client.delete.assert_called_once_with("users/user-1")

    # --- New methods ---

    def test_approve(self):
        self.mock_client.post.return_value = {"id": "user-1", "status": "active"}
        result = self.resource.approve("user-1")
        self.mock_client.post.assert_called_once_with("users/user-1/approve")
        assert result["status"] == "active"

    def test_reject(self):
        self.resource.reject("user-1")
        self.mock_client.delete.assert_called_once_with("users/user-1/reject")

    def test_change_password(self):
        self.resource.change_password("user-1", "old-pass", "new-pass")
        self.mock_client.put.assert_called_once_with(
            "users/user-1/password",
            data={"old_password": "old-pass", "new_password": "new-pass"},
        )

    # --- Invite methods ---

    def test_list_invites(self):
        self.mock_client.get.return_value = [
            {"id": "invite-1", "email": "new@example.com"}
        ]
        result = self.resource.list_invites()
        self.mock_client.get.assert_called_once_with("users/invites")
        assert len(result) == 1

    def test_create_invite(self):
        invite_data = UserInviteCreate(
            email="new@example.com",
            name="New User",
            role="user",
            auto_groups=["group-1"],
        )
        self.mock_client.post.return_value = {
            "id": "invite-1",
            "email": "new@example.com",
            "token": "abc123",
        }
        result = self.resource.create_invite(invite_data)
        self.mock_client.post.assert_called_once_with(
            "users/invites", data=invite_data.model_dump(exclude_unset=True)
        )
        assert result["token"] == "abc123"

    def test_delete_invite(self):
        self.resource.delete_invite("invite-1")
        self.mock_client.delete.assert_called_once_with("users/invites/invite-1")

    def test_regenerate_invite(self):
        self.mock_client.post.return_value = {
            "id": "invite-1",
            "token": "new-token",
        }
        result = self.resource.regenerate_invite("invite-1", expires_in=3600)
        self.mock_client.post.assert_called_once_with(
            "users/invites/invite-1/regenerate", data={"expires_in": 3600}
        )
        assert result["token"] == "new-token"

    def test_regenerate_invite_no_expiry(self):
        self.mock_client.post.return_value = {
            "id": "invite-1",
            "token": "new-token",
        }
        result = self.resource.regenerate_invite("invite-1")
        self.mock_client.post.assert_called_once_with(
            "users/invites/invite-1/regenerate", data=None
        )
        assert result["token"] == "new-token"

    def test_get_invite_info(self):
        self.mock_client.get.return_value = {
            "email": "new@example.com",
            "name": "New User",
        }
        result = self.resource.get_invite_info("abc123")
        self.mock_client.get.assert_called_once_with("users/invites/abc123")
        assert result["email"] == "new@example.com"

    def test_accept_invite(self):
        self.mock_client.post.return_value = {"status": "accepted"}
        result = self.resource.accept_invite("abc123", "my-password")
        self.mock_client.post.assert_called_once_with(
            "users/invites/abc123/accept", data={"password": "my-password"}
        )
        assert result["status"] == "accepted"

    def test_invite(self):
        self.resource.invite("user-1")
        self.mock_client.post.assert_called_once_with("users/user-1/invite")

    def test_get_current(self):
        self.mock_client.get.return_value = {
            "id": "user-1",
            "is_current": True,
        }
        result = self.resource.get_current()
        self.mock_client.get.assert_called_once_with("users/current")
        assert result["is_current"] is True
