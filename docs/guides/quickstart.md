---
layout: page
title: Quick Start Guide
description: Get started with the NetBird Python client in minutes
---

# Quick Start Guide

This guide will help you get up and running with the NetBird Python client in just a few minutes.

## 1. Installation

First, install the NetBird Python client:

```bash
pip install netbird-client
```

## 2. Get Your API Token

You'll need a NetBird API token to authenticate:

1. Log into your NetBird dashboard
2. Go to **Settings** → **Access Tokens**
3. Create a new token with appropriate permissions
4. Copy the token value

## 3. Basic Usage

### Initialize the Client

```python
from netbird import APIClient

# For NetBird Cloud
client = APIClient(
    host="api.netbird.io",
    api_token="your-api-token-here"
)

# For Self-Hosted NetBird
client = APIClient(
    host="netbird.yourcompany.com:33073",
    api_token="your-api-token-here",
    use_ssl=True
)
```

### Your First API Call

Let's start by getting information about the current authenticated user:

```python
# Get current user information
user = client.users.get_current()
print(f"Logged in as: {user['name']} ({user['email']})")
print(f"Role: {user['role']}")
```

## 4. Common Operations

### List Resources

```python
# List all peers in your network
peers = client.peers.list()
print(f"Found {len(peers)} peers:")
for peer in peers:
    status = "🟢 Online" if peer['connected'] else "🔴 Offline"
    print(f"  {status} {peer['name']} ({peer['ip']})")

# List all groups
groups = client.groups.list()
print(f"\nFound {len(groups)} groups:")
for group in groups:
    print(f"  📁 {group['name']} ({group['peers_count']} peers)")
```

### Create Resources

```python
from netbird.models import GroupCreate, SetupKeyCreate

# Create a new group
group_data = GroupCreate(
    name="Development Team",
    peers=[]  # Start with no peers
)
new_group = client.groups.create(group_data)
print(f"Created group: {new_group['name']} (ID: {new_group['id']})")

# Create a setup key for new devices
key_data = SetupKeyCreate(
    name="Development Environment",
    type="reusable",
    expires_in=86400,  # 24 hours
    usage_limit=10,
    auto_groups=[new_group['id']]
)
setup_key = client.setup_keys.create(key_data)
print(f"Setup key: {setup_key['key']}")
```

### Update Resources

```python
from netbird.models import GroupUpdate

# Update the group we just created
update_data = GroupUpdate(name="Updated Development Team")
updated_group = client.groups.update(new_group['id'], update_data)
print(f"Updated group name to: {updated_group['name']}")
```

### Error Handling

```python
from netbird.exceptions import (
    NetBirdAPIError,
    NetBirdNotFoundError,
    NetBirdAuthenticationError
)

try:
    # Try to get a non-existent user
    user = client.users.get("invalid-user-id")
except NetBirdNotFoundError:
    print("User not found")
except NetBirdAuthenticationError:
    print("Invalid API token")
except NetBirdAPIError as e:
    print(f"API error: {e}")
```

## 5. Response Format

The NetBird Python client returns **dictionary responses** (boto3 style):

```python
# API responses are dictionaries
user = client.users.get_current()

# Access data like a dictionary
print(user['name'])          # Direct access
print(user['email'])         # Familiar AWS SDK patterns
print(user.get('role'))      # Safe access with .get()

# Check if fields exist
if 'last_login' in user:
    print(f"Last login: {user['last_login']}")
```

## 6. Configuration Options

```python
client = APIClient(
    host="api.netbird.io",
    api_token="your-token",
    use_ssl=True,           # Use HTTPS (default: True)
    timeout=30.0,           # Request timeout in seconds (default: 30)
    base_path="/api"        # API base path (default: "/api")
)
```

## 7. Environment Variables

You can also use environment variables for configuration:

```bash
export NETBIRD_HOST="api.netbird.io"
export NETBIRD_API_TOKEN="your-api-token-here"
```

```python
import os
from netbird import APIClient

client = APIClient(
    host=os.getenv("NETBIRD_HOST"),
    api_token=os.getenv("NETBIRD_API_TOKEN")
)
```

## 8. Interactive Demo

For a comprehensive interactive demonstration, check out our Jupyter notebook:

```bash
# Install Jupyter if you haven't already
pip install jupyter

# Download and run the demo notebook
jupyter notebook netbird_demo.ipynb
```

## Next Steps

Now that you have the basics down, explore more advanced features:

- **[API Reference](../api/)** - Complete documentation of all resources
- **[Examples](../examples/)** - Practical examples and use cases
- **[Error Handling](../guides/error-handling/)** - Advanced error handling patterns
- **[Best Practices](../guides/best-practices/)** - Tips for production usage

## Need Help?

- **GitHub Issues**: [Report problems or ask questions](https://github.com/bhushanrane/netbird-python-client/issues)
- **NetBird Community**: [Join the discussion](https://github.com/netbirdio/netbird/discussions)
- **NetBird Documentation**: [Official NetBird docs](https://docs.netbird.io/)

## Clean Up

Don't forget to clean up any test resources you created:

```python
# Delete the test group we created
client.groups.delete(new_group['id'])
print("Cleaned up test resources")
```

Happy coding with NetBird! 🚀