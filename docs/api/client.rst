Client
======

.. module:: netbird.client

The ``APIClient`` class is the main entry point for interacting with the NetBird API.

APIClient
---------

.. autoclass:: netbird.client.APIClient
   :members:
   :undoc-members:
   :show-inheritance:

Initialization
~~~~~~~~~~~~~~

.. code-block:: python

   from netbird import APIClient

   client = APIClient(
       host="api.netbird.io",       # Required: NetBird host
       api_token="your-token",      # Required: API token
       timeout=30.0,                # Optional: timeout in seconds
       base_path="/api",            # Optional: API base path
   )

Parameters
^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Default
     - Description
   * - ``host``
     - ``str``
     - (required)
     - NetBird API host (e.g., ``"api.netbird.io"`` or ``"netbird.company.com:33073"``)
   * - ``api_token``
     - ``str``
     - (required)
     - Personal Access Token for authentication
   * - ``timeout``
     - ``float``
     - ``30.0``
     - HTTP request timeout in seconds
   * - ``base_path``
     - ``str``
     - ``"/api"``
     - API base path prefix

HTTP Methods
~~~~~~~~~~~~

The client provides low-level HTTP methods used by resource classes:

- ``get(path, params=None)`` - HTTP GET request
- ``post(path, data=None)`` - HTTP POST request
- ``put(path, data=None)`` - HTTP PUT request
- ``delete(path)`` - HTTP DELETE request

All methods handle authentication headers, response parsing, and error translation automatically.

Resource Properties
~~~~~~~~~~~~~~~~~~~

Core Resources
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Property
     - Type
     - Description
   * - ``accounts``
     - ``AccountsResource``
     - Account management
   * - ``users``
     - ``UsersResource``
     - User lifecycle management
   * - ``tokens``
     - ``TokensResource``
     - API token management
   * - ``peers``
     - ``PeersResource``
     - Network peer management
   * - ``setup_keys``
     - ``SetupKeysResource``
     - Peer setup key management
   * - ``groups``
     - ``GroupsResource``
     - Peer group management
   * - ``networks``
     - ``NetworksResource``
     - Network and resource management
   * - ``policies``
     - ``PoliciesResource``
     - Access control policies
   * - ``routes``
     - ``RoutesResource``
     - Network routing (deprecated)
   * - ``dns``
     - ``DNSResource``
     - DNS nameserver groups
   * - ``dns_zones``
     - ``DNSZonesResource``
     - Custom DNS zones and records
   * - ``events``
     - ``EventsResource``
     - Audit and traffic events
   * - ``posture_checks``
     - ``PostureChecksResource``
     - Device compliance checks
   * - ``geo_locations``
     - ``GeoLocationsResource``
     - Geographic data
   * - ``identity_providers``
     - ``IdentityProvidersResource``
     - OAuth2/OIDC providers
   * - ``instance``
     - ``InstanceResource``
     - Instance management

Cloud Namespace
^^^^^^^^^^^^^^^

Access cloud-only resources via ``client.cloud``:

.. code-block:: python

   # Cloud resources
   client.cloud.services
   client.cloud.ingress
   client.cloud.msp
   client.cloud.invoices
   client.cloud.usage
   client.cloud.event_streaming
   client.cloud.idp_scim

   # EDR resources
   client.cloud.edr.peers
   client.cloud.edr.falcon
   client.cloud.edr.huntress
   client.cloud.edr.intune
   client.cloud.edr.sentinelone

Diagram Generation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Generate network topology diagram
   client.generate_diagram(
       format="mermaid",         # "mermaid", "graphviz", or "diagrams"
       output_file="network",   # Output filename
       include_routers=True,    # Include routers
       include_policies=True,   # Include policy connections
       include_resources=True,  # Include resources
   )

CloudResources
--------------

.. module:: netbird.cloud

.. autoclass:: netbird.cloud.CloudResources
   :members:
   :undoc-members:

EDRResources
~~~~~~~~~~~~

.. autoclass:: netbird.cloud.EDRResources
   :members:
   :undoc-members:

Network Map
-----------

.. module:: netbird.network_map

.. autofunction:: netbird.network_map.generate_full_network_map

.. autofunction:: netbird.network_map.get_network_topology_data
