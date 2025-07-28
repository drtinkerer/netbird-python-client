---
layout: home
title: NetBird Python Client
---

# NetBird Python Client Documentation

[![PyPI version](https://badge.fury.io/py/netbird-client.svg)](https://badge.fury.io/py/netbird-client)
[![Python Support](https://img.shields.io/pypi/pyversions/netbird-client.svg)](https://pypi.org/project/netbird-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the official documentation for the NetBird Python client library. This client provides complete access to all NetBird API resources with a simple, intuitive interface following AWS SDK (boto3) patterns.

## Quick Start

```python
from netbird import APIClient

# Initialize the client
client = APIClient(
    host="api.netbird.io",
    api_token="your-api-token-here"
)

# Get current user
user = client.users.get_current()
print(f"Logged in as: {user['name']}")

# List all peers
peers = client.peers.list()
print(f"Found {len(peers)} peers")
```

## Features

- ✅ **Complete API Coverage** - All 11 NetBird API resources supported
- ✅ **AWS SDK Style** - Dictionary responses following boto3 patterns for familiar usage
- ✅ **Type Safety** - Pydantic models for input validation, dictionaries for responses
- ✅ **Modern Python** - Built for Python 3.8+ with async support ready
- ✅ **Comprehensive Error Handling** - Detailed exception classes for different error types
- ✅ **High Test Coverage** - 97.56% unit test coverage, 83.29% integration coverage
- ✅ **Extensive Documentation** - Complete API reference and examples

## Navigation

<div class="grid">
  <div class="card">
    <h3><a href="{{ '/guides/installation' | relative_url }}">🚀 Installation</a></h3>
    <p>Get started with pip installation and basic setup</p>
  </div>
  
  <div class="card">
    <h3><a href="{{ '/guides/quickstart' | relative_url }}">⚡ Quick Start</a></h3>
    <p>Basic usage examples and authentication setup</p>
  </div>
  
  <div class="card">
    <h3><a href="{{ '/api' | relative_url }}">📚 API Reference</a></h3>
    <p>Complete documentation of all resources and methods</p>
  </div>
  
  <div class="card">
    <h3><a href="{{ '/examples' | relative_url }}">💡 Examples</a></h3>
    <p>Practical examples and common use cases</p>
  </div>
</div>

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

## Response Format

The NetBird Python client follows the **boto3 pattern** for API responses:

- **Input validation**: Uses Pydantic models for type safety and validation
- **API responses**: Returns standard Python dictionaries (like boto3)
- **Familiar patterns**: AWS SDK users will feel right at home

```python
# Input: Type-safe Pydantic models
from netbird.models import UserCreate
user_data = UserCreate(email="john@example.com", name="John Doe")

# Output: Standard Python dictionaries
user = client.users.create(user_data)
print(user['name'])          # Access like a dictionary
print(user['email'])         # Familiar boto3-style usage
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

## Contributing

We welcome contributions! Please see our [Contributing Guide]({{ '/guides/contributing' | relative_url }}) for guidelines.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/bhushanrane/netbird-python-client/issues)
- **NetBird Community**: [Join the discussion](https://github.com/netbirdio/netbird/discussions)
- **Documentation**: [API Documentation](https://docs.netbird.io/api)

---

Made with ❤️ by [Bhushan Rane](https://github.com/bhushanrane) | Contributed to the NetBird community