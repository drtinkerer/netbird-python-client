# Contributing to NetBird Python Client

Thank you for your interest in contributing to the NetBird Python Client! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows the NetBird community standards. Please be respectful and inclusive in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A NetBird account with API access (for integration testing)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/netbird-python-client.git
   cd netbird-python-client
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Verify setup**
   ```bash
   pytest --version
   mypy --version
   black --version
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-async-support` - New features
- `fix/authentication-error` - Bug fixes
- `docs/api-reference-update` - Documentation updates
- `refactor/client-structure` - Code refactoring

### Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code structure
   - Add type hints to all functions
   - Include docstrings for public methods
   - Update relevant documentation

3. **Add tests**
   - Write unit tests for new functionality
   - Ensure existing tests still pass
   - Aim for high test coverage

4. **Run quality checks**
   ```bash
   # Run tests
   pytest
   
   # Type checking
   mypy src/
   
   # Code formatting
   black src/ tests/
   isort src/ tests/
   
   # Linting
   flake8 src/ tests/
   ```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/netbird --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration

# Run tests for specific module
pytest tests/test_client.py
```

### Test Structure

- `tests/unit/` - Unit tests that don't require external dependencies
- `tests/integration/` - Integration tests that interact with the NetBird API
- `tests/fixtures/` - Test data and fixtures

### Writing Tests

1. **Unit Tests**
   ```python
   import pytest
   from netbird import APIClient
   from netbird.exceptions import NetBirdAuthenticationError
   
   def test_client_initialization():
       client = APIClient(host="example.com", api_token="test-token")
       assert client.host == "example.com"
   
   def test_invalid_token_raises_error():
       with pytest.raises(NetBirdAuthenticationError):
           # Test authentication error handling
           pass
   ```

2. **Integration Tests**
   ```python
   import os
   import pytest
   from netbird import APIClient
   
   @pytest.fixture
   def client():
       api_token = os.getenv("NETBIRD_TEST_TOKEN")
       if not api_token:
           pytest.skip("NETBIRD_TEST_TOKEN not set")
       return APIClient(host="api.netbird.io", api_token=api_token)
   
   @pytest.mark.integration
   def test_list_users(client):
       users = client.users.list()
       assert isinstance(users, list)
   ```

### Test Environment Variables

For integration tests, set these environment variables:
```bash
export NETBIRD_TEST_TOKEN="your-test-api-token"
export NETBIRD_TEST_HOST="api.netbird.io"  # Optional
```

## Code Style

### Python Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Style Guidelines

1. **Type Hints**
   ```python
   from typing import List, Optional
   
   def get_users(self, active_only: bool = False) -> List[User]:
       \"\"\"Get list of users.
       
       Args:
           active_only: Filter for active users only
           
       Returns:
           List of User objects
       \"\"\"
   ```

2. **Docstrings**
   ```python
   def create_user(self, user_data: UserCreate) -> User:
       \"\"\"Create a new user.
       
       Args:
           user_data: User creation data
           
       Returns:
           Created User object
           
       Raises:
           NetBirdValidationError: If user data is invalid
           NetBirdAPIError: If creation fails
           
       Example:
           >>> user_data = UserCreate(email="test@example.com", name="Test User")
           >>> user = client.users.create(user_data)
       \"\"\"
   ```

3. **Error Handling**
   ```python
   try:
       response = self.client.get(f"users/{user_id}")
       return self._parse_response(response, User)
   except HTTPError as e:
       if e.response.status_code == 404:
           raise NetBirdNotFoundError(f"User {user_id} not found")
       raise NetBirdAPIError(f"Failed to get user: {e}")
   ```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Submitting Changes

### Pull Request Process

1. **Ensure your code passes all checks**
   ```bash
   pytest
   mypy src/
   black --check src/ tests/
   isort --check-only src/ tests/
   flake8 src/ tests/
   ```

2. **Update documentation**
   - Update docstrings for new/changed methods
   - Update README if needed
   - Add examples for new features

3. **Create a pull request**
   - Write a clear title and description
   - Reference any related issues
   - Include examples of new functionality

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. All conversations must be resolved
4. No merge conflicts

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Package version
   - Operating system

2. **Steps to Reproduce**
   ```python
   # Minimal code example
   from netbird import APIClient
   client = APIClient(host="api.netbird.io", api_token="token")
   # Steps that cause the issue
   ```

3. **Expected vs Actual Behavior**
   - What you expected to happen
   - What actually happened
   - Error messages or stack traces

4. **Additional Context**
   - Any other relevant information

### Feature Requests

For feature requests, please provide:

1. **Use Case**: Describe the problem you're trying to solve
2. **Proposed Solution**: How you think it should work
3. **Alternatives**: Other solutions you've considered
4. **Additional Context**: Any other relevant information

## Getting Help

- **GitHub Discussions**: For general questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **NetBird Community**: Join the broader NetBird community

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes for major features

Thank you for contributing to the NetBird Python Client! 🚀