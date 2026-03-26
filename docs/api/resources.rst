Resources
=========

Resource classes provide typed access to NetBird API endpoints. All resource classes
inherit from ``BaseResource`` and follow consistent patterns.

Common Patterns
---------------

Most resources follow the standard CRUD pattern:

.. code-block:: python

   # List all
   items = client.resource.list()

   # Get one
   item = client.resource.get("item-id")

   # Create
   from netbird.models import ResourceCreate
   data = ResourceCreate(name="New Item")
   item = client.resource.create(data)

   # Update
   from netbird.models import ResourceUpdate
   update = ResourceUpdate(name="Updated")
   item = client.resource.update("item-id", update)

   # Delete
   client.resource.delete("item-id")

All methods return **Python dictionaries** (not Pydantic models).

Core Resources
--------------

AccountsResource
~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.accounts.AccountsResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all accounts
- ``get(account_id)`` - Get account by ID
- ``update(account_id, data)`` - Update account settings
- ``delete(account_id)`` - Delete account

UsersResource
~~~~~~~~~~~~~

.. autoclass:: netbird.resources.users.UsersResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all users
- ``get(user_id)`` - Get user by ID
- ``get_current()`` - Get current authenticated user
- ``create(data)`` - Create a new user
- ``update(user_id, data)`` - Update user
- ``delete(user_id)`` - Delete user
- ``approve(user_id)`` - Approve a pending user
- ``reject(user_id)`` - Reject a pending user
- ``change_password(user_id, data)`` - Change user password
- ``list_invites()`` - List all pending invites
- ``create_invite(data)`` - Create a user invite
- ``delete_invite(invite_id)`` - Delete an invite
- ``regenerate_invite(invite_id)`` - Regenerate invite link
- ``get_invite_info(invite_id)`` - Get invite details
- ``accept_invite(invite_id, data)`` - Accept an invite

.. code-block:: python

   # Get current user
   me = client.users.get_current()
   print(f"Role: {me['role']}")

   # Create a service user
   from netbird.models import UserCreate
   user = client.users.create(UserCreate(
       email="bot@company.com",
       name="Bot",
       is_service_user=True
   ))

   # Approve a pending user
   client.users.approve("user-id")

TokensResource
~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.tokens.TokensResource
   :members:
   :undoc-members:

**Methods:**

- ``list(user_id)`` - List tokens for a user
- ``get(user_id, token_id)`` - Get a specific token
- ``create(user_id, data)`` - Create a new token
- ``delete(user_id, token_id)`` - Delete a token

PeersResource
~~~~~~~~~~~~~

.. autoclass:: netbird.resources.peers.PeersResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all peers
- ``get(peer_id)`` - Get peer by ID
- ``update(peer_id, data)`` - Update peer
- ``delete(peer_id)`` - Delete peer
- ``accessible_peers(peer_id)`` - List peers accessible to a given peer
- ``create_temporary_access(peer_id, data)`` - Grant temporary access
- ``list_jobs(peer_id)`` - List peer jobs
- ``create_job(peer_id, data)`` - Create a peer job
- ``get_job(peer_id, job_id)`` - Get a specific job

.. code-block:: python

   # List connected peers
   peers = client.peers.list()
   connected = [p for p in peers if p['connected']]
   print(f"{len(connected)}/{len(peers)} peers connected")

   # Get accessible peers
   accessible = client.peers.accessible_peers("peer-id")

SetupKeysResource
~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.setup_keys.SetupKeysResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all setup keys
- ``get(key_id)`` - Get setup key by ID
- ``create(data)`` - Create a new setup key
- ``update(key_id, data)`` - Update setup key
- ``delete(key_id)`` - Delete setup key

GroupsResource
~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.groups.GroupsResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all groups
- ``get(group_id)`` - Get group by ID
- ``create(data)`` - Create a new group
- ``update(group_id, data)`` - Update group
- ``delete(group_id)`` - Delete group

NetworksResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.networks.NetworksResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all networks
- ``get(network_id)`` - Get network by ID
- ``create(data)`` - Create a new network
- ``update(network_id, data)`` - Update network
- ``delete(network_id)`` - Delete network
- ``list_resources(network_id)`` - List resources in a network
- ``get_resource(network_id, resource_id)`` - Get a specific resource
- ``create_resource(network_id, data)`` - Create a resource
- ``update_resource(network_id, resource_id, data)`` - Update a resource
- ``delete_resource(network_id, resource_id)`` - Delete a resource
- ``list_routers(network_id)`` - List routers in a network
- ``get_router(network_id, router_id)`` - Get a specific router
- ``create_router(network_id, data)`` - Create a router
- ``update_router(network_id, router_id, data)`` - Update a router
- ``delete_router(network_id, router_id)`` - Delete a router
- ``list_all_routers()`` - List all routers across all networks

.. code-block:: python

   # Create network with resources
   from netbird.models import NetworkCreate
   network = client.networks.create(NetworkCreate(
       name="Production",
       description="Production network"
   ))

   # Add resources and routers
   resources = client.networks.list_resources(network['id'])
   routers = client.networks.list_routers(network['id'])

PoliciesResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.policies.PoliciesResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all policies
- ``get(policy_id)`` - Get policy by ID
- ``create(data)`` - Create a new policy
- ``update(policy_id, data)`` - Update policy
- ``delete(policy_id)`` - Delete policy

RoutesResource
~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.routes.RoutesResource
   :members:
   :undoc-members:

.. deprecated::
   Routes API is deprecated. Use the Networks API instead. All route methods
   emit ``DeprecationWarning``.

**Methods:**

- ``list()`` - List all routes
- ``get(route_id)`` - Get route by ID
- ``create(data)`` - Create a new route
- ``update(route_id, data)`` - Update route
- ``delete(route_id)`` - Delete route

DNSResource
~~~~~~~~~~~

.. autoclass:: netbird.resources.dns.DNSResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List nameserver groups
- ``get(ns_group_id)`` - Get nameserver group by ID
- ``create(data)`` - Create nameserver group
- ``update(ns_group_id, data)`` - Update nameserver group
- ``delete(ns_group_id)`` - Delete nameserver group
- ``get_settings()`` - Get DNS settings
- ``update_settings(data)`` - Update DNS settings

DNSZonesResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.dns_zones.DNSZonesResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all DNS zones
- ``get(zone_id)`` - Get zone by ID
- ``create(data)`` - Create a DNS zone
- ``update(zone_id, data)`` - Update zone
- ``delete(zone_id)`` - Delete zone
- ``list_records(zone_id)`` - List records in a zone
- ``get_record(zone_id, record_id)`` - Get a specific record
- ``create_record(zone_id, data)`` - Create a DNS record
- ``update_record(zone_id, record_id, data)`` - Update a record
- ``delete_record(zone_id, record_id)`` - Delete a record

EventsResource
~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.events.EventsResource
   :members:
   :undoc-members:

**Methods:**

- ``get_audit_events()`` - Get audit log events
- ``get_network_traffic_events(**filters)`` - Get network traffic events with filtering
- ``get_proxy_events(**filters)`` - Get reverse proxy events with filtering

.. code-block:: python

   # Audit events
   events = client.events.get_audit_events()

   # Network traffic with filters
   traffic = client.events.get_network_traffic_events(
       protocol="tcp",
       user_id="user-123",
       start_date="2024-01-01",
       end_date="2024-01-31",
       page_size=100,
   )

   # Proxy events with filters
   proxy = client.events.get_proxy_events(
       method="POST",
       host="api.example.com",
       status_code=200,
       sort_by="timestamp",
       sort_order="desc",
   )

PostureChecksResource
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.posture_checks.PostureChecksResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List all posture checks
- ``get(check_id)`` - Get posture check by ID
- ``create(data)`` - Create a posture check
- ``update(check_id, data)`` - Update posture check
- ``delete(check_id)`` - Delete posture check

GeoLocationsResource
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.geo_locations.GeoLocationsResource
   :members:
   :undoc-members:

**Methods:**

- ``get_countries()`` - List all countries
- ``get_cities(country_code)`` - List cities in a country

IdentityProvidersResource
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.identity_providers.IdentityProvidersResource
   :members:
   :undoc-members:

**Methods:**

- ``list()`` - List identity providers
- ``get(provider_id)`` - Get provider by ID
- ``create(data)`` - Create identity provider
- ``update(provider_id, data)`` - Update provider
- ``delete(provider_id)`` - Delete provider

InstanceResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.instance.InstanceResource
   :members:
   :undoc-members:

**Methods:**

- ``get_status()`` - Get instance status
- ``get_version()`` - Get instance version
- ``setup(data)`` - Initial instance setup

Cloud Resources
---------------

Cloud resources are only available on NetBird Cloud (``api.netbird.io``).
Access via ``client.cloud.<resource>``.

ServicesResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.services.ServicesResource
   :members:
   :undoc-members:

IngressResource
~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.ingress.IngressResource
   :members:
   :undoc-members:

EDR Resources
~~~~~~~~~~~~~

EDR integrations are accessed via ``client.cloud.edr``:

.. code-block:: python

   # CrowdStrike Falcon
   falcon = client.cloud.edr.falcon.get()

   # Huntress
   huntress = client.cloud.edr.huntress.get()

   # Microsoft Intune
   intune = client.cloud.edr.intune.get()

   # SentinelOne
   sentinelone = client.cloud.edr.sentinelone.get()

   # EDR Peers
   edr_peers = client.cloud.edr.peers.list()

MSPResource
~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.msp.MSPResource
   :members:
   :undoc-members:

InvoiceResource
~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.invoice.InvoiceResource
   :members:
   :undoc-members:

UsageResource
~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.usage.UsageResource
   :members:
   :undoc-members:

EventStreamingResource
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.event_streaming.EventStreamingResource
   :members:
   :undoc-members:

IDPScimResource
~~~~~~~~~~~~~~~

.. autoclass:: netbird.resources.cloud.idp_scim.IDPScimResource
   :members:
   :undoc-members:
