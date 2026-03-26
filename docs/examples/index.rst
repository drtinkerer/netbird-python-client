Examples
========

Practical examples showing common use cases with the NetBird Python client.

.. toctree::
   :maxdepth: 2

   user-management
   network-management
   diagrams

Getting Started
---------------

All examples assume you have initialized the client:

.. code-block:: python

   from netbird import APIClient

   client = APIClient(
       host="api.netbird.io",
       api_token="your-api-token"
   )

Quick Examples
--------------

List All Peers
~~~~~~~~~~~~~~

.. code-block:: python

   peers = client.peers.list()
   for peer in peers:
       status = "online" if peer["connected"] else "offline"
       print(f"{peer['name']:20s} {peer['ip']:15s} {status}")

Get Account Info
~~~~~~~~~~~~~~~~

.. code-block:: python

   accounts = client.accounts.list()
   for account in accounts:
       print(f"Account: {account['id']}")
       print(f"Domain: {account.get('domain', 'N/A')}")

List Groups with Peer Counts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   groups = client.groups.list()
   for group in sorted(groups, key=lambda g: g['name']):
       peers = group.get('peers', [])
       print(f"{group['name']}: {len(peers)} peers")

Monitor Audit Events
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   events = client.events.get_audit_events()
   for event in events[-10:]:
       print(f"[{event['timestamp']}] {event['activity']}")

Export Network Data
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json

   # Export peers
   peers = client.peers.list()
   with open("peers.json", "w") as f:
       json.dump(peers, f, indent=2)

   # Export groups
   groups = client.groups.list()
   with open("groups.json", "w") as f:
       json.dump(groups, f, indent=2)

Cloud Resources
~~~~~~~~~~~~~~~

.. code-block:: python

   # These only work with NetBird Cloud (api.netbird.io)

   # Get usage statistics
   usage = client.cloud.usage.get()
   print(f"Active peers: {usage.get('active_peers', 'N/A')}")

   # List reverse proxy services
   services = client.cloud.services.list()
   for svc in services:
       print(f"Service: {svc['name']}")

   # Check EDR integrations
   try:
       falcon = client.cloud.edr.falcon.get()
       print(f"Falcon: {falcon}")
   except Exception:
       print("Falcon not configured")
