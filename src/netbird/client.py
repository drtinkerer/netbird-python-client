"""
NetBird API Client

Core client implementation for the NetBird API.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from httpx import Response

from .auth import TokenAuth

if TYPE_CHECKING:
    from .resources.accounts import AccountsResource
    from .resources.users import UsersResource
    from .resources.tokens import TokensResource
    from .resources.peers import PeersResource
    from .resources.setup_keys import SetupKeysResource
    from .resources.groups import GroupsResource
    from .resources.networks import NetworksResource
    from .resources.policies import PoliciesResource
    from .resources.routes import RoutesResource
    from .resources.dns import DNSResource
    from .resources.events import EventsResource

from .exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)


class APIClient:
    """NetBird API Client.

    Provides access to all NetBird API resources including users, peers, groups,
    networks, policies, routes, DNS settings, and events.

    Args:
        host: NetBird API host (e.g., 'api.netbird.io' or 'your-domain.com')
        api_token: API token for authentication
        use_ssl: Whether to use HTTPS (default: True)
        timeout: Request timeout in seconds (default: 30)
        base_path: API base path (default: '/api')

    Example:
        >>> client = APIClient(host="api.netbird.io", api_token="your-token")
        >>> peers = client.peers.list()
        >>> users = client.users.list()

        # For self-hosted instances
        >>> client = APIClient(
        ...     host="netbird.yourcompany.com:33073",
        ...     api_token="your-token"
        ... )
    """

    def __init__(
        self,
        host: str,
        api_token: str,
        use_ssl: bool = True,
        timeout: float = 30.0,
        base_path: str = "/api",
    ) -> None:
        self.host = host.strip().rstrip("/")
        self.base_path = base_path.strip()
        self.use_ssl = use_ssl
        self.timeout = timeout

        # Build base URL - if host already has protocol, use as-is
        if self.host.startswith(("http://", "https://")):
            self.base_url = f"{self.host}{self.base_path}"
        else:
            scheme = "https" if use_ssl else "http"
            self.base_url = f"{scheme}://{self.host}{self.base_path}"

        # Set up authentication
        self.auth = TokenAuth(api_token)

        # Create HTTP client
        self.client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                **self.auth.get_auth_headers(),
            },
        )

        # Lazy-load resource handlers
        self._accounts: Optional["AccountsResource"] = None
        self._users: Optional["UsersResource"] = None
        self._tokens: Optional["TokensResource"] = None
        self._peers: Optional["PeersResource"] = None
        self._setup_keys: Optional["SetupKeysResource"] = None
        self._groups: Optional["GroupsResource"] = None
        self._networks: Optional["NetworksResource"] = None
        self._policies: Optional["PoliciesResource"] = None
        self._routes: Optional["RoutesResource"] = None
        self._dns: Optional["DNSResource"] = None
        self._events: Optional["EventsResource"] = None

    @property
    def accounts(self) -> "AccountsResource":
        """Access to accounts API endpoints."""
        if self._accounts is None:
            from .resources.accounts import AccountsResource

            self._accounts = AccountsResource(self)
        return self._accounts

    @property
    def users(self) -> "UsersResource":
        """Access to users API endpoints."""
        if self._users is None:
            from .resources.users import UsersResource

            self._users = UsersResource(self)
        return self._users

    @property
    def tokens(self) -> "TokensResource":
        """Access to tokens API endpoints."""
        if self._tokens is None:
            from .resources.tokens import TokensResource

            self._tokens = TokensResource(self)
        return self._tokens

    @property
    def peers(self) -> "PeersResource":
        """Access to peers API endpoints."""
        if self._peers is None:
            from .resources.peers import PeersResource

            self._peers = PeersResource(self)
        return self._peers

    @property
    def setup_keys(self) -> "SetupKeysResource":
        """Access to setup keys API endpoints."""
        if self._setup_keys is None:
            from .resources.setup_keys import SetupKeysResource

            self._setup_keys = SetupKeysResource(self)
        return self._setup_keys

    @property
    def groups(self) -> "GroupsResource":
        """Access to groups API endpoints."""
        if self._groups is None:
            from .resources.groups import GroupsResource

            self._groups = GroupsResource(self)
        return self._groups

    @property
    def networks(self) -> "NetworksResource":
        """Access to networks API endpoints."""
        if self._networks is None:
            from .resources.networks import NetworksResource

            self._networks = NetworksResource(self)
        return self._networks

    @property
    def policies(self) -> "PoliciesResource":
        """Access to policies API endpoints."""
        if self._policies is None:
            from .resources.policies import PoliciesResource

            self._policies = PoliciesResource(self)
        return self._policies

    @property
    def routes(self) -> "RoutesResource":
        """Access to routes API endpoints."""
        if self._routes is None:
            from .resources.routes import RoutesResource

            self._routes = RoutesResource(self)
        return self._routes

    @property
    def dns(self) -> "DNSResource":
        """Access to DNS API endpoints."""
        if self._dns is None:
            from .resources.dns import DNSResource

            self._dns = DNSResource(self)
        return self._dns

    @property
    def events(self) -> "EventsResource":
        """Access to events API endpoints."""
        if self._events is None:
            from .resources.events import EventsResource

            self._events = EventsResource(self)
        return self._events

    def _build_url(self, path: str) -> str:
        """Build full URL from path."""
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _handle_response(self, response: Response) -> Any:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            data = response.json() if response.content else {}
        except ValueError:
            data = {"error": "Invalid JSON response"}

        if response.is_success:
            return data

        # Extract error message
        error_msg = (
            data.get("message") or data.get("error") or f"HTTP {response.status_code}"
        )

        # Map status codes to exceptions
        if response.status_code in [400, 409, 422]:
            raise NetBirdValidationError(error_msg, response.status_code, data)
        elif response.status_code == 401:
            raise NetBirdAuthenticationError(error_msg, response.status_code, data)
        elif response.status_code == 404:
            raise NetBirdNotFoundError(error_msg, response.status_code, data)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            raise NetBirdRateLimitError(
                error_msg, response.status_code, data, retry_seconds
            )
        elif response.status_code >= 500:
            raise NetBirdServerError(error_msg, response.status_code, data)
        else:
            raise NetBirdAPIError(error_msg, response.status_code, data)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.get(url, params=params)
        return self._handle_response(response)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a POST request.

        Args:
            path: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.post(url, json=data, params=params)
        return self._handle_response(response)

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a PUT request.

        Args:
            path: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.put(url, json=data, params=params)
        return self._handle_response(response)

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a DELETE request.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.delete(url, params=params)
        return self._handle_response(response)

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self) -> "APIClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    def generate_diagram(
        self,
        format: str = "mermaid",
        output_file: Optional[str] = None,
        include_routers: bool = True,
        include_policies: bool = True,
        include_resources: bool = True,
    ) -> Union[str, None]:
        """Generate network topology diagram in various formats.

        Args:
            format: Diagram format ('mermaid', 'graphviz', 'diagrams')
            output_file: Output filename (without extension)
            include_routers: Whether to include routers in the diagram
            include_policies: Whether to include policies in the diagram
            include_resources: Whether to include resources in the diagram

        Returns:
            For mermaid: Returns mermaid syntax as string
            For graphviz: Returns None (saves files directly)
            For diagrams: Returns output filename

        Example:
            >>> mermaid_content = client.generate_diagram(format="mermaid")
            >>> client.generate_diagram(format="graphviz", output_file="my_network")
            >>> client.generate_diagram(format="diagrams")
        """

        # Get enriched network data
        from .network_map import generate_full_network_map

        networks = generate_full_network_map(
            self, include_routers, include_policies, include_resources
        )

        if not networks:
            print("❌ No networks found.")
            return None

        if format == "mermaid":
            return self._create_mermaid_diagram(networks, output_file)
        elif format == "graphviz":
            return self._create_graphviz_diagram(networks, output_file)
        elif format == "diagrams":
            return self._create_diagrams_diagram(networks, output_file)
        else:
            raise ValueError(
                f"Unsupported format: {format}. "
                f"Use 'mermaid', 'graphviz', or 'diagrams'"
            )

    def _get_source_group_colors(self, source_groups: List[str]) -> Dict[str, str]:
        """Generate color mapping for source groups dynamically."""
        DEFAULT_COLORS = [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FECA57",
            "#FF9FF3",
            "#A8E6CF",
            "#FFD93D",
            "#6BCF7F",
            "#4D96FF",
            "#9B59B6",
            "#E67E22",
            "#1ABC9C",
            "#E74C3C",
        ]

        source_group_colors = {}
        sorted_groups = sorted(source_groups)

        for i, group_name in enumerate(sorted_groups):
            color_index = i % len(DEFAULT_COLORS)
            source_group_colors[group_name] = DEFAULT_COLORS[color_index]

        return source_group_colors

    def _format_policy_label(
        self, policy_names: List[str], connection_type: str = "Group"
    ) -> str:
        """Format policy labels for better readability."""
        unique_policies = list(set(policy_names))
        if len(unique_policies) <= 2:
            return f"{connection_type}: {', '.join(unique_policies)}"
        else:
            return f"{connection_type}: {len(unique_policies)} policies"

    def _sanitize_id(self, name: str) -> str:
        """Sanitize node ID for various diagram formats."""
        import re

        # Replace any non-alphanumeric character (except underscore) with underscore
        return re.sub(r"[^a-zA-Z0-9_]", "_", name)

    def _create_mermaid_diagram(
        self, networks: List[Dict[str, Any]], output_file: Optional[str] = None
    ) -> str:
        """Create a network diagram using Mermaid syntax with optimized connections."""

        mermaid_lines = ["graph LR"]

        # Get optimized connections
        from .network_map import get_network_topology_data

        connections_data = get_network_topology_data(self, optimize_connections=True)

        # Create source groups subgraph
        mermaid_lines.append('    subgraph SG["Source Groups"]')
        for source_group in sorted(connections_data["all_source_groups"]):
            safe_id = f"src_{self._sanitize_id(source_group)}"
            mermaid_lines.append(f'        {safe_id}["👥 {source_group}"]')
        mermaid_lines.append("    end")

        # Create networks subgraphs
        for network_idx, network in enumerate(networks):
            network_name = network["name"]
            resources = network.get("resources", [])
            routers = network.get("routers", [])

            mermaid_lines.append(f'    subgraph N{network_idx}["🌐 {network_name}"]')

            # Add resources
            for res_idx, resource in enumerate(resources):
                resource_name = resource.get("name", "Unknown")
                resource_address = resource.get("address", "N/A")
                resource_type = resource.get("type", "unknown")
                resource_groups = resource.get("groups", [])

                icon = (
                    "🖥️"
                    if resource_type == "host"
                    else "🌐" if resource_type == "subnet" else "📁"
                )
                resource_node_name = f"res_{network_idx}_{res_idx}"
                resource_label = f"{icon} {resource_name}<br/>{resource_address}"

                if resource_groups:
                    group_names = []
                    for group in resource_groups:
                        if isinstance(group, dict):
                            group_name = (
                                group.get("name") or group.get("id") or "Unknown"
                            )
                            group_names.append(str(group_name))
                        else:
                            group_names.append(str(group))
                    resource_label += f"<br/>🏷️ {', '.join(group_names)}"

                mermaid_lines.append(
                    f'        {resource_node_name}["{resource_label}"]'
                )

            # Add routers
            for router_idx, router in enumerate(routers):
                router_name = router.get("name", "Unknown Router")
                router_node_name = f"router_{network_idx}_{router_idx}"
                mermaid_lines.append(f'        {router_node_name}["🔀 {router_name}"]')

            mermaid_lines.append("    end")

        # Generate dynamic color mapping
        source_group_colors = self._get_source_group_colors(
            list(connections_data["all_source_groups"])
        )

        # Create optimized group connections
        for (source_name, dest_group_name), policy_names in connections_data[
            "group_connections"
        ].items():
            if dest_group_name in connections_data["group_name_to_nodes"]:
                safe_source = f"src_{self._sanitize_id(source_name)}"
                merged_label = self._format_policy_label(policy_names, "Group")

                for resource_node in connections_data["group_name_to_nodes"][
                    dest_group_name
                ]:
                    mermaid_lines.append(
                        f'    {safe_source} -.->|"{merged_label}"| {resource_node}'
                    )

        # Create optimized direct connections
        for (source_name, dest_node), policy_names in connections_data[
            "direct_connections"
        ].items():
            safe_source = f"src_{self._sanitize_id(source_name)}"
            merged_label = self._format_policy_label(policy_names, "Direct")
            mermaid_lines.append(f'    {safe_source} -->|"{merged_label}"| {dest_node}')

        # Add styling
        mermaid_lines.append("")
        mermaid_lines.append("    %% Styling")

        # Style source groups with dynamic colors
        for source_group in sorted(connections_data["all_source_groups"]):
            safe_id = f"src_{self._sanitize_id(source_group)}"
            color = source_group_colors.get(source_group, "#FF6B6B")
            mermaid_lines.append(
                f"    classDef {safe_id}_style "
                f"fill:{color},stroke:#333,stroke-width:2px,color:#000"
            )
            mermaid_lines.append(f"    class {safe_id} {safe_id}_style")

        # Style networks
        for network_idx, network in enumerate(networks):
            mermaid_lines.append(
                f"    classDef network{network_idx}_style "
                f"fill:#E1F5FE,stroke:#0277BD,stroke-width:2px"
            )
            resources = network.get("resources", [])
            routers = network.get("routers", [])

            for res_idx, resource in enumerate(resources):
                resource_node_name = f"res_{network_idx}_{res_idx}"
                mermaid_lines.append(
                    f"    class {resource_node_name} network{network_idx}_style"
                )

            for router_idx, router in enumerate(routers):
                router_node_name = f"router_{network_idx}_{router_idx}"
                mermaid_lines.append(
                    f"    class {router_node_name} network{network_idx}_style"
                )

        mermaid_content = "\n".join(mermaid_lines)

        # Save files if output_file specified
        if output_file:
            mermaid_file = f"{output_file}.mmd"
            with open(mermaid_file, "w") as f:
                f.write(mermaid_content)
            print(f"✅ Mermaid diagram saved as {mermaid_file}")

            # Also save as markdown file
            markdown_file = f"{output_file}.md"
            with open(markdown_file, "w") as f:
                f.write("# NetBird Network Topology\n\n")
                f.write("```mermaid\n")
                f.write(mermaid_content)
                f.write("\n```\n")
            print(f"✅ Markdown file saved as {markdown_file}")

        return mermaid_content

    def _create_graphviz_diagram(
        self, networks: List[Dict[str, Any]], output_file: Optional[str] = None
    ) -> Optional[str]:
        """Create a network diagram using Graphviz with optimized connections."""
        try:
            import graphviz  # type: ignore[import-untyped]
        except ImportError:
            print("❌ Error: graphviz library not installed. Run: pip install graphviz")
            return None

        # Get optimized connections
        from .network_map import get_network_topology_data

        connections_data = get_network_topology_data(self, optimize_connections=True)

        # Create a new directed graph
        dot = graphviz.Digraph("NetBird_Networks", comment="NetBird Network Topology")
        dot.attr(rankdir="LR", splines="ortho", nodesep="2.0", ranksep="3.0")
        dot.attr(
            "graph", bgcolor="white", fontname="Arial", fontsize="16", compound="true"
        )
        dot.attr("node", fontname="Arial", fontsize="12")
        dot.attr("edge", fontname="Arial", fontsize="10")

        # Create source groups subgraph
        with dot.subgraph(name="cluster_sources") as sources_graph:
            sources_graph.attr(
                label="Source Groups",
                style="filled",
                fillcolor="lightblue",
                fontsize="14",
                fontweight="bold",
            )

            for source_group in sorted(connections_data["all_source_groups"]):
                sources_graph.node(
                    f"src_{source_group}",
                    label=f"👥 {source_group}",
                    shape="box",
                    style="filled,rounded",
                    fillcolor="#FFE4E1",
                    color="#CD5C5C",
                    penwidth="2",
                )

        # Create networks subgraphs
        for network_idx, network in enumerate(networks):
            network_name = network["name"]
            resources = network.get("resources", [])
            routers = network.get("routers", [])

            with dot.subgraph(name=f"cluster_network_{network_idx}") as net_graph:
                net_graph.attr(
                    label=f"🌐 {network_name}",
                    style="filled",
                    fillcolor="lightcyan",
                    fontsize="14",
                    fontweight="bold",
                    color="blue",
                    penwidth="2",
                )

                # Add resources
                for res_idx, resource in enumerate(resources):
                    resource_name = resource.get("name", "Unknown")
                    resource_address = resource.get("address", "N/A")
                    resource_type = resource.get("type", "unknown")
                    resource_groups = resource.get("groups", [])

                    icon = (
                        "🖥️"
                        if resource_type == "host"
                        else "🌐" if resource_type == "subnet" else "📁"
                    )
                    resource_node_name = f"res_{network_idx}_{res_idx}"
                    resource_label = (
                        f"{icon} {resource_name}\\\\\\\\n{resource_address}"
                    )

                    if resource_groups:
                        group_names = []
                        for group in resource_groups:
                            if isinstance(group, dict):
                                group_name = (
                                    group.get("name") or group.get("id") or "Unknown"
                                )
                                group_names.append(str(group_name))
                            else:
                                group_names.append(str(group))
                        resource_label += f'\\\\\\\\n🏷️ {", ".join(group_names)}'

                    net_graph.node(
                        resource_node_name,
                        label=resource_label,
                        shape="box",
                        style="filled,rounded",
                        fillcolor="#FFFACD",
                        color="#DAA520",
                        penwidth="2",
                    )

                # Add routers
                for router_idx, router in enumerate(routers):
                    router_name = router.get("name", "Unknown Router")
                    router_node_name = f"router_{network_idx}_{router_idx}"

                    net_graph.node(
                        router_node_name,
                        label=f"🔀 {router_name}",
                        shape="box",
                        style="filled,rounded",
                        fillcolor="#FFFACD",
                        color="#DAA520",
                        penwidth="2",
                    )

        # Generate dynamic color mapping
        source_group_colors = self._get_source_group_colors(
            list(connections_data["all_source_groups"])
        )

        # Create optimized group connections
        for (source_name, dest_group_name), policy_names in connections_data[
            "group_connections"
        ].items():
            if dest_group_name in connections_data["group_name_to_nodes"]:
                color = source_group_colors.get(source_name, "#FF6B6B")
                merged_label = self._format_policy_label(policy_names, "Group")

                for resource_node in connections_data["group_name_to_nodes"][
                    dest_group_name
                ]:
                    dot.edge(
                        f"src_{source_name}",
                        resource_node,
                        label=merged_label,
                        color=color,
                        style="dashed",
                        penwidth="2",
                    )

        # Create optimized direct connections
        for (source_name, dest_node), policy_names in connections_data[
            "direct_connections"
        ].items():
            color = source_group_colors.get(source_name, "#FF6B6B")
            merged_label = self._format_policy_label(policy_names, "Direct")

            dot.edge(
                f"src_{source_name}",
                dest_node,
                label=merged_label,
                color=color,
                style="solid",
                penwidth="3",
            )

        # Save files
        output_base = output_file or "netbird_networks_unified_graphviz"

        # Save multiple formats
        dot.render(output_base, format="png", cleanup=True)
        print(f"✅ PNG diagram saved as {output_base}.png")

        dot.render(f"{output_base}_svg", format="svg", cleanup=True)
        print(f"✅ SVG diagram saved as {output_base}_svg.svg")

        dot.render(f"{output_base}_pdf", format="pdf", cleanup=True)
        print(f"✅ PDF diagram saved as {output_base}_pdf.pdf")

        # Save DOT source
        with open(f"{output_base}.dot", "w") as f:
            f.write(dot.source)
        print(f"✅ DOT source saved as {output_base}.dot")

        return None

    def _create_diagrams_diagram(
        self, networks: List[Dict[str, Any]], output_file: Optional[str] = None
    ) -> Optional[str]:
        """Create a network diagram using Python Diagrams with optimized connections."""
        try:
            from diagrams import (  # type: ignore[import-untyped]
                Cluster,
                Diagram,
                Edge,
            )
            from diagrams.generic.network import Router  # type: ignore[import-untyped]
            from diagrams.onprem.network import Internet  # type: ignore[import-untyped]
        except ImportError:
            print("❌ Error: diagrams library not installed. Run: pip install diagrams")
            return None

        # Get optimized connections
        from .network_map import get_network_topology_data

        connections_data = get_network_topology_data(self, optimize_connections=True)

        diagram_name = output_file or "netbird_network_topology"

        with Diagram(
            diagram_name,
            show=False,
            direction="LR",
            graph_attr={"splines": "ortho", "nodesep": "2.0", "ranksep": "3.0"},
        ):

            # Create source groups
            source_group_nodes = {}
            with Cluster("Source Groups"):
                for source_group in sorted(connections_data["all_source_groups"]):
                    source_group_nodes[source_group] = Internet(f"👥 {source_group}")

            # Create networks
            network_resource_nodes = {}
            for network_idx, network in enumerate(networks):
                network_name = network["name"]
                resources = network.get("resources", [])
                routers = network.get("routers", [])

                with Cluster(f"🌐 {network_name}"):
                    # Add resources
                    for res_idx, resource in enumerate(resources):
                        resource_name = resource.get("name", "Unknown")
                        resource_address = resource.get("address", "N/A")
                        resource_type = resource.get("type", "unknown")
                        resource_groups = resource.get("groups", [])

                        icon_class = (
                            Internet if resource_type in ["subnet", "host"] else Router
                        )
                        resource_node_name = f"res_{network_idx}_{res_idx}"

                        label = f"{resource_name}\\n{resource_address}"
                        if resource_groups:
                            group_names = []
                            for group in resource_groups:
                                if isinstance(group, dict):
                                    group_name = (
                                        group.get("name")
                                        or group.get("id")
                                        or "Unknown"
                                    )
                                    group_names.append(str(group_name))
                                else:
                                    group_names.append(str(group))
                            label += f"\\n🏷️ {', '.join(group_names)}"

                        network_resource_nodes[resource_node_name] = icon_class(label)

                    # Add routers
                    for router_idx, router in enumerate(routers):
                        router_name = router.get("name", "Unknown Router")
                        router_node_name = f"router_{network_idx}_{router_idx}"
                        network_resource_nodes[router_node_name] = Router(
                            f"🔀 {router_name}"
                        )

            # Generate dynamic color mapping
            source_group_colors = self._get_source_group_colors(
                list(connections_data["all_source_groups"])
            )

            # Create optimized group connections
            for (source_name, dest_group_name), policy_names in connections_data[
                "group_connections"
            ].items():
                if (
                    dest_group_name in connections_data["group_name_to_nodes"]
                    and source_name in source_group_nodes
                ):
                    color = source_group_colors.get(source_name, "#FF6B6B")
                    merged_label = self._format_policy_label(policy_names, "Group")

                    for resource_node in connections_data["group_name_to_nodes"][
                        dest_group_name
                    ]:
                        if resource_node in network_resource_nodes:
                            (
                                source_group_nodes[source_name]
                                >> Edge(
                                    color=color,
                                    style="dashed",
                                    label=merged_label,
                                    penwidth="2",
                                )
                                >> network_resource_nodes[resource_node]
                            )

            # Create optimized direct connections
            for (source_name, dest_node), policy_names in connections_data[
                "direct_connections"
            ].items():
                if (
                    source_name in source_group_nodes
                    and dest_node in network_resource_nodes
                ):
                    color = source_group_colors.get(source_name, "#FF6B6B")
                    merged_label = self._format_policy_label(policy_names, "Direct")

                    (
                        source_group_nodes[source_name]
                        >> Edge(
                            color=color, style="solid", label=merged_label, penwidth="3"
                        )
                        >> network_resource_nodes[dest_node]
                    )

        output_filename = f"{diagram_name}.png"
        print(f"✅ Diagrams saved as {output_filename}")
        return output_filename

    def __repr__(self) -> str:
        return f"APIClient(host={self.host}, base_url={self.base_url})"
