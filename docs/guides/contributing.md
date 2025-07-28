---
layout: page
title: Contributing Guide
description: How to contribute to the NetBird Python client project
---

# Contributing Guide

We welcome contributions to the NetBird Python client! This guide will help you get started.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/netbird-python-client.git
cd netbird-python-client
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### 3. Verify Setup

```bash
# Run tests to ensure everything works
pytest

# Check code formatting
black --check src/ tests/
isort --check-only src/ tests/

# Run type checking
mypy src/
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/netbird --cov-report=html

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests (requires API token)
```

### 4. Code Quality Checks

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Go to GitHub and create a pull request
- Fill out the PR template
- Link any related issues
- Request review from maintainers

## Code Style Guidelines

### Python Style

We follow PEP 8 with some modifications:

```python
# Good: Clear, descriptive names
def create_user_with_groups(user_data: UserCreate, group_ids: List[str]) -> Dict[str, Any]:
    """Create a user and assign to specified groups."""
    pass

# Good: Type hints
def get_peers_by_status(client: APIClient, connected: bool = True) -> List[Dict[str, Any]]:
    return [peer for peer in client.peers.list() if peer['connected'] == connected]

# Good: Dictionary access for responses
user = client.users.get_current()
print(f"User: {user['name']} ({user['email']})")

# Good: Pydantic models for input
user_data = UserCreate(email="test@example.com", name="Test User")
```

### Documentation Style

```python
def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """Brief description of the function.
    
    Longer description with more details about what the function does,
    any important considerations, and usage examples.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2. Defaults to 10.
        
    Returns:
        Dictionary containing the result data
        
    Raises:
        NetBirdAPIError: When the API request fails
        NetBirdNotFoundError: When the resource is not found
        
    Example:
        >>> result = example_function("test", 20)
        >>> print(result['status'])
        success
    """
    pass
```

## Testing Guidelines

### Unit Tests

- Test individual functions and methods
- Use mocks for external dependencies
- Focus on edge cases and error conditions
- Aim for high coverage (>95%)

```python
def test_user_creation_success(mock_client):
    """Test successful user creation."""
    # Arrange
    user_data = UserCreate(email="test@example.com", name="Test User")
    expected_response = {"id": "user-123", "name": "Test User", "email": "test@example.com"}
    mock_client.post.return_value = expected_response
    
    # Act
    result = client.users.create(user_data)
    
    # Assert
    assert result == expected_response
    mock_client.post.assert_called_once_with(
        "users", 
        data=user_data.model_dump(exclude_unset=True)
    )
```

### Integration Tests

- Test against real API (with proper test environment)
- Test complete workflows
- Include cleanup in finally blocks
- Mark as slow tests

```python
@pytest.mark.integration
@pytest.mark.slow
def test_group_lifecycle(integration_client):
    """Test complete group creation, update, and deletion."""
    group_data = GroupCreate(name="test-group-integration", peers=[])
    created_group = None
    
    try:
        # Create
        created_group = integration_client.groups.create(group_data)
        assert created_group['name'] == "test-group-integration"
        
        # Update
        update_data = GroupUpdate(name="updated-group-name")
        updated_group = integration_client.groups.update(created_group['id'], update_data)
        assert updated_group['name'] == "updated-group-name"
        
    finally:
        # Cleanup
        if created_group:
            try:
                integration_client.groups.delete(created_group['id'])
            except NetBirdAPIError:
                pass  # Ignore cleanup errors
```

## Adding New Features

### 1. New API Resources

When adding support for a new NetBird API resource:

1. **Create the model classes** in `src/netbird/models/`
2. **Create the resource handler** in `src/netbird/resources/`
3. **Add to client** in `src/netbird/client.py`
4. **Write comprehensive tests**
5. **Update documentation**

Example structure:

```python
# src/netbird/models/new_resource.py
from pydantic import BaseModel
from typing import Optional

class NewResource(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class NewResourceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class NewResourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
```

### 2. New Methods

When adding new methods to existing resources:

1. **Follow existing patterns** for method signatures
2. **Use proper type hints** for parameters and returns
3. **Add comprehensive docstrings** with examples
4. **Write tests** for success and error cases
5. **Update API documentation**

### 3. Bug Fixes

1. **Create a test** that reproduces the bug
2. **Fix the issue** with minimal changes
3. **Ensure the test passes**
4. **Check for similar issues** elsewhere in the codebase

## Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include examples in docstrings
- Document all parameters and return values
- Explain any complex logic

### API Documentation

When updating the API documentation:

1. **Update method signatures** in the API reference
2. **Add new examples** to the examples section
3. **Update the changelog** with your changes
4. **Test documentation locally** before submitting

```bash
# Test documentation locally
cd docs/
bundle exec jekyll serve
# Visit http://localhost:4000 to preview
```

## Release Process

### Version Numbering

We use semantic versioning (semver):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes, backwards compatible

### Changelog

Update `CHANGELOG.md` with your changes:

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description

### Deprecated
- Deprecated feature description

### Removed
- Removed feature description

### Security
- Security improvement description
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Assume good intentions

### Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Pull Requests**: Code contributions

### Getting Help

If you need help contributing:

1. **Check existing issues** and discussions
2. **Read the documentation** thoroughly
3. **Ask questions** in GitHub Discussions
4. **Reach out to maintainers** if needed

## Recognition

Contributors will be recognized in:

- Repository README
- Release notes
- Documentation credits

Thank you for contributing to the NetBird Python client! 🚀

## Quick Reference

### Useful Commands

```bash
# Development setup
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/netbird --cov-report=html

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Build documentation
cd docs && bundle exec jekyll serve

# Build package
python -m build
```

### Branch Naming

- `feature/feature-name` - New features
- `bugfix/issue-description` - Bug fixes
- `docs/documentation-update` - Documentation updates
- `refactor/code-improvement` - Code improvements

### Commit Messages

Follow conventional commits:

- `feat: add new feature`
- `fix: resolve bug in user creation`
- `docs: update API documentation`
- `test: add integration tests for groups`
- `refactor: improve error handling`
- `chore: update dependencies`