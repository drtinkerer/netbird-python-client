NetBird Python Client
=====================

.. warning::
   This is an **unofficial**, community-maintained client library. It is **not affiliated with, endorsed by, or officially supported** by NetBird or the NetBird team. For official NetBird tools and support, please visit `netbird.io <https://netbird.io>`_.

**Unofficial** Python client library for the `NetBird <https://netbird.io>`_ API. Provides complete access to all NetBird API resources with a simple, intuitive interface.

.. grid:: 2

    .. grid-item-card:: 🚀 Quick Start
        :link: quickstart
        :link-type: doc

        Get up and running with NetBird Python client in minutes

    .. grid-item-card:: 📖 API Reference  
        :link: api/index
        :link-type: doc

        Complete API documentation for all resources

    .. grid-item-card:: 💡 Examples
        :link: examples/index
        :link-type: doc

        Practical examples and use cases

    .. grid-item-card:: 🔧 Installation
        :link: installation
        :link-type: doc

        Installation guide and requirements

Features
--------

.. grid:: 3

    .. grid-item-card:: ✅ Complete API Coverage
        
        All 11 NetBird API resources supported

    .. grid-item-card:: ✅ Type Safety
        
        Pydantic models for input validation

    .. grid-item-card:: ✅ Network Visualization
        
        Built-in diagram generation

    .. grid-item-card:: ✅ Modern Python
        
        Python 3.9+ (supports 3.9-3.13)

    .. grid-item-card:: ✅ Exceptional Coverage
        
        98.01% test coverage

    .. grid-item-card:: ✅ Easy to Use
        
        Clean dictionary responses

Installation
------------

.. code-block:: bash

   pip install netbird

Quick Example
-------------

.. code-block:: python

   from netbird import APIClient
   
   # Initialize the client
   client = APIClient(
       host="your-netbird-host.com",
       api_token="your-api-token-here"
   )
   
   # List all peers
   peers = client.peers.list()
   print(f"Found {len(peers)} peers")
   
   # Generate network diagram
   diagram = client.generate_diagram(format="mermaid")
   print(diagram)

Supported Resources
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Resource
     - Description  
     - Endpoints
   * - **Accounts**
     - Account management and settings
     - List, Update, Delete
   * - **Users**
     - User lifecycle management
     - CRUD + Invite, Current user
   * - **Tokens**
     - API token management
     - CRUD operations
   * - **Peers**
     - Network peer management
     - CRUD + Accessible peers
   * - **Setup Keys**
     - Peer setup key management
     - CRUD operations
   * - **Groups**
     - Peer group management
     - CRUD operations
   * - **Networks**
     - Network and resource management
     - CRUD + Resources/Routers
   * - **Policies**
     - Access control policies
     - CRUD operations
   * - **Routes**
     - Network routing configuration
     - CRUD operations
   * - **DNS**
     - DNS settings and nameservers
     - Nameserver groups + Settings
   * - **Events**
     - Audit and traffic events
     - Audit logs, Network traffic

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting Started

   installation
   quickstart
   
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: User Guide
   
   user-guide/authentication
   user-guide/network-visualization
   user-guide/error-handling

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: API Reference
   
   api/index
   api/client
   api/resources
   api/models
   api/exceptions

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Examples
   
   examples/index
   examples/user-management
   examples/network-management
   examples/diagrams

.. toctree::
   :maxdepth: 1  
   :hidden:
   :caption: Development
   
   contributing
   changelog