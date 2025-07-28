# NetBird Python Client

[![PyPI version](https://badge.fury.io/py/netbird.svg)](https://badge.fury.io/py/netbird)
[![Python Support](https://img.shields.io/pypi/pyversions/netbird.svg)](https://pypi.org/project/netbird/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python client library for the [NetBird](https://netbird.io) API. Provides complete access to all NetBird API resources with a simple, intuitive interface.

This client follows the same upstream schemas as the official NetBird REST APIs, ensuring full compatibility and consistency with the NetBird ecosystem.

## Features

- ✅ **Complete API Coverage** - All 11 NetBird API resources supported
- ✅ **Upstream Schema Compliance** - Follows official NetBird REST API schemas exactly
- ✅ **Dictionary Responses** - Clean dictionary responses for easy data access
- ✅ **Type Safety** - Pydantic models for input validation, dictionaries for responses
- ✅ **Modern Python** - Built for Python 3.8+ with async support ready
- ✅ **Comprehensive Error Handling** - Detailed exception classes for different error types
- ✅ **High Test Coverage** - 97.56% unit test coverage, 83.29% integration coverage
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
pip install netbird
```

## Quick Start

```python
from netbird import APIClient

# Initialize the client
client = APIClient(
    host="api.netbird.io",
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
    name="Development Team",
    peers=["peer-1", "peer-2"]
)
group = client.groups.create(group_data)
print(f"Created group: {group['name']}")
```

## Authentication

NetBird uses token-based authentication. You can use either a personal access token or a service user token:

### Personal Access Token (Recommended)
```python
client = APIClient(
    host="api.netbird.io",
    api_token="your-personal-access-token"
)
```

### Service User Token
```python
client = APIClient(
    host="api.netbird.io",
    api_token="your-service-user-token"
)
```

### Self-Hosted NetBird
```python
client = APIClient(
    host="netbird.yourcompany.com:33073",
    api_token="your-token",
    use_ssl=True  # or False for HTTP
)
```

## Examples

### User Management
```python
from netbird.models import UserCreate, UserRole

# Create a new user
user_data = UserCreate(
    email="john@example.com",
    name="John Doe",
    role=UserRole.USER,
    auto_groups=["group-developers"]
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
    name="Production Network",
    description="Main production environment"
)
network = client.networks.create(network_data)
print(f"Created network: {network['name']}")

# Create access policy
rule = PolicyRule(
    name="Allow SSH",
    action="accept",
    protocol="tcp", 
    ports=["22"],
    sources=["group-admins"],
    destinations=["group-servers"]
)
policy_data = PolicyCreate(
    name="Admin SSH Access",
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
    name="Development Environment",
    type="reusable",
    expires_in=86400,  # 24 hours
    usage_limit=10,
    auto_groups=["group-dev"]
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
    host="api.netbird.io",
    api_token="your-token",
    use_ssl=True,           # Use HTTPS (default: True)
    timeout=30.0,           # Request timeout in seconds (default: 30)
    base_path="/api"        # API base path (default: "/api")
)
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/netbirdio/netbird-python-client.git
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

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/drtinkerer/netbird-python-client/issues)
- **NetBird Community**: [Join the discussion](https://github.com/netbirdio/netbird/discussions)
- **Documentation**: [API Documentation](https://docs.netbird.io/api)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

Made with ❤️ by [Bhushan Rane](https://github.com/drtinkerer)