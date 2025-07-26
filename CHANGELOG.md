# Changelog

All notable changes to the NetBird Python Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - TBD

### Added
- Initial release of NetBird Python Client
- Complete API coverage for all 11 NetBird API resources:
  - Accounts - Account management and settings
  - Users - User lifecycle management with roles and permissions
  - Tokens - API token management for users
  - Peers - Network peer management and connectivity
  - Setup Keys - Peer setup key management with auto-groups
  - Groups - Peer group management and organization
  - Networks - Network and resource management with nested resources
  - Policies - Access control policies with rules and posture checks
  - Routes - Network routing configuration with masquerading
  - DNS - DNS settings and nameserver group management
  - Events - Audit events and network traffic monitoring
- Modern Python package structure with pyproject.toml
- Type-safe Pydantic models for all API objects
- Comprehensive error handling with specific exception types:
  - `NetBirdAPIError` - Base exception for all API errors
  - `NetBirdAuthenticationError` - Authentication failures (401)
  - `NetBirdValidationError` - Request validation errors (400)
  - `NetBirdNotFoundError` - Resource not found errors (404)
  - `NetBirdRateLimitError` - Rate limiting errors (429)
  - `NetBirdServerError` - Server errors (5xx)
- Flexible authentication support:
  - Personal access tokens
  - Service user tokens
  - Bearer token authentication
- HTTP client with proper timeout and error handling
- Context manager support for resource cleanup
- Extensive documentation and examples:
  - Complete README with usage examples
  - API reference documentation
  - Practical example scripts
  - Type hints and docstrings throughout
- Development tooling:
  - pytest for testing with coverage reporting
  - mypy for type checking
  - black for code formatting
  - isort for import sorting
  - flake8 for linting
  - pre-commit hooks for code quality

### Features
- **Complete Resource Coverage**: Support for all NetBird API endpoints
- **Type Safety**: Full typing support with runtime validation
- **Error Handling**: Comprehensive exception hierarchy for different error types
- **Authentication**: Multiple authentication methods supported
- **Documentation**: Extensive docs with practical examples
- **Modern Python**: Built for Python 3.8+ with modern packaging
- **Developer Experience**: Rich tooling and clear error messages

### Examples Included
- `basic_client.py` - Basic API usage and resource listing
- `user_management.py` - User creation, tokens, and role management
- `network_automation.py` - Complete network setup automation

### Development
- Modern pyproject.toml configuration
- Comprehensive test suite setup
- Type checking with mypy
- Code formatting with black and isort
- Linting with flake8
- Coverage reporting with pytest-cov

---

## Release Notes

### Version 0.1.0
This is the initial release of the NetBird Python Client. It provides complete coverage of the NetBird API with a focus on developer experience, type safety, and comprehensive documentation.

**Key Highlights:**
- 🎯 **Complete API Coverage** - All 11 NetBird resources supported
- 🔒 **Type Safe** - Full Pydantic model validation
- 📚 **Well Documented** - Extensive docs and examples
- 🚀 **Production Ready** - Proper error handling and testing
- 🐍 **Modern Python** - Built for Python 3.8+ with best practices

The client is designed to be intuitive for NetBird users while providing the flexibility needed for automation and integration scenarios.