---
layout: page
title: Users API
description: User management and authentication
parent: API Reference
---

# Users API

The Users API provides complete user lifecycle management including creation, updates, invitations, and authentication.

## Methods

### `list()`

List all users in the account.

**Returns:** `List[Dict[str, Any]]` - List of user dictionaries

**Example:**
```python
users = client.users.list()
for user in users:
    print(f"User: {user['name']} ({user['email']}) - Role: {user['role']}")
```

### `create(user_data)`

Create a new user.

**Parameters:**
- `user_data` (UserCreate): User creation data

**Returns:** `Dict[str, Any]` - Created user dictionary

**Example:**
```python
from netbird.models import UserCreate, UserRole

user_data = UserCreate(
    email="john@example.com",
    name="John Doe",
    role=UserRole.USER,
    auto_groups=["group-id-1", "group-id-2"]
)
user = client.users.create(user_data)
print(f"Created user: {user['name']} (ID: {user['id']})")
```

### `get(user_id)`

Get a specific user by ID.

**Parameters:**
- `user_id` (str): Unique user identifier

**Returns:** `Dict[str, Any]` - User dictionary

**Example:**
```python
user = client.users.get("user-123")
print(f"User: {user['name']} - Status: {user['status']}")
```

### `update(user_id, user_data)`

Update an existing user.

**Parameters:**
- `user_id` (str): Unique user identifier
- `user_data` (UserUpdate): User update data

**Returns:** `Dict[str, Any]` - Updated user dictionary

**Example:**
```python
from netbird.models import UserUpdate, UserRole

update_data = UserUpdate(role=UserRole.ADMIN)
user = client.users.update("user-123", update_data)
print(f"Updated user role to: {user['role']}")
```

### `delete(user_id)`

Delete a user.

**Parameters:**
- `user_id` (str): Unique user identifier

**Returns:** `None`

**Example:**
```python
client.users.delete("user-123")
print("User deleted successfully")
```

### `invite(user_id)`

Resend user invitation.

**Parameters:**
- `user_id` (str): Unique user identifier

**Returns:** `None`

**Example:**
```python
client.users.invite("user-123")
print("Invitation sent")
```

### `get_current()`

Get the current authenticated user.

**Returns:** `Dict[str, Any]` - Current user dictionary

**Example:**
```python
current_user = client.users.get_current()
print(f"Logged in as: {current_user['name']} ({current_user['email']})")
print(f"Role: {current_user['role']}")
```

## Data Models

### User Response

User dictionaries contain the following fields:

```python
{
    "id": "user-123",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "user",  # "owner", "admin", "user"
    "status": "active",  # "active", "disabled", "invited"
    "auto_groups": ["group-id-1", "group-id-2"],
    "is_current": false,
    "is_service_user": false,
    "is_blocked": false,
    "last_login": "2023-01-01T12:00:00Z",
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
}
```

### UserCreate

Input model for creating users:

```python
from netbird.models import UserCreate, UserRole

user_data = UserCreate(
    email="john@example.com",        # Required: User email
    name="John Doe",                 # Required: Display name
    role=UserRole.USER,              # Optional: user role (default: USER)
    auto_groups=["group-id-1"]       # Optional: auto-assign to groups
)
```

### UserUpdate

Input model for updating users:

```python
from netbird.models import UserUpdate, UserRole

update_data = UserUpdate(
    name="John Smith",               # Optional: new display name
    role=UserRole.ADMIN,             # Optional: new role
    auto_groups=["group-id-2"]       # Optional: update auto-groups
)
```

## User Roles

- `owner` - Full administrative access
- `admin` - Administrative access to most features
- `user` - Standard user access

## User Status

- `active` - User is active and can access the system
- `disabled` - User account is disabled
- `invited` - User has been invited but hasn't accepted yet

## Error Handling

```python
from netbird.exceptions import NetBirdNotFoundError, NetBirdValidationError

try:
    user = client.users.get("invalid-id")
except NetBirdNotFoundError:
    print("User not found")
except NetBirdValidationError as e:
    print(f"Validation error: {e}")
```

## Common Patterns

### Bulk User Creation

```python
users_to_create = [
    {"email": "user1@company.com", "name": "User One"},
    {"email": "user2@company.com", "name": "User Two"},
]

created_users = []
for user_info in users_to_create:
    user_data = UserCreate(**user_info)
    user = client.users.create(user_data)
    created_users.append(user)
    
    # Send invitation
    client.users.invite(user['id'])
```

### Find Users by Email Domain

```python
users = client.users.list()
company_users = [
    user for user in users 
    if user.get('email', '').endswith('@company.com')
]
```

### Filter by Role

```python
users = client.users.list()
admins = [user for user in users if user['role'] in ['admin', 'owner']]
regular_users = [user for user in users if user['role'] == 'user']
```