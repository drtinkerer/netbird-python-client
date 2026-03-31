"""
Unit tests for the NetBird MCP server.
"""

from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("mcp", reason="mcp package not installed (requires Python 3.10+)")


class TestMCPServerImport:
    """Test that the MCP server module imports correctly."""

    def test_server_imports(self):
        from netbird.mcp.server import mcp

        assert mcp is not None

    def test_server_name(self):
        from netbird.mcp.server import mcp

        assert mcp.name == "netbird"

    def test_main_function_exists(self):
        from netbird.mcp.server import main

        assert callable(main)


class TestGetClient:
    """Test the _get_client singleton factory."""

    def setup_method(self):
        import netbird.mcp.server as srv

        srv._client = None

    def test_raises_without_env_vars(self):
        from netbird.mcp.server import _get_client

        with patch.dict("os.environ", {}, clear=True):
            import os

            os.environ.pop("NETBIRD_HOST", None)
            os.environ.pop("NETBIRD_API_TOKEN", None)
            with pytest.raises(ValueError, match="NETBIRD_HOST and NETBIRD_API_TOKEN"):
                _get_client()

    def test_raises_missing_host(self):
        from netbird.mcp.server import _get_client

        with patch.dict("os.environ", {"NETBIRD_API_TOKEN": "tok"}, clear=False):
            import os

            os.environ.pop("NETBIRD_HOST", None)
            import netbird.mcp.server as srv

            srv._client = None
            with pytest.raises(ValueError):
                _get_client()

    def test_raises_missing_token(self):
        from netbird.mcp.server import _get_client

        with patch.dict("os.environ", {"NETBIRD_HOST": "api.netbird.io"}, clear=False):
            import os

            os.environ.pop("NETBIRD_API_TOKEN", None)
            import netbird.mcp.server as srv

            srv._client = None
            with pytest.raises(ValueError):
                _get_client()

    def test_creates_client_with_env_vars(self):
        import netbird.mcp.server as srv

        srv._client = None
        with patch.dict(
            "os.environ",
            {"NETBIRD_HOST": "api.netbird.io", "NETBIRD_API_TOKEN": "test-token"},
        ):
            with patch("netbird.mcp.server.APIClient") as MockClient:
                MockClient.return_value = MagicMock()
                from netbird.mcp.server import _get_client

                client = _get_client()
                MockClient.assert_called_once_with(
                    host="api.netbird.io", api_token="test-token"
                )
                assert client is not None

    def test_singleton_returns_same_client(self):
        import netbird.mcp.server as srv

        srv._client = None
        with patch.dict(
            "os.environ",
            {"NETBIRD_HOST": "api.netbird.io", "NETBIRD_API_TOKEN": "test-token"},
        ):
            with patch("netbird.mcp.server.APIClient") as MockClient:
                mock_instance = MagicMock()
                MockClient.return_value = mock_instance
                from netbird.mcp.server import _get_client

                client1 = _get_client()
                client2 = _get_client()
                assert client1 is client2
                MockClient.assert_called_once()


class TestAccountTools:
    """Test account-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_get_account_returns_first(self):
        from netbird.mcp.server import get_account

        self.mock_client.accounts.list.return_value = [{"id": "acc1"}]
        result = get_account()
        assert result == {"id": "acc1"}

    def test_get_account_empty(self):
        from netbird.mcp.server import get_account

        self.mock_client.accounts.list.return_value = []
        result = get_account()
        assert result == {}


class TestUserTools:
    """Test user-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_get_current_user(self):
        from netbird.mcp.server import get_current_user

        self.mock_client.users.get_current.return_value = {
            "id": "u1",
            "email": "a@b.com",
        }
        result = get_current_user()
        assert result["id"] == "u1"

    def test_list_users(self):
        from netbird.mcp.server import list_users

        self.mock_client.users.list.return_value = [{"id": "u1"}, {"id": "u2"}]
        result = list_users()
        assert len(result) == 2


