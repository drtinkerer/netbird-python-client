Quick Start
===========

This guide will help you get started with the NetBird Python client in just a few minutes.

Installation
------------

Install the NetBird Python client using pip:

.. code-block:: bash

   pip install netbird

Basic Usage
-----------

Here's how to get started with the basic functionality:

.. code-block:: python

   from netbird import APIClient
   
   # Initialize the client
   client = APIClient(
       host="your-netbird-host.com",  # e.g., "api.netbird.io" for cloud
       api_token="your-api-token-here"
   )
   
   # Get current user info
   user = client.users.get_current()
   print(f"Logged in as: {user['name']} ({user['email']})")
   
   # List all peers
   peers = client.peers.list()
   print(f"Found {len(peers)} peers")
   
   # List all groups
   groups = client.groups.list()
   for group in groups:
       print(f"Group: {group['name']} ({len(group['peers'])} peers)")

Authentication
--------------

NetBird uses token-based authentication. You can get your API token from:

- **NetBird Cloud**: Dashboard → Settings → API Tokens
- **Self-hosted**: Your NetBird management interface

.. tabs::

   .. tab:: NetBird Cloud

      .. code-block:: python

         client = APIClient(
             host="api.netbird.io",  # For NetBird Cloud
             api_token="your-api-token"
         )

   .. tab:: Self-hosted NetBird

      .. code-block:: python

         client = APIClient(
             host="netbird.yourcompany.com:33073",
             api_token="your-api-token"
         )

Common Operations
-----------------

User Management
~~~~~~~~~~~~~~~

.. code-block:: python

   from netbird.models import UserCreate, UserRole
   
   # Create a new user
   user_data = UserCreate(
       email="user@company.com",
       name="New User",
       role=UserRole.USER,
       auto_groups=["group-default"]
   )
   user = client.users.create(user_data)
   print(f"Created user: {user['name']}")

Group Management
~~~~~~~~~~~~~~~~

.. code-block:: python

   from netbird.models import GroupCreate
   
   # Create a new group
   group_data = GroupCreate(
       name="My Team",
       peers=["peer-1", "peer-2"]
   )
   group = client.groups.create(group_data)
   print(f"Created group: {group['name']}")

Network Visualization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Generate a Mermaid diagram
   mermaid_content = client.generate_diagram(format="mermaid")
   print(mermaid_content)
   
   # Generate a Graphviz diagram (saves as PNG)
   client.generate_diagram(format="graphviz", output_file="my_network")
   
   # Generate a Python Diagrams visualization  
   client.generate_diagram(format="diagrams", output_file="network_topology")

Error Handling
--------------

The client provides specific exception types for different error conditions:

.. code-block:: python

   from netbird.exceptions import (
       NetBirdAPIError,
       NetBirdAuthenticationError,
       NetBirdNotFoundError,
       NetBirdRateLimitError
   )
   
   try:
       user = client.users.get("invalid-user-id")
   except NetBirdNotFoundError:
       print("User not found")
   except NetBirdAuthenticationError:
       print("Invalid API token")
   except NetBirdRateLimitError as e:
       print(f"Rate limited. Retry after {e.retry_after} seconds")
   except NetBirdAPIError as e:
       print(f"API error: {e.message}")

Next Steps
----------

- Check out the :doc:`api/index` for complete API documentation
- Explore :doc:`examples/index` for more detailed examples
- Learn about :doc:`user-guide/network-visualization` for advanced diagram features
- Read the :doc:`user-guide/authentication` guide for more auth options