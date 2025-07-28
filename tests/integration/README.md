# Integration Tests Guide

## What Are Integration Tests?

Integration tests verify that your NetBird Python client works correctly with a **real NetBird server**. Unlike unit tests that use mocks, these tests make actual API calls and verify real responses.

## Setup Required

### 1. Environment Variables
```bash
# Required: Your NetBird API token
export NETBIRD_TEST_TOKEN="your-actual-netbird-api-token-here"

# Optional: NetBird server host (defaults to api.netbird.io)
export NETBIRD_TEST_HOST="your-netbird-instance.com"
```

### 2. Get Your API Token
1. Log into your NetBird dashboard
2. Go to **Settings** → **Access Tokens**
3. Create a new token with appropriate permissions
4. Copy the token value

## Running Integration Tests

### Run All Integration Tests
```bash
# Run all integration tests
pytest tests/integration/ -v -m integration

# Run with more detailed output
pytest tests/integration/ -v -s -m integration
```

### Run Specific Test Files
```bash
# Run only read-only tests (safe)
pytest tests/integration/test_basic_integration.py -v

# Run CRUD tests (modifies data - use test environment!)
pytest tests/integration/test_crud_integration.py -v
```

### Run by Test Type
```bash
# Run only slow tests
pytest -m "integration and slow" -v

# Run only safe read-only tests
pytest -m "integration and not slow" -v
```

## Test Categories

### 1. Basic Integration Tests (`test_basic_integration.py`)
- **Read-only operations** - Safe to run on any environment
- Tests data retrieval: users, peers, groups, etc.
- Validates data structure and types
- Tests error handling with real API responses

**Example:**
```python
def test_get_current_user(self, integration_client):
    user = integration_client.users.get_current()  # Real API call
    
    assert user['id'] is not None
    assert user['email'] is not None
    assert user['role'] in ["admin", "user", "owner"]
```

### 2. CRUD Integration Tests (`test_crud_integration.py`) 
- **Modifies data** - Only run on test environments!
- Tests create, read, update, delete operations
- Tests data consistency across operations
- Tests real error scenarios

**Example:**
```python
def test_group_lifecycle(self, integration_client):
    # CREATE
    group_data = GroupCreate(name="test-group", peers=[])
    created_group = integration_client.groups.create(group_data)
    
    # READ
    fetched_group = integration_client.groups.get(created_group['id'])
    
    # UPDATE
    update_data = GroupUpdate(name="updated-name")
    updated_group = integration_client.groups.update(created_group['id'], update_data)
    
    # DELETE
    integration_client.groups.delete(created_group['id'])
```

## Response Format (Important!)

The NetBird Python client uses **dictionary responses** (boto3 style):

```python
# API responses are dictionaries
user = client.users.get_current()
print(user['name'])          # Dictionary access
print(user['email'])         # Familiar AWS SDK patterns
print(user.get('role'))      # Safe access with .get()

# Input validation still uses Pydantic models
user_data = UserCreate(email="test@example.com", name="Test User")
created_user = client.users.create(user_data)
print(f"Created: {created_user['name']}")  # Response is a dictionary
```

## Key Differences from Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|------------|-------------------|
| **Speed** | Fast (milliseconds) | Slow (seconds) |
| **Dependencies** | None (uses mocks) | Real NetBird server |
| **Data** | Fake/mocked data | Real API responses |
| **Side Effects** | None | Can modify server data |
| **Environment** | Any | Requires test server |
| **Purpose** | Test code logic | Test real integration |
| **Response Format** | Mock dictionaries | Real API dictionaries |

## Best Practices

### 1. Use Test Environment
- **Never run CRUD tests on production!**
- Use a dedicated test NetBird instance
- Or use a test account with disposable data

### 2. Test Data Cleanup
- Always clean up created resources in `finally` blocks
- Use unique names (UUID) to avoid conflicts
- Handle cleanup failures gracefully

### 3. Error Handling
- Test both success and error scenarios
- Verify specific exception types
- Test edge cases that only appear with real data

### 4. Idempotent Tests
- Tests should be able to run multiple times
- Don't depend on specific server state
- Handle cases where test data already exists

## Example: Running Your First Integration Test

1. **Set your token:**
```bash
export NETBIRD_TEST_TOKEN="nb_1234567890abcdef"
```

2. **Run a safe test:**
```bash
pytest tests/integration/test_basic_integration.py::TestBasicIntegration::test_get_current_user -v
```

3. **Expected output:**
```
tests/integration/test_basic_integration.py::TestBasicIntegration::test_get_current_user PASSED
```

If you see `SKIPPED`, it means `NETBIRD_TEST_TOKEN` is not set.
If you see `FAILED`, check your token and network connection.

## Debugging Integration Tests

### Check Token
```python
import os
from netbird import APIClient

token = os.getenv("NETBIRD_TEST_TOKEN")
client = APIClient(host="api.netbird.io", api_token=token)

try:
    user = client.users.get_current()
    print(f"Token works! User: {user['email']}")
except Exception as e:
    print(f"Token error: {e}")
```

### Verbose Output
```bash
pytest tests/integration/ -v -s --tb=long
```

This will show detailed error messages and print statements.