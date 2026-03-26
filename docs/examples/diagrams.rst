Network Diagrams
================

Examples for generating network topology diagrams.

Mermaid Diagrams
----------------

Mermaid diagrams require no extra dependencies and render natively in GitHub and GitLab.

.. code-block:: python

   from netbird import APIClient

   client = APIClient(host="api.netbird.io", api_token="your-token")

   # Generate and print Mermaid diagram
   mermaid = client.generate_diagram(format="mermaid")
   print(mermaid)

   # Save to file
   client.generate_diagram(
       format="mermaid",
       output_file="network_topology"
   )
   # Creates network_topology.mmd

Embed in Markdown
~~~~~~~~~~~~~~~~~

.. code-block:: python

   mermaid = client.generate_diagram(format="mermaid")

   # Write as GitHub-compatible Markdown
   with open("NETWORK.md", "w") as f:
       f.write("# Network Topology\n\n")
       f.write("```mermaid\n")
       f.write(mermaid)
       f.write("\n```\n")

Graphviz Diagrams
-----------------

Graphviz produces high-quality PNG, SVG, and PDF output.

.. code-block:: bash

   # Install dependencies
   pip install graphviz
   brew install graphviz  # macOS

.. code-block:: python

   # Generate PNG
   client.generate_diagram(
       format="graphviz",
       output_file="network"
   )
   # Creates network.png

Python Diagrams
---------------

Python Diagrams creates architecture-style diagrams.

.. code-block:: bash

   pip install diagrams

.. code-block:: python

   client.generate_diagram(
       format="diagrams",
       output_file="architecture"
   )
   # Creates architecture.png

Customizing Diagrams
--------------------

.. code-block:: python

   # Full network view with all details
   client.generate_diagram(
       format="mermaid",
       include_routers=True,
       include_policies=True,
       include_resources=True,
       output_file="complete_network"
   )

   # Simplified view (resources only)
   client.generate_diagram(
       format="mermaid",
       include_routers=False,
       include_policies=False,
       include_resources=True,
       output_file="resources_only"
   )

Working with Network Map Data
-----------------------------

For custom visualizations, use the lower-level functions:

.. code-block:: python

   from netbird.network_map import (
       generate_full_network_map,
       get_network_topology_data,
   )

   # Get raw network data
   networks = generate_full_network_map(client)
   for network in networks:
       print(f"\nNetwork: {network['name']}")
       print(f"  Resources: {len(network.get('resources', []))}")
       print(f"  Routers: {len(network.get('routers', []))}")
       print(f"  Policies: {len(network.get('policies', []))}")

       for resource in network.get('resources', []):
           addr = resource.get('address', 'N/A')
           rtype = resource.get('type', 'N/A')
           print(f"    {resource['name']}: {addr} ({rtype})")

   # Get topology data for custom rendering
   topology = get_network_topology_data(client, optimize_connections=True)

   print(f"\nTopology Summary:")
   print(f"  Source groups: {len(topology['all_source_groups'])}")
   print(f"  Group connections: {len(topology['group_connections'])}")
   print(f"  Direct connections: {len(topology['direct_connections'])}")

   # Build custom visualization from topology data
   for conn in topology.get('group_connections', []):
       print(f"  {conn['source']} -> {conn['destination']}: {conn['policies']}")

Export to JSON
--------------

.. code-block:: python

   import json
   from netbird.network_map import generate_full_network_map

   networks = generate_full_network_map(client)

   with open("network_map.json", "w") as f:
       json.dump(networks, f, indent=2, default=str)

   print(f"Exported {len(networks)} networks to network_map.json")
