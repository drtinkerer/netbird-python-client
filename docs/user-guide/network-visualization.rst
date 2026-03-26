Network Visualization
=====================

The NetBird Python client includes built-in network visualization that generates topology diagrams in multiple formats.

Overview
--------

Network visualization works in two steps:

1. **Data collection**: Fetches networks, resources, routers, and policies from the API
2. **Diagram generation**: Renders the topology in the chosen format

Supported Formats
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Format
     - Output
     - Best For
   * - **Mermaid**
     - ``.mmd``, ``.md``
     - GitHub/GitLab docs, web viewing, no dependencies needed
   * - **Graphviz**
     - ``.png``, ``.svg``, ``.pdf``, ``.dot``
     - High-quality publications, presentations
   * - **Diagrams**
     - ``.png``
     - Code documentation, architecture diagrams

Quick Start
-----------

.. code-block:: python

   from netbird import APIClient

   client = APIClient(host="api.netbird.io", api_token="your-token")

   # Generate Mermaid diagram (no extra dependencies)
   mermaid = client.generate_diagram(format="mermaid")
   print(mermaid)

   # Save as Graphviz PNG
   client.generate_diagram(format="graphviz", output_file="my_network")

   # Save as Python Diagrams PNG
   client.generate_diagram(format="diagrams", output_file="network_topology")

Diagram Options
---------------

The ``generate_diagram`` method accepts these parameters:

.. code-block:: python

   client.generate_diagram(
       format="mermaid",             # "mermaid", "graphviz", or "diagrams"
       output_file="network",        # Output filename (without extension)
       include_routers=True,         # Show network routers
       include_policies=True,        # Show policy connections
       include_resources=True,       # Show network resources
   )

Diagram Features
----------------

Source Groups
~~~~~~~~~~~~~

User groups are shown with distinct colors for easy identification. Each source group
gets a unique color automatically.

Networks and Resources
~~~~~~~~~~~~~~~~~~~~~~

Networks are rendered as hierarchical containers with their resources nested inside,
showing resource names, addresses, and types.

Policy Connections
~~~~~~~~~~~~~~~~~~

Policies are visualized as connections between groups:

- **Group-based access**: Dashed lines showing group-to-group policies
- **Direct resource access**: Solid lines showing group-to-resource policies

Connection Optimization
~~~~~~~~~~~~~~~~~~~~~~~

When multiple policies share the same source and destination, connections are merged
to reduce visual complexity. A label shows the number of policies.

Network Map Functions
---------------------

For programmatic access to network data, use the lower-level functions:

.. code-block:: python

   from netbird.network_map import (
       generate_full_network_map,
       get_network_topology_data,
   )

   # Get enriched network data
   networks = generate_full_network_map(client)
   for network in networks:
       print(f"Network: {network['name']}")
       for resource in network.get('resources', []):
           print(f"  Resource: {resource['name']} - {resource['address']}")
       for policy in network.get('policies', []):
           print(f"  Policy: {policy['name']}")

   # Get topology data for custom visualization
   topology = get_network_topology_data(client, optimize_connections=True)
   print(f"Source groups: {len(topology['all_source_groups'])}")
   print(f"Group connections: {len(topology['group_connections'])}")
   print(f"Direct connections: {len(topology['direct_connections'])}")

Error Handling
--------------

.. code-block:: python

   from netbird.exceptions import (
       NetBirdAPIError,
       NetBirdAuthenticationError,
   )

   try:
       networks = generate_full_network_map(client)
   except NetBirdAuthenticationError:
       print("Authentication failed - check your API token")
   except NetBirdAPIError as e:
       print(f"API error: {e.message}")

The network map functions handle individual resource/router/policy fetch failures
gracefully - if one resource fails to load, others still appear in the output.

Installation for Diagrams
-------------------------

.. code-block:: bash

   # Mermaid - no extra Python dependencies
   # Render with any Mermaid-compatible tool (GitHub, GitLab, mermaid.live)

   # Graphviz
   pip install graphviz
   brew install graphviz   # macOS system package also required

   # Python Diagrams
   pip install diagrams
