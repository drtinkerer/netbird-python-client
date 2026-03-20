Contributing
============

We welcome contributions to the NetBird Python client! This guide will help you get started.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   .. code-block:: bash

      git clone https://github.com/YOUR-USERNAME/netbird-python-client.git
      cd netbird-python-client

3. **Install development dependencies**:

   .. code-block:: bash

      pip install -e ".[dev,docs]"

4. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

Development Workflow
--------------------

Code Style
~~~~~~~~~~

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run all checks:

.. code-block:: bash

   # Format code
   black src/ tests/
   isort src/ tests/
   
   # Run linting
   flake8 src/ tests/
   
   # Run type checking
   mypy src/

Testing
~~~~~~~

We maintain exceptional test coverage (98.01%). All new code should include tests.

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage report
   pytest --cov=src/netbird --cov-report=html
   
   # Run specific test categories
   pytest tests/unit/          # Unit tests only
   pytest tests/integration/   # Integration tests only

Documentation
~~~~~~~~~~~~~

Documentation is built with Sphinx and the Furo theme:

.. code-block:: bash

   # Build documentation
   cd docs
   make html
   
   # Live reload during development
   make livehtml
   
   # Check for broken links
   make linkcheck

Contribution Guidelines
-----------------------

Issues
~~~~~~

- **Search existing issues** before creating a new one
- **Use issue templates** when available
- **Provide clear reproduction steps** for bugs
- **Include version information** and environment details

Pull Requests
~~~~~~~~~~~~~

1. **Create a feature branch** from main:

   .. code-block:: bash

      git checkout -b feature/amazing-feature

2. **Make your changes** with appropriate tests
3. **Run the test suite** to ensure everything passes
4. **Update documentation** if needed
5. **Commit your changes** with clear commit messages:

   .. code-block:: bash

      git commit -m "Add amazing feature"

6. **Push to your fork**:

   .. code-block:: bash

      git push origin feature/amazing-feature

7. **Create a Pull Request** on GitHub

Commit Messages
~~~~~~~~~~~~~~~

Follow these guidelines for commit messages:

- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Reference issues and pull requests when applicable
- Include more details in the body if needed

Code Guidelines
---------------

General Principles
~~~~~~~~~~~~~~~~~~

- **Follow existing patterns** in the codebase
- **Write clear, readable code** with descriptive names
- **Add docstrings** to all public functions and classes
- **Include type hints** for all function parameters and return values
- **Handle errors gracefully** with appropriate exceptions

API Design
~~~~~~~~~~

- **Input validation**: Use Pydantic models for type safety
- **Response format**: Return standard Python dictionaries
- **Error handling**: Raise specific exception types
- **Documentation**: Include examples in docstrings

Testing Guidelines
~~~~~~~~~~~~~~~~~~

- **Write tests for all new functionality**
- **Include both positive and negative test cases**
- **Mock external dependencies** in unit tests
- **Use descriptive test names** that explain what is being tested
- **Group related tests** in the same test class

Documentation Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

- **Keep documentation up to date** with code changes
- **Include practical examples** in API documentation
- **Write clear, concise explanations**
- **Use proper reStructuredText formatting**

Release Process
---------------

The project follows semantic versioning (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Releases are handled by maintainers and include:

1. Version bump in ``src/netbird/__init__.py``
2. Updated ``CHANGELOG.md``
3. GitHub release with release notes
4. PyPI package publication

Community
---------

- **Be respectful** and constructive in all interactions
- **Help others** when you can
- **Ask questions** if something is unclear
- **Share knowledge** and best practices

Getting Help
------------

If you need help with contributing:

- **Check existing issues** and discussions
- **Join the NetBird community** discussions
- **Open an issue** with your question
- **Contact maintainers** if needed

Thank you for contributing to the NetBird Python client! 🎉