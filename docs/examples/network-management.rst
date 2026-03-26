Network Management
==================

Examples for managing networks, peers, groups, policies, and DNS.

Peer Management
---------------

List and Filter Peers
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   peers = client.peers.list()

   # Connected peers
   connected = [p for p in peers if p['connected']]
   print(f"Connected: {len(connected)}/{len(peers)}")

   # Peers by IP range
   internal = [p for p in peers if p['ip'].startswith('100.')]
   print(f"Internal peers: {len(internal)}")

   # Detailed peer info
   for peer in connected:
       print(f"  {peer['name']:20s} {peer['ip']:15s} OS: {peer.get('os', 'N/A')}")

Update Peer Settings
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from netbird.models import PeerUpdate

   # Enable SSH on a peer
   client.peers.update("peer-id", PeerUpdate(
       ssh_enabled=True,
       name="renamed-peer"
   ))

   # Disable login expiration
   client.peers.update("peer-id", PeerUpdate(
       login_expiration_enabled=False
   ))

Accessible Peers
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find which peers can access a specific peer
   accessible = client.peers.accessible_peers("peer-id")
   for peer in accessible:
       print(f"Can access: {peer['name']} ({peer['ip']})")

Temporary Access
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Grant temporary access to a peer
   access = client.peers.create_temporary_access("peer-id", {
       "expires_at": "2024-12-31T23:59:59Z"
   })

Group Management
----------------

.. code-block:: python

   from netbird.models import GroupCreate, GroupUpdate

   # List all groups
   groups = client.groups.list()
   for group in groups:
       peers = group.get('peers', [])
       print(f"{group['name']}: {len(peers)} peers")

   # Create a group
   group = client.groups.create(GroupCreate(
       name="Backend Team",
       peers=["peer-id-1", "peer-id-2"]
   ))

   # Update a group
   client.groups.update(group['id'], GroupUpdate(
       name="Backend Engineers",
       peers=["peer-id-1", "peer-id-2", "peer-id-3"]
   ))

   # Delete a group
   client.groups.delete(group['id'])

Network Management
------------------

.. code-block:: python

   from netbird.models import NetworkCreate, NetworkUpdate

   # List networks
   networks = client.networks.list()
   for net in networks:
       print(f"{net['name']}: {net.get('description', '')}")

   # Create a network
   network = client.networks.create(NetworkCreate(
       name="Production",
       description="Production environment network"
   ))

   # List resources in a network
   resources = client.networks.list_resources(network['id'])
   for resource in resources:
       print(f"  Resource: {resource['name']} - {resource.get('address', 'N/A')}")

   # List routers in a network
   routers = client.networks.list_routers(network['id'])
   for router in routers:
       print(f"  Router: {router.get('peer', 'N/A')}")

   # List all routers across all networks
   all_routers = client.networks.list_all_routers()

Policy Management
-----------------

.. code-block:: python

   from netbird.models import PolicyCreate, PolicyRule, PolicyUpdate

   # List policies
   policies = client.policies.list()
   for policy in policies:
       enabled = "enabled" if policy.get('enabled') else "disabled"
       print(f"{policy['name']} ({enabled})")

   # Create a policy
   rule = PolicyRule(
       name="Allow SSH",
       action="accept",
       protocol="tcp",
       ports=["22"],
       sources=["source-group-id"],
       destinations=["dest-group-id"],
       bidirectional=False,
   )

   policy = client.policies.create(PolicyCreate(
       name="SSH Access Policy",
       description="Allow SSH access from dev to prod",
       rules=[rule],
       enabled=True,
   ))

   # Disable a policy
   client.policies.update(policy['id'], PolicyUpdate(enabled=False))

Setup Keys
----------

.. code-block:: python

   from netbird.models import SetupKeyCreate

   # List setup keys
   keys = client.setup_keys.list()
   for key in keys:
       status = "valid" if key.get('valid') else "invalid"
       print(f"{key['name']}: {status}, used {key.get('used_times', 0)} times")

   # Create a reusable key
   key = client.setup_keys.create(SetupKeyCreate(
       name="Auto-enrollment",
       type="reusable",
       expires_in=86400,     # 24 hours
       usage_limit=100,
       auto_groups=["default-group"],
   ))
   print(f"Key: {key['key']}")

   # Create a one-off key
   one_off = client.setup_keys.create(SetupKeyCreate(
       name="Single Use",
       type="one-off",
       expires_in=3600,      # 1 hour
   ))

DNS Management
--------------

.. code-block:: python

   # Get DNS settings
   settings = client.dns.get_settings()
   print(f"Disabled groups: {settings.get('disabled_management_groups', [])}")

   # List nameserver groups
   ns_groups = client.dns.list()
   for ns in ns_groups:
       print(f"{ns['name']}: {ns.get('nameservers', [])}")

DNS Zones
~~~~~~~~~

.. code-block:: python

   from netbird.models import DNSZoneCreate, DNSRecordCreate

   # List DNS zones
   zones = client.dns_zones.list()
   for zone in zones:
       print(f"Zone: {zone['name']}")

   # Create a DNS zone
   zone = client.dns_zones.create(DNSZoneCreate(
       name="internal.company.com",
   ))

   # Add a record to the zone
   record = client.dns_zones.create_record(zone['id'], DNSRecordCreate(
       name="app",
       type="A",
       value="10.0.0.1",
   ))

Posture Checks
--------------

.. code-block:: python

   from netbird.models import PostureCheckCreate

   # List posture checks
   checks = client.posture_checks.list()
   for check in checks:
       print(f"{check['name']}: {check.get('description', '')}")

   # Create a posture check
   check = client.posture_checks.create(PostureCheckCreate(
       name="Minimum OS Version",
       description="Require minimum OS version",
       checks={
           "os_version_check": {
               "min_version": "10.0"
           }
       }
   ))

Events and Monitoring
---------------------

.. code-block:: python

   # Audit events
   events = client.events.get_audit_events()
   for event in events[-10:]:
       initiator = event.get('initiator_name', 'system')
       print(f"[{event['timestamp']}] {event['activity']} by {initiator}")

   # Network traffic events with filters
   traffic = client.events.get_network_traffic_events(
       protocol="tcp",
       connection_type="p2p",
       start_date="2024-01-01",
       end_date="2024-01-31",
       page_size=100,
   )

   for t in traffic[:5]:
       print(f"{t['source_ip']} -> {t['destination_ip']} ({t['protocol']})")

   # Proxy events
   proxy = client.events.get_proxy_events(
       method="POST",
       status="success",
       host="api.example.com",
       page_size=50,
       sort_by="timestamp",
       sort_order="desc",
   )

Geographic Data
---------------

.. code-block:: python

   # List countries
   countries = client.geo_locations.get_countries()
   for country in countries[:10]:
       print(f"{country['code']}: {country['name']}")

   # List cities in a country
   cities = client.geo_locations.get_cities("US")
   for city in cities[:10]:
       print(f"  {city['name']}")
