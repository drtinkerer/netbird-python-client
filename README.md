# NetBird Python Client

[![PyPI version](https://badge.fury.io/py/netbird-client.svg)](https://badge.fury.io/py/netbird-client)
[![Python Support](https://img.shields.io/pypi/pyversions/netbird-client.svg)](https://pypi.org/project/netbird-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python client library for the [NetBird](https://netbird.io) API. Provides complete access to all NetBird API resources with a simple, intuitive interface.

## Features

- ✅ **Complete API Coverage** - All 11 NetBird API resources supported
- ✅ **Type Safety** - Full typing support with Pydantic models
- ✅ **Modern Python** - Built for Python 3.8+ with async support ready
- ✅ **Comprehensive Error Handling** - Detailed exception classes for different error types
- ✅ **Extensive Documentation** - Complete API reference and examples
- ✅ **PyPI Ready** - Easy installation and distribution

## Supported Resources

| Resource | Description | Endpoints |
|----------|-------------|-----------|
| **Accounts** | Account management and settings | List, Update, Delete |
| **Users** | User lifecycle management | CRUD + Invite, Current user |
| **Tokens** | API token management | CRUD operations |
| **Peers** | Network peer management | CRUD + Accessible peers |
| **Setup Keys** | Peer setup key management | CRUD operations |
| **Groups** | Peer group management | CRUD operations |
| **Networks** | Network and resource management | CRUD + Resources/Routers |
| **Policies** | Access control policies | CRUD operations |
| **Routes** | Network routing configuration | CRUD operations |
| **DNS** | DNS settings and nameservers | Nameserver groups + Settings |
| **Events** | Audit and traffic events | Audit logs, Network traffic |

## Installation

```bash
pip install netbird-client
```

## Quick Start

```python
from netbird import APIClient

# Initialize the client
client = APIClient(
    host=\"api.netbird.io\",
    api_token=\"your-api-token-here\"
)

# List all peers
peers = client.peers.list()
print(f\"Found {len(peers)} peers\")

# Get current user
user = client.users.get_current()
print(f\"Logged in as: {user.name}\")

# Create a new group
from netbird.models import GroupCreate
group_data = GroupCreate(
    name=\"Development Team\",
    peers=[\"peer-1\", \"peer-2\"]
)
group = client.groups.create(group_data)
print(f\"Created group: {group.name}\")
```

## Authentication

NetBird uses token-based authentication. You can use either a personal access token or a service user token:

### Personal Access Token (Recommended)
```python
client = APIClient(
    host=\"api.netbird.io\",
    api_token=\"your-personal-access-token\"
)
```

### Service User Token
```python
client = APIClient(
    host=\"api.netbird.io\",
    api_token=\"your-service-user-token\"
)
```

### Self-Hosted NetBird
```python
client = APIClient(
    host=\"netbird.yourcompany.com:33073\",
    api_token=\"your-token\",
    use_ssl=True  # or False for HTTP
)
```

## Examples

### User Management
```python
from netbird.models import UserCreate, UserRole

# Create a new user
user_data = UserCreate(
    email=\"john@example.com\",
    name=\"John Doe\",
    role=UserRole.USER,
    auto_groups=[\"group-developers\"]
)
user = client.users.create(user_data)

# Update user role
from netbird.models import UserUpdate
update_data = UserUpdate(role=UserRole.ADMIN)
updated_user = client.users.update(user.id, update_data)
```

### Network Management
```python
from netbird.models import NetworkCreate, PolicyCreate, PolicyRule

# Create a network
network_data = NetworkCreate(
    name=\"Production Network\",
    description=\"Main production environment\"
)
network = client.networks.create(network_data)

# Create access policy
rule = PolicyRule(
    name=\"Allow SSH\",
    action=\"accept\",
    protocol=\"tcp\", 
    ports=[\"22\"],
    sources=[\"group-admins\"],
    destinations=[\"group-servers\"]
)
policy_data = PolicyCreate(
    name=\"Admin SSH Access\",
    rules=[rule]
)
policy = client.policies.create(policy_data)
```

### Setup Key Management
```python
from netbird.models import SetupKeyCreate

# Create a reusable setup key
key_data = SetupKeyCreate(
    name=\"Development Environment\",
    type=\"reusable\",
    expires_in=86400,  # 24 hours
    usage_limit=10,
    auto_groups=[\"group-dev\"]
)
setup_key = client.setup_keys.create(key_data)
print(f\"Setup key: {setup_key.key}\")
```

### Event Monitoring
```python
# Get audit events
audit_events = client.events.get_audit_events()
for event in audit_events[-10:]:  # Last 10 events
    print(f\"{event.timestamp}: {event.activity}\")

# Get network traffic events (cloud-only)
traffic_events = client.events.get_network_traffic_events(
    protocol=\"tcp\",
    page_size=100
)
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
    user = client.users.get(\"invalid-user-id\")
except NetBirdNotFoundError:
    print(\"User not found\")
except NetBirdAuthenticationError:
    print(\"Invalid API token\")
except NetBirdRateLimitError as e:
    print(f\"Rate limited. Retry after {e.retry_after} seconds\")
except NetBirdAPIError as e:
    print(f\"API error: {e.message}\")
```

## Configuration Options

```python
client = APIClient(
    host=\"api.netbird.io\",
    api_token=\"your-token\",
    use_ssl=True,           # Use HTTPS (default: True)
    timeout=30.0,           # Request timeout in seconds (default: 30)
    base_path=\"/api\"        # API base path (default: \"/api\")
)
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/netbirdio/netbird-python-client.git
cd netbird-python-client

# Install development dependencies
pip install -e \".[dev]\"

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

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/netbird --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

## Documentation

- **[API Reference](docs/api-reference/)** - Complete API documentation
- **[User Guide](docs/)** - Detailed usage guide and examples
- **[Examples](examples/)** - Practical example scripts
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

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/netbirdio/netbird-python-client/issues)
- **NetBird Community**: [Join the discussion](https://github.com/netbirdio/netbird/discussions)
- **Documentation**: [API Documentation](https://docs.netbird.io/api)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

Made with ❤️ by [Bhushan Rane](https://github.com/bhushanrane) | Contributed to the NetBird community