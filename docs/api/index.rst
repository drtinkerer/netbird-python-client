API Reference
=============

Complete API reference for the NetBird Python client. The library provides typed
Python access to all NetBird REST API endpoints.

.. toctree::
   :maxdepth: 2

   client
   resources
   models
   exceptions

Overview
--------

The API follows a consistent pattern:

- **Client**: ``APIClient`` manages authentication and HTTP requests
- **Resources**: Each API endpoint has a dedicated resource class (e.g., ``PeersResource``)
- **Models**: Pydantic models provide type-safe input validation (e.g., ``UserCreate``)
- **Exceptions**: Specific exception types for different error conditions

Usage Pattern
~~~~~~~~~~~~~

.. code-block:: python

   from netbird import APIClient
   from netbird.models import GroupCreate

   # 1. Initialize client
   client = APIClient(host="api.netbird.io", api_token="token")

   # 2. Use resource methods (returns dictionaries)
   peers = client.peers.list()

   # 3. Use models for input validation
   group_data = GroupCreate(name="Team", peers=["peer-1"])
   group = client.groups.create(group_data)

   # 4. Handle errors
   from netbird.exceptions import NetBirdNotFoundError
   try:
       client.peers.get("bad-id")
   except NetBirdNotFoundError:
       pass

Resource Access
~~~~~~~~~~~~~~~

Core resources are accessed as properties on the client:

.. code-block:: python

   client.accounts       # AccountsResource
   client.users          # UsersResource
   client.tokens         # TokensResource
   client.peers          # PeersResource
   client.setup_keys     # SetupKeysResource
   client.groups         # GroupsResource
   client.networks       # NetworksResource
   client.policies       # PoliciesResource
   client.routes         # RoutesResource
   client.dns            # DNSResource
   client.dns_zones      # DNSZonesResource
   client.events         # EventsResource
   client.posture_checks # PostureChecksResource
   client.geo_locations  # GeoLocationsResource
   client.identity_providers  # IdentityProvidersResource
   client.instance       # InstanceResource

Cloud resources are accessed via the ``cloud`` namespace:

.. code-block:: python

   client.cloud.services         # ServicesResource
   client.cloud.ingress          # IngressResource
   client.cloud.msp              # MSPResource
   client.cloud.invoices         # InvoicesResource
   client.cloud.usage            # UsageResource
   client.cloud.event_streaming  # EventStreamingResource
   client.cloud.idp_scim         # IDPSCIMResource

   # EDR integrations
   client.cloud.edr.peers        # EDRPeersResource
   client.cloud.edr.falcon       # EDRFalconResource
   client.cloud.edr.huntress     # EDRHuntressResource
   client.cloud.edr.intune       # EDRIntuneResource
   client.cloud.edr.sentinelone  # EDRSentinelOneResource
