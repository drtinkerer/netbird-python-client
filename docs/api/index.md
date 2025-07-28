---
layout: page
title: API Reference
description: Complete API documentation for the NetBird Python client
---

# API Reference

Complete documentation for all NetBird Python client resources and methods.

## Client Initialization

### APIClient

The main entry point for the NetBird Python client.

```python
from netbird import APIClient

client = APIClient(
    host="api.netbird.io",
    api_token="your-api-token",
    use_ssl=True,
    timeout=30.0,
    base_path="/api"
)
```

**Parameters:**
- `host` (str): NetBird server hostname
- `api_token` (str): Your NetBird API token
- `use_ssl` (bool, optional): Use HTTPS. Default: True
- `timeout` (float, optional): Request timeout in seconds. Default: 30.0
- `base_path` (str, optional): API base path. Default: "/api"

## Resources

The NetBird Python client provides access to all 11 NetBird API resources:

<div class="grid">
  <div class="card">
    <h3><a href="users/">👤 Users</a></h3>
    <p>User lifecycle management, authentication, and permissions</p>
    <span class="badge badge-info">CRUD + Invite</span>
  </div>
  
  <div class="card">
    <h3><a href="peers/">🖥️ Peers</a></h3>
    <p>Network peer management and device connectivity</p>
    <span class="badge badge-info">CRUD + Accessible</span>
  </div>
  
  <div class="card">
    <h3><a href="groups/">👥 Groups</a></h3>
    <p>Peer group organization and management</p>
    <span class="badge badge-success">CRUD</span>
  </div>
  
  <div class="card">
    <h3><a href="policies/">🔐 Policies</a></h3>
    <p>Network access control and security policies</p>
    <span class="badge badge-success">CRUD</span>
  </div>
  
  <div class="card">
    <h3><a href="networks/">🌐 Networks</a></h3>
    <p>Network and resource management</p>
    <span class="badge badge-info">CRUD + Resources/Routers</span>
  </div>
  
  <div class="card">
    <h3><a href="routes/">🛣️ Routes</a></h3>
    <p>Network routing configuration</p>
    <span class="badge badge-success">CRUD</span>
  </div>
  
  <div class="card">
    <h3><a href="setup-keys/">🔑 Setup Keys</a></h3>
    <p>Device setup key management</p>
    <span class="badge badge-success">CRUD</span>
  </div>
  
  <div class="card">
    <h3><a href="accounts/">🏢 Accounts</a></h3>
    <p>Account settings and configuration</p>
    <span class="badge badge-warning">List, Update, Delete</span>
  </div>
  
  <div class="card">
    <h3><a href="tokens/">🎫 Tokens</a></h3>
    <p>API token management</p>
    <span class="badge badge-success">CRUD</span>
  </div>
  
  <div class="card">
    <h3><a href="dns/">🌍 DNS</a></h3>
    <p>DNS settings and nameserver groups</p>
    <span class="badge badge-info">Nameservers + Settings</span>
  </div>
  
  <div class="card">
    <h3><a href="events/">📊 Events</a></h3>
    <p>Audit logs and network traffic events</p>
    <span class="badge badge-warning">Read-only</span>
  </div>
</div>

## Response Format

All API methods return **dictionary responses** following the boto3 pattern:

```python
# API responses are dictionaries
user = client.users.get_current()
print(user['name'])          # Dictionary access
print(user['email'])         # Familiar AWS SDK patterns
print(user.get('role'))      # Safe access with .get()

# Input validation uses Pydantic models
from netbird.models import UserCreate
user_data = UserCreate(email="john@example.com", name="John Doe")
created_user = client.users.create(user_data)
print(f"Created: {created_user['name']}")  # Response is a dictionary
```

## Common Patterns

### CRUD Operations

Most resources support standard CRUD operations:

```python
# CREATE
from netbird.models import GroupCreate
group_data = GroupCreate(name="New Group", peers=[])
group = client.groups.create(group_data)

# READ
group = client.groups.get(group['id'])
all_groups = client.groups.list()

# UPDATE
from netbird.models import GroupUpdate
update_data = GroupUpdate(name="Updated Group")
updated_group = client.groups.update(group['id'], update_data)

# DELETE
client.groups.delete(group['id'])
```

### Error Handling

```python
from netbird.exceptions import (
    NetBirdAPIError,
    NetBirdNotFoundError,
    NetBirdAuthenticationError,
    NetBirdValidationError,
    NetBirdRateLimitError,
    NetBirdServerError
)

try:
    user = client.users.get("user-id")
except NetBirdNotFoundError:
    print("User not found")
except NetBirdAuthenticationError:
    print("Invalid API token")
except NetBirdValidationError as e:
    print(f"Validation error: {e}")
except NetBirdRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except NetBirdServerError:
    print("Server error")
except NetBirdAPIError as e:
    print(f"General API error: {e}")
```

### Pagination

Some resources support pagination:

```python
# Get paginated results
events = client.events.get_audit_events(page_size=50)

# Process results
for event in events:
    print(f"{event['timestamp']}: {event['activity']}")
```

## Data Models

The client uses Pydantic models for input validation. All models are available in the `netbird.models` module:

### Core Models
- `UserCreate`, `UserUpdate` - User management
- `PeerUpdate` - Peer management
- `GroupCreate`, `GroupUpdate` - Group management
- `PolicyCreate`, `PolicyUpdate`, `PolicyRule` - Policy management
- `NetworkCreate`, `NetworkUpdate` - Network management
- `RouteCreate`, `RouteUpdate` - Route management
- `SetupKeyCreate`, `SetupKeyUpdate` - Setup key management
- `TokenCreate` - Token management

### Common Fields

Most resources include these common fields in responses:

```python
{
    'id': 'unique-identifier',
    'created_at': '2023-01-01T00:00:00Z',
    'updated_at': '2023-01-01T00:00:00Z',
    'name': 'resource-name'
}
```

## Rate Limiting

The NetBird API may enforce rate limits. The client handles this automatically:

```python
try:
    users = client.users.list()
except NetBirdRateLimitError as e:
    # Wait for the specified time before retrying
    time.sleep(e.retry_after)
    users = client.users.list()
```

## Best Practices

1. **Use environment variables** for API tokens
2. **Handle exceptions** appropriately for your use case
3. **Use context managers** for automatic cleanup
4. **Cache responses** when appropriate to reduce API calls
5. **Use specific exceptions** instead of catching all `NetBirdAPIError`

```python
# Good: Use context manager
with APIClient(host=host, api_token=token) as client:
    users = client.users.list()

# Good: Environment variables
import os
client = APIClient(
    host=os.getenv("NETBIRD_HOST"),
    api_token=os.getenv("NETBIRD_TOKEN")
)
```

## Next Steps

- Explore specific resource documentation in the sections above
- Check out [practical examples](../examples/)
- Review [integration patterns](../guides/integration/)
- Learn about [testing strategies](../guides/testing/)