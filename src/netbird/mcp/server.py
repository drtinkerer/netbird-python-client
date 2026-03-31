"""
NetBird MCP Server

Exposes 25 NetBird management tools via the Model Context Protocol.

Configuration (environment variables):
    NETBIRD_HOST       - NetBird API host (e.g. api.netbird.io)
    NETBIRD_API_TOKEN  - Personal Access Token
"""

import os
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(
        "The 'mcp' package is required to use the NetBird MCP server. "
        "Install it with: pip install 'netbird[mcp]' (requires Python 3.10+)"
    ) from e

from netbird import APIClient

mcp = FastMCP("netbird")

# --- Client singleton ---

_client: Optional[APIClient] = None


def _get_client() -> APIClient:
    global _client
    if _client is None:
        host = os.environ.get("NETBIRD_HOST")
        token = os.environ.get("NETBIRD_API_TOKEN")
        if not host or not token:
            raise ValueError(
                "NETBIRD_HOST and NETBIRD_API_TOKEN environment variables are required."
            )
        _client = APIClient(host=host, api_token=token)
    return _client


# --- Account tools ---


@mcp.tool()
def get_account() -> dict:
    """Get the current NetBird account settings and configuration."""
    client = _get_client()
    accounts = client.accounts.list()
    return accounts[0] if accounts else {}


# --- User tools ---


@mcp.tool()
def get_current_user() -> dict:
    """Get the currently authenticated user's profile and permissions."""
    client = _get_client()
    return client.users.get_current()


@mcp.tool()
def list_users() -> list:
    """List all users in the NetBird account."""
    client = _get_client()
    return client.users.list()


# --- Peer tools ---


@mcp.tool()
def list_peers() -> list:
    """List all peers in the network with their connection status and IP addresses."""
    client = _get_client()
    return client.peers.list()


@mcp.tool()
def get_peer(peer_id: str) -> dict:
    """Get details of a specific peer by ID.

    Args:
        peer_id: The peer ID.
    """
    client = _get_client()
    return client.peers.get(peer_id)


@mcp.tool()
def update_peer(
    peer_id: str,
    name: Optional[str] = None,
    ssh_enabled: Optional[bool] = None,
    login_expiration_enabled: Optional[bool] = None,
) -> dict:
    """Update a peer's settings.

    Args:
        peer_id: The peer ID.
        name: New peer name.
        ssh_enabled: Enable or disable SSH access.
        login_expiration_enabled: Enable or disable login expiration.
    """
    from netbird.models import PeerUpdate

    client = _get_client()
    data = PeerUpdate(
        name=name,
        ssh_enabled=ssh_enabled,
        login_expiration_enabled=login_expiration_enabled,
    )
    return client.peers.update(peer_id, data)


@mcp.tool()
def delete_peer(peer_id: str) -> dict:
    """Remove a peer from the network.

    Args:
        peer_id: The peer ID to remove.
    """
    client = _get_client()
    client.peers.delete(peer_id)
    return {"peer_id": peer_id, "deleted": True}


@mcp.tool()
def get_peer_accessible_peers(peer_id: str) -> list:
    """List all peers that a given peer can access based on current policies.

    Args:
        peer_id: The peer ID to check accessibility for.
    """
    client = _get_client()
    return client.peers.get_accessible_peers(peer_id)


# --- Group tools ---


@mcp.tool()
def list_groups() -> list:
    """List all peer groups with their member counts."""
    client = _get_client()
    return client.groups.list()


@mcp.tool()
def get_group(group_id: str) -> dict:
    """Get details of a specific group including its members.

    Args:
        group_id: The group ID.
    """
    client = _get_client()
    return client.groups.get(group_id)


@mcp.tool()
def create_group(name: str, peers: Optional[list] = None) -> dict:
    """Create a new peer group.

    Args:
        name: Group name.
        peers: Optional list of peer IDs to add to the group.
    """
    from netbird.models import GroupCreate

    client = _get_client()
    return client.groups.create(GroupCreate(name=name, peers=peers or []))


@mcp.tool()
def update_group(
    group_id: str,
    name: Optional[str] = None,
    peers: Optional[list] = None,
) -> dict:
    """Update a group's name or members.

    Args:
        group_id: The group ID.
        name: New group name.
        peers: New list of peer IDs (replaces existing members).
    """
    from netbird.models import GroupUpdate

    client = _get_client()
    return client.groups.update(group_id, GroupUpdate(name=name, peers=peers))


