Installation
============

Requirements
------------

- Python 3.10 or higher (supports Python 3.10-3.14)
- NetBird API access (cloud or self-hosted)

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Python Version
     - Support Status
   * - 3.10
     - Fully Supported
   * - 3.11
     - Fully Supported
   * - 3.12
     - Fully Supported
   * - 3.13
     - Fully Supported
   * - 3.14
     - Fully Supported

Basic Installation
------------------

Install from PyPI using pip:

.. code-block:: bash

   pip install netbird

This installs the core NetBird client with required dependencies:

- `httpx <https://www.python-httpx.org/>`_ - HTTP client
- `pydantic <https://docs.pydantic.dev/>`_ - Data validation
- `typing-extensions <https://pypi.org/project/typing-extensions/>`_ - Type hints

Development Installation
------------------------

To contribute or run the latest development version:

.. code-block:: bash

   git clone https://github.com/drtinkerer/netbird-python-client.git
   cd netbird-python-client

   # Install in development mode with all dependencies
   pip install -e ".[dev,docs]"

Optional Dependencies
---------------------

Network Visualization
~~~~~~~~~~~~~~~~~~~~~

For generating network topology diagrams:

.. code-block:: bash

   # For Graphviz diagrams (PNG, SVG, PDF)
   pip install graphviz

   # For Python Diagrams (architectural diagrams)
   pip install diagrams

   # Mermaid requires no additional Python dependencies

MCP Server (AI Assistants)
~~~~~~~~~~~~~~~~~~~~~~~~~~

To use NetBird with AI assistants via the Model Context Protocol:

.. code-block:: bash

   pip install "netbird[mcp]"

This installs `mcp[cli] <https://pypi.org/project/mcp/>`_ and the ``netbird-mcp`` CLI entry point.
See :doc:`user-guide/mcp-server` for setup instructions.

Development Tools
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install netbird[dev]

Includes: pytest, black, isort, mypy, flake8, pre-commit.

Documentation
~~~~~~~~~~~~~

.. code-block:: bash

   pip install netbird[docs]

Includes: Sphinx, Furo theme, MyST Parser, sphinx-design, sphinx-copybutton, sphinx-tabs.

Verification
------------

.. code-block:: python

   import netbird
   print(netbird.__version__)  # Should print "1.3.0"

Virtual Environments
--------------------

.. code-block:: bash

   python -m venv netbird-env
   source netbird-env/bin/activate   # Linux/macOS
   # netbird-env\Scripts\activate    # Windows
   pip install netbird

Common Issues
-------------

Import Errors
~~~~~~~~~~~~~

.. code-block:: bash

   pip install --upgrade netbird

Missing Diagram Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install graphviz diagrams

On macOS, Graphviz also requires the system package:

.. code-block:: bash

   brew install graphviz

Next Steps
----------

After installation, check out the :doc:`quickstart` guide.
