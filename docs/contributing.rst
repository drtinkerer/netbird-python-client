Contributing
============

We welcome contributions to the NetBird Python client!

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork the repository** on GitHub
2. **Clone your fork**:

   .. code-block:: bash

      git clone https://github.com/YOUR-USERNAME/netbird-python-client.git
      cd netbird-python-client

3. **Install development dependencies**:

   .. code-block:: bash

      pip install -e ".[dev,docs]"

4. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

Code Quality
------------

We enforce code quality with automated tools:

- **Black** - Code formatting (line length: 88)
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Strict type checking

Run all checks:

.. code-block:: bash

   black src/ tests/
   isort src/ tests/
   flake8 src/ tests/
   mypy src/

Testing
-------

We maintain 88% test coverage with 364+ unit tests.

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=src/netbird --cov-report=html

   # Run specific categories
   pytest tests/unit/           # Core resource tests
   pytest tests/unit/cloud/     # Cloud resource tests

All new code should include tests. Use ``pytest.mark.unit`` for unit tests.

API Design Principles
---------------------

- **Input validation**: Use Pydantic models (``ResourceCreate``, ``ResourceUpdate``)
- **Response format**: Return standard Python dictionaries
- **Error handling**: Raise specific exception types from ``netbird.exceptions``
- **Forward compatibility**: Use ``extra="allow"`` on all models

Documentation
-------------

Documentation is built with Sphinx and the Furo theme:

.. code-block:: bash

   cd docs
   make html          # Build HTML docs
   make livehtml      # Live reload during development
   make linkcheck     # Check for broken links

Pull Requests
-------------

1. Create a feature branch from ``main``
2. Make changes with tests
3. Run the full test suite
4. Update documentation if needed
5. Submit a Pull Request

Commit messages should use imperative mood ("Add feature", not "Added feature").

Release Process
---------------

Releases follow semantic versioning:

1. Version bump in ``src/netbird/__init__.py``
2. Update ``CHANGELOG.md``
3. Create GitHub release with notes
4. PyPI package is published automatically

Getting Help
------------

- Check `existing issues <https://github.com/drtinkerer/netbird-python-client/issues>`_
- Open a new issue with your question
- See the `full documentation <https://drtinkerer.github.io/netbird-python-client/>`_