class TestPeerTools:
    """Test peer-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_peers(self):
        from netbird.mcp.server import list_peers

        self.mock_client.peers.list.return_value = [{"id": "p1"}]
        result = list_peers()
        assert result == [{"id": "p1"}]

    def test_get_peer(self):
        from netbird.mcp.server import get_peer

        self.mock_client.peers.get.return_value = {"id": "p1", "name": "myhost"}
        result = get_peer("p1")
        self.mock_client.peers.get.assert_called_once_with("p1")
        assert result["name"] == "myhost"

    def test_update_peer(self):
        from netbird.mcp.server import update_peer

        self.mock_client.peers.update.return_value = {"id": "p1", "name": "newname"}
        result = update_peer("p1", name="newname")
        assert result["name"] == "newname"
        self.mock_client.peers.update.assert_called_once()

    def test_delete_peer(self):
        from netbird.mcp.server import delete_peer

        result = delete_peer("p1")
        self.mock_client.peers.delete.assert_called_once_with("p1")
        assert result == {"peer_id": "p1", "deleted": True}

    def test_get_peer_accessible_peers(self):
        from netbird.mcp.server import get_peer_accessible_peers

        self.mock_client.peers.get_accessible_peers.return_value = [{"id": "p2"}]
        result = get_peer_accessible_peers("p1")
        self.mock_client.peers.get_accessible_peers.assert_called_once_with("p1")
        assert result == [{"id": "p2"}]


class TestGroupTools:
    """Test group-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_groups(self):
        from netbird.mcp.server import list_groups

        self.mock_client.groups.list.return_value = [{"id": "g1"}]
        result = list_groups()
        assert result == [{"id": "g1"}]

    def test_get_group(self):
        from netbird.mcp.server import get_group

        self.mock_client.groups.get.return_value = {"id": "g1", "name": "All"}
        result = get_group("g1")
        self.mock_client.groups.get.assert_called_once_with("g1")
        assert result["name"] == "All"

    def test_create_group(self):
        from netbird.mcp.server import create_group

        self.mock_client.groups.create.return_value = {"id": "g2", "name": "Dev"}
        result = create_group("Dev", peers=["p1"])
        assert result["name"] == "Dev"
        self.mock_client.groups.create.assert_called_once()

    def test_create_group_no_peers(self):
        from netbird.mcp.server import create_group

        self.mock_client.groups.create.return_value = {"id": "g2", "name": "Dev"}
        result = create_group("Dev")
        assert result["name"] == "Dev"

    def test_update_group(self):
        from netbird.mcp.server import update_group

        self.mock_client.groups.update.return_value = {"id": "g1", "name": "Prod"}
        result = update_group("g1", name="Prod")
        self.mock_client.groups.update.assert_called_once()
        assert result["name"] == "Prod"

    def test_delete_group(self):
        from netbird.mcp.server import delete_group

        result = delete_group("g1")
        self.mock_client.groups.delete.assert_called_once_with("g1")
        assert result == {"group_id": "g1", "deleted": True}


class TestPolicyTools:
    """Test policy-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_policies(self):
        from netbird.mcp.server import list_policies

        self.mock_client.policies.list.return_value = [{"id": "pol1"}]
        result = list_policies()
        assert result == [{"id": "pol1"}]

    def test_create_policy(self):
        from netbird.mcp.server import create_policy

        self.mock_client.policies.create.return_value = {"id": "pol2", "name": "SSH"}
        result = create_policy(
            name="SSH",
            sources=["g1"],
            destinations=["g2"],
            protocol="tcp",
            ports=["22"],
        )
        assert result["name"] == "SSH"
        self.mock_client.policies.create.assert_called_once()

    def test_create_policy_defaults(self):
        from netbird.mcp.server import create_policy

        self.mock_client.policies.create.return_value = {"id": "pol3", "name": "All"}
        result = create_policy(name="All", sources=["g1"], destinations=["g2"])
        assert result["id"] == "pol3"

    def test_delete_policy(self):
        from netbird.mcp.server import delete_policy

        result = delete_policy("pol1")
        self.mock_client.policies.delete.assert_called_once_with("pol1")
        assert result == {"policy_id": "pol1", "deleted": True}


class TestNetworkTools:
    """Test network-related MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_networks(self):
        from netbird.mcp.server import list_networks

        self.mock_client.networks.list.return_value = [{"id": "net1"}]
        result = list_networks()
        assert result == [{"id": "net1"}]

    def test_get_network(self):
        from netbird.mcp.server import get_network

        self.mock_client.networks.get.return_value = {"id": "net1", "name": "Corp"}
        self.mock_client.networks.list_resources.return_value = []
        self.mock_client.networks.list_routers.return_value = []
        result = get_network("net1")
        assert result["name"] == "Corp"
        assert "resources" in result
        assert "routers" in result


