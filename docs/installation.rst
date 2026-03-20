Installation
============

This page covers the installation of the NetBird Python client library.

Requirements
------------

- Python 3.9 or higher (supports Python 3.9-3.13)
- NetBird API access (cloud or self-hosted)

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Python Version
     - Support Status
   * - 3.9
     - ✅ Fully Supported
   * - 3.10
     - ✅ Fully Supported  
   * - 3.11
     - ✅ Fully Supported
   * - 3.12
     - ✅ Fully Supported
   * - 3.13
     - ✅ Fully Supported

Basic Installation
------------------

Install from PyPI using pip:

.. code-block:: bash

   pip install netbird

This will install the core NetBird client with all required dependencies.

Development Installation
------------------------

If you want to contribute to the project or run the latest development version:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/drtinkerer/netbird-python-client.git
   cd netbird-python-client
   
   # Install in development mode with all dependencies
   pip install -e ".[dev,docs]"

Optional Dependencies
---------------------

The NetBird client includes optional dependencies for enhanced functionality:

Network Visualization
~~~~~~~~~~~~~~~~~~~~~

For generating network topology diagrams:

.. code-block:: bash

   # For Graphviz diagrams (PNG, SVG, PDF)
   pip install graphviz
   
   # For Python Diagrams (architectural diagrams)
   pip install diagrams

Development Tools
~~~~~~~~~~~~~~~~~

For development and testing:

.. code-block:: bash

   # Install development dependencies
   pip install netbird[dev]

This includes:

- pytest (testing framework)
- black (code formatting)
- isort (import sorting)
- mypy (type checking)  
- flake8 (linting)
- pre-commit (git hooks)

Documentation
~~~~~~~~~~~~~

For building documentation:

.. code-block:: bash

   # Install documentation dependencies
   pip install netbird[docs]

This includes:

- Sphinx (documentation generator)
- Furo (modern documentation theme)
- MyST Parser (Markdown support)
- sphinx-design (UI components)

Verification
------------

Verify your installation by running:

.. code-block:: python

   import netbird
   print(netbird.__version__)

You should see the version number printed without any errors.

Common Issues
-------------

Import Errors
~~~~~~~~~~~~~

If you encounter import errors, make sure you have installed the package correctly:

.. code-block:: bash

   pip install --upgrade netbird

Missing Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you get errors when trying to generate diagrams:

.. code-block:: bash

   # For graphviz errors
   pip install graphviz
   
   # For diagrams errors  
   pip install diagrams

Python Version Issues
~~~~~~~~~~~~~~~~~~~~~

If you're using an unsupported Python version, upgrade to Python 3.9+:

.. code-block:: bash

   # Check your Python version
   python --version
   
   # Upgrade Python using your system package manager
   # or download from https://www.python.org/downloads/

Virtual Environments
--------------------

It's recommended to use virtual environments to avoid dependency conflicts:

.. code-block:: bash

   # Create a virtual environment
   python -m venv netbird-env
   
   # Activate it (Linux/macOS)
   source netbird-env/bin/activate
   
   # Activate it (Windows)
   netbird-env\Scripts\activate
   
   # Install NetBird
   pip install netbird

Next Steps
----------

After installation, check out the :doc:`quickstart` guide to start using the NetBird Python client.