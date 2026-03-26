NetBird Python Client
=====================

.. warning::
   This is an **unofficial**, community-maintained client library. It is **not affiliated with, endorsed by, or officially supported** by NetBird or the NetBird team. For official NetBird tools and support, please visit `netbird.io <https://netbird.io>`_.

**Unofficial** Python client library for the `NetBird <https://netbird.io>`_ API. Provides complete access to **30+ API resources** across core, cloud, and EDR endpoints with type-safe input validation and clean dictionary responses.

.. grid:: 2

    .. grid-item-card:: Quick Start
        :link: quickstart
        :link-type: doc

        Get up and running with the NetBird Python client in minutes

    .. grid-item-card:: API Reference
        :link: api/index
        :link-type: doc

        Complete API documentation for all 30+ resources

    .. grid-item-card:: Examples
        :link: examples/index
        :link-type: doc

        Practical examples for common use cases

    .. grid-item-card:: Installation
        :link: installation
        :link-type: doc

        Installation guide and requirements

Features
--------

.. grid:: 3

    .. grid-item-card:: Full API Parity

        30+ resources covering core, cloud, and EDR endpoints

    .. grid-item-card:: Cloud & Self-Hosted

        Works with both NetBird Cloud and self-hosted instances

    .. grid-item-card:: Forward-Compatible

        ``extra="allow"`` on all models accepts future API fields

    .. grid-item-card:: Type Safety

        Pydantic models for input validation

    .. grid-item-card:: Network Visualization

        Built-in diagram generation (Mermaid, Graphviz, Diagrams)

    .. grid-item-card:: Modern Python

        Python 3.9+ (supports 3.9-3.14)

Architecture
------------

The client uses a **dual-pattern design**:

- **Input validation**: Pydantic models (``UserCreate``, ``GroupCreate``, etc.) provide type-safe request validation
- **API responses**: Standard Python dictionaries for easy data access

.. code-block:: python

   from netbird import APIClient
   from netbird.models import UserCreate

   client = APIClient(host="api.netbird.io", api_token="your-token")

   # Input: Type-safe Pydantic models
   user_data = UserCreate(email="john@example.com", name="John Doe")

   # Output: Standard Python dictionaries
   user = client.users.create(user_data)
   print(user['name'])          # "John Doe"
   print(user.get('role'))      # Safe access with .get()

Resource Namespaces
-------------------

Resources are organized into two namespaces:

**Core Resources** (``client.<resource>``)
   Available on both self-hosted and cloud NetBird instances. Includes accounts, users,
   peers, groups, networks, policies, DNS, events, and more.

**Cloud Resources** (``client.cloud.<resource>``)
   Available only on NetBird Cloud (``api.netbird.io``). Includes services, ingress,
   EDR integrations, MSP management, billing, and event streaming.

.. code-block:: python

   # Core resources (all instances)
   peers = client.peers.list()
   groups = client.groups.list()

   # Cloud resources (NetBird Cloud only)
   usage = client.cloud.usage.get()
   falcon = client.cloud.edr.falcon.get()

Core Resources
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Resource
     - Description
     - Key Methods
   * - **Accounts**
     - Account management and settings
     - ``list``, ``update``, ``delete``
   * - **Users**
     - User lifecycle management
     - ``list``, ``get``, ``create``, ``update``, ``delete``, ``approve``, ``reject``, ``change_password``
   * - **Tokens**
     - API token management
     - ``list``, ``get``, ``create``, ``delete``
   * - **Peers**
     - Network peer management
     - ``list``, ``get``, ``update``, ``delete``, ``accessible_peers``, ``create_temporary_access``
   * - **Setup Keys**
     - Peer setup key management
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **Groups**
     - Peer group management
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **Networks**
     - Network and resource management
     - ``list``, ``get``, ``create``, ``update``, ``delete``, ``list_resources``, ``list_routers``
   * - **Policies**
     - Access control policies
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **Routes**
     - Network routing (deprecated)
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **DNS**
     - DNS nameserver groups
     - ``list``, ``get``, ``create``, ``update``, ``delete``, ``get_settings``, ``update_settings``
   * - **DNS Zones**
     - Custom DNS zones and records
     - Zone CRUD + Record CRUD
   * - **Events**
     - Audit and traffic events
     - ``get_audit_events``, ``get_network_traffic_events``, ``get_proxy_events``
   * - **Posture Checks**
     - Device compliance verification
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **Geo Locations**
     - Geographic data queries
     - ``get_countries``, ``get_cities``
   * - **Identity Providers**
     - OAuth2/OIDC providers
     - ``list``, ``get``, ``create``, ``update``, ``delete``
   * - **Instance**
     - Instance management
     - ``get_status``, ``get_version``, ``setup``

Cloud Resources
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Resource
     - Description
     - Key Methods
   * - **Services**
     - Reverse proxy services
     - CRUD + Domain management
   * - **Ingress**
     - Ingress port allocation
     - Port + Peer management
   * - **EDR Peers**
     - EDR peer bypass
     - ``list``, ``bypass``, ``revoke``
   * - **EDR Falcon**
     - CrowdStrike Falcon
     - ``get``, ``create``, ``update``, ``delete``
   * - **EDR Huntress**
     - Huntress integration
     - ``get``, ``create``, ``update``, ``delete``
   * - **EDR Intune**
     - Microsoft Intune
     - ``get``, ``create``, ``update``, ``delete``
   * - **EDR SentinelOne**
     - SentinelOne integration
     - ``get``, ``create``, ``update``, ``delete``
   * - **MSP**
     - Multi-tenant management
     - Tenants CRUD + Users/Peers
   * - **Invoices**
     - Billing invoices
     - ``list``, ``get_pdf``, ``get_csv``
   * - **Usage**
     - Billing usage stats
     - ``get``
   * - **Event Streaming**
     - Event streaming integrations
     - CRUD operations
   * - **IDP/SCIM**
     - SCIM identity providers
     - CRUD + Token + Logs

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