@mcp.tool()
def delete_group(group_id: str) -> dict:
    """Delete a peer group.

    Args:
        group_id: The group ID to delete.
    """
    client = _get_client()
    client.groups.delete(group_id)
    return {"group_id": group_id, "deleted": True}


# --- Policy tools ---


@mcp.tool()
def list_policies() -> list:
    """List all access control policies with their rules."""
    client = _get_client()
    return client.policies.list()


@mcp.tool()
def create_policy(
    name: str,
    sources: list,
    destinations: list,
    protocol: str = "all",
    action: str = "accept",
    bidirectional: bool = True,
    ports: Optional[list] = None,
    description: Optional[str] = None,
) -> dict:
    """Create a new access control policy.

    Args:
        name: Policy name.
        sources: List of source group IDs.
        destinations: List of destination group IDs.
        protocol: Network protocol - "all", "tcp", "udp", or "icmp".
        action: Policy action - "accept" or "drop".
        bidirectional: Whether the rule applies in both directions.
        ports: Optional list of port numbers as strings (e.g. ["22", "443"]).
        description: Optional policy description.
    """
    from netbird.models import PolicyCreate, PolicyRule

    client = _get_client()
    rule = PolicyRule(
        name=name,
        action=action,
        protocol=protocol,
        sources=sources,
        destinations=destinations,
        bidirectional=bidirectional,
        ports=ports,
        enabled=True,
    )
    return client.policies.create(
        PolicyCreate(name=name, description=description, rules=[rule], enabled=True)
    )


@mcp.tool()
def delete_policy(policy_id: str) -> dict:
    """Delete an access control policy.

    Args:
        policy_id: The policy ID to delete.
    """
    client = _get_client()
    client.policies.delete(policy_id)
    return {"policy_id": policy_id, "deleted": True}


# --- Network tools ---


@mcp.tool()
def list_networks() -> list:
    """List all networks with their resources and routers."""
    client = _get_client()
    return client.networks.list()


@mcp.tool()
def get_network(network_id: str) -> dict:
    """Get details of a specific network including resources and routers.

    Args:
        network_id: The network ID.
    """
    client = _get_client()
    network = client.networks.get(network_id)
    network["resources"] = client.networks.list_resources(network_id)
    network["routers"] = client.networks.list_routers(network_id)
    return network


# --- Setup Key tools ---


@mcp.tool()
def list_setup_keys() -> list:
    """List all setup keys with their validity and usage stats."""
    client = _get_client()
    return client.setup_keys.list()


@mcp.tool()
def create_setup_key(
    name: str,
    key_type: str = "reusable",
    expires_in: int = 86400,
    auto_groups: Optional[list] = None,
    usage_limit: Optional[int] = None,
    ephemeral: bool = False,
) -> dict:
    """Create a new setup key for enrolling peers.

    Args:
        name: Setup key name.
        key_type: "reusable" or "one-off".
        expires_in: Expiration in seconds (default 86400 = 24h).
        auto_groups: Group IDs to auto-assign enrolled peers to.
        usage_limit: Maximum number of uses (reusable keys only).
        ephemeral: If True, peers enrolled with this key are ephemeral.
    """
    from netbird.models import SetupKeyCreate

    client = _get_client()
    return client.setup_keys.create(
        SetupKeyCreate(
            name=name,
            type=key_type,
            expires_in=expires_in,
            auto_groups=auto_groups or [],
            usage_limit=usage_limit,
            ephemeral=ephemeral,
        )
    )


# --- DNS tools ---


@mcp.tool()
def list_nameservers() -> list:
    """List all DNS nameserver groups."""
    client = _get_client()
    return client.dns.list_nameserver_groups()


@mcp.tool()
def get_dns_settings() -> dict:
    """Get the global DNS settings for the account."""
    client = _get_client()
    return client.dns.get_settings()


# --- Posture check tools ---


@mcp.tool()
def list_posture_checks() -> list:
    """List all device posture checks (compliance policies)."""
    client = _get_client()
    return client.posture_checks.list()


# --- Events tools ---


@mcp.tool()
def get_audit_events() -> list:
    """Get recent audit log events showing account activity."""
    client = _get_client()
    return client.events.get_audit_events()


# --- Diagram tool ---


@mcp.tool()
def generate_network_diagram(format: str = "mermaid") -> str:
    """Generate a network topology diagram.

    Args:
        format: Diagram format - "mermaid" (default), "graphviz", or "diagrams".
                Use "mermaid" for text output (GitHub/GitLab compatible).
    """
    client = _get_client()
    result = client.generate_diagram(format=format)
    return result or "No diagram generated."


# --- Entry point ---


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
