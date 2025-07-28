# Test Fixtures

This directory contains test fixtures following industry standards for maintainable test suites.

## Directory Structure

```
fixtures/
├── __init__.py              # Fixture loader utilities
├── README.md               # This documentation
├── api_responses/          # Mock API response data
│   ├── users.json
│   ├── peers.json
│   ├── groups.json
│   ├── accounts.json
│   ├── setup_keys.json
│   └── policies.json
├── sample_data/           # Individual resource samples
│   ├── user.json
│   ├── peer.json
│   └── group.json
└── mock_configs/          # Configuration files
    ├── client.yaml
    └── auth.yaml
```

## Benefits of File-Based Fixtures

### ✅ Industry Standard Approach
- **Maintainable**: Centralized test data
- **Reusable**: Same data across multiple tests
- **Readable**: JSON/YAML is easier to read than Python dicts
- **Realistic**: Can store real API response samples
- **Version Control**: Track changes to test data

### ✅ vs Inline Test Data
**Before (inline data):**
```python
def test_user():
    user_data = {
        "id": "user-123",
        "email": "test@example.com",
        # ... 20 more lines of data
    }
```

**After (fixture files):**
```python
def test_user():
    user_data = load_sample_data("user")
```

## Usage Examples

### 1. Loading Individual Resources
```python
from tests.fixtures import load_sample_data

# Load single resource data
user_data = load_sample_data("user")
peer_data = load_sample_data("peer")
group_data = load_sample_data("group")
```

### 2. Loading API Responses
```python
from tests.fixtures import load_api_response

# Load complete API response arrays
users_list = load_api_response("users")
peers_list = load_api_response("peers")
```

### 3. Loading Configurations
```python
from tests.fixtures import load_mock_config

# Load YAML configuration files
client_config = load_mock_config("client")
auth_config = load_mock_config("auth")

# Access nested configuration
default_client = client_config["default_client"]
token = auth_config["token_auth"]["valid_token"]
```

### 4. Using with Pytest Fixtures
```python
# In conftest.py
@pytest.fixture
def sample_user_data():
    return load_sample_data("user")

# In test files - for response validation
def test_user_response(sample_user_data):
    # Fixtures contain dictionary data (like API responses)
    assert isinstance(sample_user_data, dict)
    assert sample_user_data['email'] == "test@example.com"
    assert 'id' in sample_user_data
    
    # For input validation, use Pydantic models
    user_create = UserCreate(**sample_user_data)
    assert user_create.email == "test@example.com"
```

## File Formats

### JSON Files (api_responses/, sample_data/)
- **Purpose**: Store realistic API response data as dictionaries (boto3 style)
- **Usage**: Response validation, API response mocking, dictionary access testing
- **Format**: Standard Python dictionaries matching actual API responses
- **Example**: `api_responses/users.json`

### YAML Files (mock_configs/)
- **Purpose**: Configuration data, environment settings
- **Usage**: Client configuration, authentication scenarios
- **Example**: `mock_configs/client.yaml`

## Adding New Fixtures

### 1. Add New JSON Fixture
```bash
# Create new API response fixture
echo '{"id": "route-123", "network": "10.0.0.0/24"}' > fixtures/api_responses/routes.json
```

### 2. Add New Configuration
```yaml
# fixtures/mock_configs/new_config.yaml
feature_flags:
  enable_new_feature: true
  debug_mode: false
```

### 3. Use in Tests
```python
# Load the new fixtures
routes = load_api_response("routes")
config = load_mock_config("new_config")
```

## Best Practices

### ✅ Do
- Store large/complex test data in fixture files
- Use realistic data that matches actual API responses
- Group related fixtures in subdirectories
- Document fixture file purposes
- Keep fixture files up-to-date with API changes

### ❌ Don't
- Store simple test data (2-3 fields) in files
- Hardcode file paths - use the loader utilities
- Mix test logic with fixture data
- Create duplicate fixture data

## Testing the Fixtures

Run the fixture demonstration tests:
```bash
pytest tests/unit/test_fixtures_demo.py -v
```

This validates:
- ✅ All fixture files load correctly
- ✅ Data formats match model schemas
- ✅ Configuration files are valid YAML
- ✅ Integration with pytest fixtures works

## Real API Data

The fixture files contain realistic data structures based on actual NetBird API responses, including:

- **Geographic data**: `city_name`, `country_code`, `geoname_id`
- **System information**: `kernel_version`, `os`, `version`
- **Network details**: `accessible_peers_count`, `dns_label`
- **Timestamps**: ISO 8601 formatted dates
- **Nested objects**: Groups with peer details, policy rules

This ensures your tests work with data structures that match production.