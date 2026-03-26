# NetBird Python Client (Unofficial)

[![PyPI version](https://badge.fury.io/py/netbird.svg)](https://badge.fury.io/py/netbird)
[![Python Support](https://img.shields.io/pypi/pyversions/netbird.svg)](https://pypi.org/project/netbird/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Unofficial** Python client library for the [NetBird](https://netbird.io) API. Provides complete access to all NetBird API resources with a simple, intuitive interface.

> **⚠️ Disclaimer**: This is an **unofficial**, community-maintained client library. It is **not affiliated with, endorsed by, or officially supported** by NetBird or the NetBird team. For official NetBird tools and support, please visit [netbird.io](https://netbird.io).

This client follows the same upstream schemas as the official NetBird REST APIs, ensuring full compatibility and consistency with the NetBird ecosystem.

## Features

- ✅ **Full API Parity** - 30+ resources covering core, cloud, and EDR endpoints
- ✅ **Cloud & Self-Hosted** - Works with NetBird Cloud and self-hosted instances
- ✅ **Forward-Compatible** - `extra="allow"` on all models accepts future API fields gracefully
- ✅ **Upstream Schema Compliance** - Follows official NetBird REST API schemas exactly
- ✅ **Dictionary Responses** - Clean dictionary responses for easy data access
- ✅ **Type Safety** - Pydantic models for input validation, dictionaries for responses
- ✅ **Network Visualization** - Built-in diagram generation (Mermaid, Graphviz, Python Diagrams)
- ✅ **Modern Python** - Built for Python 3.9+ (supports 3.9-3.14)
- ✅ **Comprehensive Error Handling** - Detailed exception classes for different error types
- ✅ **88% Test Coverage** - 364 unit tests covering all resources
- ✅ **PyPI Ready** - Easy installation and distribution

## Supported Resources

### Core Resources

| Resource | Description | Key Methods |
|----------|-------------|-------------|
| **Accounts** | Account management and settings | List, Update, Delete |
| **Users** | User lifecycle management | CRUD, Approve, Reject, Invites, Password |
| **Tokens** | API token management | CRUD operations |
| **Peers** | Network peer management | CRUD, Temporary Access, Jobs |
| **Setup Keys** | Peer setup key management | CRUD operations |
| **Groups** | Peer group management | CRUD operations |
| **Networks** | Network and resource management | CRUD + Resources/Routers |
| **Policies** | Access control policies | CRUD operations |
| **Routes** | Network routing (deprecated) | CRUD (use Networks instead) |
| **DNS** | DNS nameserver groups | CRUD + Settings |
| **DNS Zones** | Custom DNS zones and records | Zone CRUD + Record CRUD |
| **Events** | Audit and traffic events | Audit, Traffic, Proxy events |
| **Posture Checks** | Device compliance verification | CRUD operations |
| **Geo Locations** | Geographic data | Countries, Cities |
| **Identity Providers** | OAuth2/OIDC providers | CRUD operations |
| **Instance** | Instance management | Status, Version, Setup |

### Cloud Resources (`client.cloud.*`)

| Resource | Description | Key Methods |
|----------|-------------|-------------|
| **Services** | Reverse proxy services | CRUD + Domain management |
| **Ingress** | Ingress port allocation | Port + Peer management |
| **EDR Peers** | EDR peer bypass | Bypass, List, Revoke |
| **EDR Falcon** | CrowdStrike Falcon | Get, Create, Update, Delete |
| **EDR Huntress** | Huntress integration | Get, Create, Update, Delete |
| **EDR Intune** | Microsoft Intune | Get, Create, Update, Delete |
| **EDR SentinelOne** | SentinelOne integration | Get, Create, Update, Delete |
| **MSP** | Multi-tenant management | Tenants CRUD + Users/Peers |
| **Invoices** | Billing invoices | List, PDF, CSV |
| **Usage** | Billing usage stats | Get usage |
| **Event Streaming** | Event streaming integrations | CRUD operations |
| **IDP/SCIM** | SCIM identity providers | CRUD + Token + Logs |

## Installation

```bash
pip install netbird
```

## Quick Start

```python
from netbird import APIClient

# Initialize the client
client = APIClient(
    host="api.netbird.io",  # or "netbird.yourcompany.com" for self-hosted
    api_token="your-api-token-here"
)

# List all peers
peers = client.peers.list()
print(f"Found {len(peers)} peers")

# Get current user
user = client.users.get_current()
print(f"Logged in as: {user['name']}")

# Create a new group
from netbird.models import GroupCreate
group_data = GroupCreate(
    name="My Team",
    peers=["peer-1", "peer-2"]
)
group = client.groups.create(group_data)
print(f"Created group: {group['name']}")

# Access cloud-only resources (NetBird Cloud only)
usage = client.cloud.usage.get()
print(f"Active peers: {usage['active_peers']}")

# EDR integrations
falcon_config = client.cloud.edr.falcon.get()
```

## Authentication

NetBird uses token-based authentication with API access tokens:

```python
client = APIClient(
    host="your-netbird-host.com",  # e.g., "api.netbird.io" for cloud
    api_token="your-api-token"
)
```

You can get your API token from:
- **NetBird Cloud**: Dashboard → Settings → API Tokens
- **Self-hosted**: Your NetBird management interface

### Self-Hosted NetBird
```python
client = APIClient(
    host="netbird.yourcompany.com:33073",
    api_token="your-token"
)
```

## Examples

### User Management
```python
from netbird.models import UserCreate, UserRole

# Create a new user
user_data = UserCreate(
    email="user@company.com",
    name="New User",
    role=UserRole.USER,
    auto_groups=["group-default"]
)
user = client.users.create(user_data)
print(f"Created user: {user['name']} ({user['email']})")

# Update user role
from netbird.models import UserUpdate
update_data = UserUpdate(role=UserRole.ADMIN)
updated_user = client.users.update(user['id'], update_data)
print(f"Updated user role to: {updated_user['role']}")
```

### Network Management
```python
from netbird.models import NetworkCreate, PolicyCreate, PolicyRule

# Create a network
network_data = NetworkCreate(
    name="My Network",
    description="Network environment"
)
network = client.networks.create(network_data)
print(f"Created network: {network['name']}")

# Create access policy
rule = PolicyRule(
    name="Allow Access",
    action="accept",
    protocol="tcp", 
    ports=["22"],
    sources=["source-group"],
    destinations=["destination-group"]
)
policy_data = PolicyCreate(
    name="Access Policy",
    rules=[rule]
)
policy = client.policies.create(policy_data)
print(f"Created policy: {policy['name']}")
```

### Setup Key Management
```python
from netbird.models import SetupKeyCreate

# Create a reusable setup key
key_data = SetupKeyCreate(
    name="Environment Setup",
    type="reusable",
    expires_in=86400,  # 24 hours
    usage_limit=10,
    auto_groups=["default-group"]
)
setup_key = client.setup_keys.create(key_data)
print(f"Setup key: {setup_key['key']}")
print(f"Key valid: {setup_key['valid']}")
```

### Event Monitoring
```python
# Get audit events
audit_events = client.events.get_audit_events()
for event in audit_events[-10:]:  # Last 10 events
    print(f"{event['timestamp']}: {event['activity']}")
    if event.get('initiator_name'):
        print(f"  Initiated by: {event['initiator_name']}")

# Get network traffic events (cloud-only)
traffic_events = client.events.get_network_traffic_events(
    protocol="tcp",
    page_size=100
)
for traffic in traffic_events[:5]:
    print(f"Traffic: {traffic['source_ip']} -> {traffic['destination_ip']}")
```

## Network Visualization

The NetBird Python client includes powerful network visualization capabilities that can generate topology diagrams in multiple formats:

### Generate Network Maps

```python
from netbird import APIClient
from netbird.network_map import generate_full_network_map

# Initialize client
client = APIClient(host="your-netbird-host.com", api_token="your-token")

# Generate enriched network data
networks = generate_full_network_map(client)

# Access enriched data
for network in networks:
    print(f"Network: {network['name']}")
    for resource in network.get('resources', []):
        print(f"  Resource: {resource['name']} - {resource['address']}")
    for policy in network.get('policies', []):
        print(f"  Policy: {policy['name']}")
```

### Topology Visualization

```python
from netbird.network_map import get_network_topology_data

# Get optimized topology data for visualization
topology = get_network_topology_data(client, optimize_connections=True)

print(f"Found {len(topology['all_source_groups'])} source groups")
print(f"Found {len(topology['group_connections'])} group connections")
print(f"Found {len(topology['direct_connections'])} direct connections")
```

### Diagram Generation

Generate visual network topology diagrams directly from the client:

```python
from netbird import APIClient

# Initialize client
client = APIClient(host="your-netbird-host.com", api_token="your-token")

# Generate Mermaid diagram (default, GitHub/GitLab compatible)
mermaid_content = client.generate_diagram(format="mermaid")
print(mermaid_content)

# Generate Graphviz diagram (PNG, SVG, PDF)
client.generate_diagram(format="graphviz", output_file="my_network")

# Generate Python Diagrams (PNG)
client.generate_diagram(format="diagrams", output_file="network_topology")

# Customize what to include
client.generate_diagram(
    format="mermaid",
    include_routers=True,
    include_policies=True, 
    include_resources=True,
    output_file="complete_network"
)
```

### Supported Diagram Formats

| Format | Output Files | Best For |
|--------|-------------|----------|
| **Mermaid** | `.mmd`, `.md` | GitHub/GitLab documentation, web viewing |
| **Graphviz** | `.png`, `.svg`, `.pdf`, `.dot` | High-quality publications, presentations |
| **Diagrams** | `.png` | Code documentation, architecture diagrams |

### Diagram Features

- **Source Groups**: Visual representation of user groups with distinct colors
- **Networks & Resources**: Hierarchical network structure with resource details
- **Policy Connections**: 
  - 🟢 **Group-based access** (dashed lines)
  - 🔵 **Direct resource access** (solid lines)
- **Optimized Layout**: Merged connections to reduce visual complexity
- **Rich Information**: Resource addresses, types, and group memberships

### Installation for Diagrams

```bash
# For Graphviz diagrams
pip install graphviz

# For Python Diagrams
pip install diagrams

# Mermaid requires no additional dependencies
```

## Error Handling

The client provides specific exception types for different error conditions:

```python
from netbird.exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)

try:
    user = client.users.get("invalid-user-id")
except NetBirdNotFoundError:
    print("User not found")
except NetBirdAuthenticationError:
    print("Invalid API token")
except NetBirdRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except NetBirdAPIError as e:
    print(f"API error: {e.message}")
```

## Configuration Options

```python
client = APIClient(
    host="your-netbird-host.com",  # Your NetBird API host
    api_token="your-token",
    timeout=30.0,           # Request timeout in seconds (default: 30)
    base_path="/api"        # API base path (default: "/api")
)
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/drtinkerer/netbird-python-client.git
cd netbird-python-client

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src/

# Format code
black src/ tests/
isort src/ tests/

# Run linting
flake8 src/ tests/
```

### Testing & Coverage

#### Test Statistics
- **Total Tests**: 364 unit tests
- **Coverage**: 88% (2,045 statements)
- **All models and resources**: 100% coverage

#### Coverage by Module
| Module | Coverage |
|--------|----------|
| **Models** (core + cloud) | 100% |
| **Resources** (core + cloud) | 100% |
| **Auth / Exceptions** | 100% |
| **Cloud Namespace** | 88% |
| **Network Map** | 98% |
| **Client Core** | 47% (diagram generation untested) |

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/netbird --cov-report=html

# Run specific test categories
pytest tests/unit/              # Core resource tests
pytest tests/unit/cloud/        # Cloud resource tests
```

## Response Format

The NetBird Python client provides clean and intuitive API responses:

- **Input validation**: Uses Pydantic models for type safety and validation
- **API responses**: Returns standard Python dictionaries for easy access
- **Familiar patterns**: Simple dictionary-based responses

```python
# Input: Type-safe Pydantic models
user_data = UserCreate(email="john@example.com", name="John Doe")

# Output: Standard Python dictionaries
user = client.users.create(user_data)
print(user['name'])          # Access like a dictionary
print(user['email'])         # Easy dictionary access
print(user.get('role'))      # Safe access with .get()
```

## Interactive Demo

Explore the client with our **Jupyter notebook demo**:

```bash
# Install Jupyter if you haven't already
pip install jupyter

# Start the demo notebook
jupyter notebook netbird_demo.ipynb
```

The demo notebook shows real usage examples for all API resources.

## Documentation

- **[Full Documentation](https://drtinkerer.github.io/netbird-python-client/)** - Comprehensive Sphinx docs with API reference, user guides, and examples
- **[Jupyter Demo](netbird_demo.ipynb)** - Interactive demonstration of all features
- **[Integration Tests](tests/integration/)** - Real API usage examples
- **[Unit Tests](tests/unit/)** - Complete test coverage examples
- **[NetBird Documentation](https://docs.netbird.io/)** - Official NetBird docs

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer & Legal

**This is an unofficial, community-maintained client library.**

- ❌ **Not official**: This library is NOT affiliated with, endorsed by, or officially supported by NetBird or the NetBird team
- ❌ **No warranty**: This software is provided "as is" without warranty of any kind
- ❌ **No official support**: For official NetBird support, please contact NetBird directly
- ✅ **Open source**: This is a community effort to provide Python developers with NetBird API access
- ✅ **Best effort compatibility**: We strive to maintain compatibility with NetBird's official API

**NetBird** is a trademark of NetBird. This project is not endorsed by or affiliated with NetBird.

For official NetBird tools, documentation, and support:
- **Official Website**: [netbird.io](https://netbird.io)
- **Official Documentation**: [docs.netbird.io](https://docs.netbird.io)
- **Official GitHub**: [github.com/netbirdio/netbird](https://github.com/netbirdio/netbird)

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/drtinkerer/netbird-python-client/issues)
- **NetBird Community**: [Join the discussion](https://github.com/netbirdio/netbird/discussions)
- **Documentation**: [API Documentation](https://docs.netbird.io/api)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

Made with ❤️ by [Bhushan Rane](https://github.com/drtinkerer)