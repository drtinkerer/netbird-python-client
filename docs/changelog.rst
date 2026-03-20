Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.1.0] - 2025-08-01
---------------------

Added
~~~~~
- Python 3.13 support
- Built-in network diagram generation with ``client.generate_diagram()``
- Support for multiple diagram formats (Mermaid, Graphviz, Python Diagrams)
- Network topology optimization and visualization
- Comprehensive test coverage (98.01%)
- Modern Sphinx documentation with Furo theme

Changed
~~~~~~~
- Migrated from standalone diagram script to integrated client method
- Updated documentation theme from Jekyll to modern Sphinx + Furo
- Enhanced error handling with specific exception types
- Improved type safety with strict mypy compliance

Fixed
~~~~~
- Type checking issues in GitHub Actions pipeline
- Import formatting and linting compliance
- Optional dependency handling for diagram generation

[1.0.0] - 2024-12-01
---------------------

Added
~~~~~
- Initial release of NetBird Python client
- Complete API coverage for all NetBird resources
- Pydantic models for type safety
- Comprehensive error handling
- Integration and unit tests
- Basic documentation

Features
~~~~~~~~
- Support for all NetBird API endpoints
- Clean dictionary responses
- Token-based authentication
- Self-hosted and cloud NetBird support
- Python 3.9+ compatibility