class TestSetupKeyTools:
    """Test setup key MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_setup_keys(self):
        from netbird.mcp.server import list_setup_keys

        self.mock_client.setup_keys.list.return_value = [{"id": "sk1"}]
        result = list_setup_keys()
        assert result == [{"id": "sk1"}]

    def test_create_setup_key(self):
        from netbird.mcp.server import create_setup_key

        self.mock_client.setup_keys.create.return_value = {"id": "sk2", "key": "abc"}
        result = create_setup_key("enrollment-key")
        assert result["id"] == "sk2"
        self.mock_client.setup_keys.create.assert_called_once()

    def test_create_setup_key_with_groups(self):
        from netbird.mcp.server import create_setup_key

        self.mock_client.setup_keys.create.return_value = {"id": "sk3"}
        result = create_setup_key(
            "dev-key",
            key_type="one-off",
            expires_in=3600,
            auto_groups=["g1", "g2"],
            ephemeral=True,
        )
        assert result["id"] == "sk3"


class TestDNSTools:
    """Test DNS MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_nameservers(self):
        from netbird.mcp.server import list_nameservers

        self.mock_client.dns.list_nameserver_groups.return_value = [{"id": "ns1"}]
        result = list_nameservers()
        assert result == [{"id": "ns1"}]

    def test_get_dns_settings(self):
        from netbird.mcp.server import get_dns_settings

        self.mock_client.dns.get_settings.return_value = {"items": []}
        result = get_dns_settings()
        assert "items" in result


class TestPostureAndEventsTools:
    """Test posture checks and events MCP tools."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_list_posture_checks(self):
        from netbird.mcp.server import list_posture_checks

        self.mock_client.posture_checks.list.return_value = [{"id": "pc1"}]
        result = list_posture_checks()
        assert result == [{"id": "pc1"}]

    def test_get_audit_events(self):
        from netbird.mcp.server import get_audit_events

        self.mock_client.events.get_audit_events.return_value = [{"id": "ev1"}]
        result = get_audit_events()
        assert result == [{"id": "ev1"}]


class TestDiagramTool:
    """Test network diagram generation MCP tool."""

    def setup_method(self):
        import netbird.mcp.server as srv

        self.mock_client = MagicMock()
        srv._client = self.mock_client

    def test_generate_diagram_mermaid(self):
        from netbird.mcp.server import generate_network_diagram

        self.mock_client.generate_diagram.return_value = "graph TD\n  A --> B"
        result = generate_network_diagram()
        self.mock_client.generate_diagram.assert_called_once_with(format="mermaid")
        assert "graph" in result

    def test_generate_diagram_empty(self):
        from netbird.mcp.server import generate_network_diagram

        self.mock_client.generate_diagram.return_value = None
        result = generate_network_diagram()
        assert result == "No diagram generated."

    def test_generate_diagram_graphviz(self):
        from netbird.mcp.server import generate_network_diagram

        self.mock_client.generate_diagram.return_value = "digraph G {}"
        result = generate_network_diagram(format="graphviz")
        self.mock_client.generate_diagram.assert_called_once_with(format="graphviz")
