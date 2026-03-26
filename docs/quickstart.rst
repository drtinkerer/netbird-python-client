Quick Start
===========

This guide gets you started with the NetBird Python client in minutes.

Installation
------------

.. code-block:: bash

   pip install netbird

Initialize the Client
---------------------

.. tabs::

   .. tab:: NetBird Cloud

      .. code-block:: python

         from netbird import APIClient

         client = APIClient(
             host="api.netbird.io",
             api_token="your-api-token"
         )

   .. tab:: Self-hosted

      .. code-block:: python

         from netbird import APIClient

         client = APIClient(
             host="netbird.yourcompany.com:33073",
             api_token="your-api-token"
         )

Authentication
--------------

You need a **Personal Access Token (PAT)** to authenticate. Generate one from:

- **NetBird Cloud**: Dashboard > Settings > API Tokens
- **Self-hosted**: Your NetBird management interface

.. code-block:: python

   import os

   client = APIClient(
       host=os.environ["NETBIRD_HOST"],
       api_token=os.environ["NETBIRD_API_TOKEN"]
   )

Basic Operations
----------------

List Peers
~~~~~~~~~~

.. code-block:: python

   peers = client.peers.list()
   for peer in peers:
       status = "connected" if peer["connected"] else "offline"
       print(f"{peer['name']} ({peer['ip']}) - {status}")

Get Current User
~~~~~~~~~~~~~~~~

.. code-block:: python

   user = client.users.get_current()
   print(f"Logged in as: {user['name']} ({user['email']})")
   print(f"Role: {user['role']}")

List Groups
~~~~~~~~~~~

.. code-block:: python

   groups = client.groups.list()
   for group in groups:
       peer_count = len(group.get('peers', []))
       print(f"{group['name']}: {peer_count} peers")

Create Resources
~~~~~~~~~~~~~~~~

.. code-block:: python

   from netbird.models import GroupCreate, UserCreate

   # Create a group
   group_data = GroupCreate(
       name="Engineering",
       peers=["peer-id-1", "peer-id-2"]
   )
   group = client.groups.create(group_data)
   print(f"Created group: {group['name']}")

   # Create a user
   user_data = UserCreate(
       email="alice@company.com",
       name="Alice",
       role="admin",
       is_service_user=False
   )
   user = client.users.create(user_data)
   print(f"Created user: {user['email']}")

Cloud Resources
~~~~~~~~~~~~~~~

Cloud-only resources are available via the ``client.cloud`` namespace.
These only work with NetBird Cloud (``api.netbird.io``).

.. code-block:: python

   # Get billing usage
   usage = client.cloud.usage.get()

   # EDR integrations
   falcon_config = client.cloud.edr.falcon.get()

   # Reverse proxy services
   services = client.cloud.services.list()

.. note::

   When using ``client.cloud`` with a self-hosted instance, a warning is emitted
   and API calls may return 404 errors.

Events and Monitoring
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Audit events
   events = client.events.get_audit_events()
   for event in events[-5:]:
       print(f"{event['timestamp']}: {event['activity']}")

   # Network traffic events
   traffic = client.events.get_network_traffic_events(
       protocol="tcp",
       page_size=50
   )

   # Proxy events
   proxy_events = client.events.get_proxy_events(
       method="POST",
       status_code=200,
       page_size=25
   )

Network Visualization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Generate a Mermaid diagram
   mermaid = client.generate_diagram(format="mermaid")
   print(mermaid)

   # Generate a PNG with Graphviz
   client.generate_diagram(format="graphviz", output_file="network")

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from netbird.exceptions import (
       NetBirdAPIError,
       NetBirdAuthenticationError,
       NetBirdNotFoundError,
       NetBirdRateLimitError,
   )

   try:
       peer = client.peers.get("nonexistent-id")
   except NetBirdNotFoundError:
       print("Peer not found")
   except NetBirdAuthenticationError:
       print("Invalid API token")
   except NetBirdRateLimitError as e:
       print(f"Rate limited. Retry after {e.retry_after}s")
   except NetBirdAPIError as e:
       print(f"API error ({e.status_code}): {e.message}")

Configuration Options
---------------------

.. code-block:: python

   client = APIClient(
       host="your-netbird-host.com",    # Required: NetBird API host
       api_token="your-token",          # Required: API access token
       timeout=30.0,                    # Optional: Request timeout (default: 30s)
       base_path="/api",                # Optional: API base path (default: "/api")
   )

Next Steps
----------

- :doc:`user-guide/authentication` - Authentication details and best practices
- :doc:`user-guide/network-visualization` - Advanced diagram generation
- :doc:`user-guide/error-handling` - Comprehensive error handling
- :doc:`api/index` - Full API reference
- :doc:`examples/index` - More code examples
