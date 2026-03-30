MCP Server
==========

The NetBird Python Client includes a built-in `Model Context Protocol <https://modelcontextprotocol.io>`_ (MCP) server that exposes 25 NetBird management tools to AI assistants like `Claude Desktop <https://claude.ai>`_.

This lets you manage your NetBird network through natural language — no scripting required.

Installation
------------

The MCP server requires the optional ``mcp`` dependency:

.. code-block:: bash

   pip install "netbird[mcp]"

Configuration
-------------

The server reads credentials from environment variables:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``NETBIRD_HOST``
     - NetBird API host (e.g. ``api.netbird.io`` or ``netbird.yourcompany.com``)
   * - ``NETBIRD_API_TOKEN``
     - Personal Access Token from the NetBird dashboard

Claude Desktop Setup
--------------------

Add the following to your Claude Desktop configuration file:

- **macOS**: ``~/Library/Application Support/Claude/claude_desktop_config.json``
- **Windows**: ``%APPDATA%\Claude\claude_desktop_config.json``

.. code-block:: json

   {
     "mcpServers": {
       "netbird": {
         "command": "netbird-mcp",
         "env": {
           "NETBIRD_HOST": "api.netbird.io",
           "NETBIRD_API_TOKEN": "your-api-token"
         }
       }
     }
   }

Restart Claude Desktop after saving. You should see NetBird tools available in the conversation.

Self-Hosted NetBird
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "mcpServers": {
       "netbird": {
         "command": "netbird-mcp",
         "env": {
           "NETBIRD_HOST": "netbird.yourcompany.com",
           "NETBIRD_API_TOKEN": "your-api-token"
         }
       }
     }
   }

Running the Server Manually
---------------------------

.. code-block:: bash

   NETBIRD_HOST=api.netbird.io NETBIRD_API_TOKEN=your-token netbird-mcp

Or using ``python -m``:

.. code-block:: bash

   python -m netbird.mcp.server

Available Tools
---------------

The server exposes 25 tools organized by resource:

Account
~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``get_account``
     - Get the current NetBird account settings and configuration

Users
~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``get_current_user``
     - Get the currently authenticated user's profile and permissions
   * - ``list_users``
     - List all users in the NetBird account

Peers
~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_peers``
     - List all peers with connection status and IP addresses
   * - ``get_peer``
     - Get details of a specific peer by ID
   * - ``update_peer``
     - Update a peer's name, SSH access, or login expiration
   * - ``delete_peer``
     - Remove a peer from the network
   * - ``get_peer_accessible_peers``
     - List all peers a given peer can access based on current policies

Groups
~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_groups``
     - List all peer groups with member counts
   * - ``get_group``
     - Get details of a specific group including its members
   * - ``create_group``
     - Create a new peer group with optional initial members
   * - ``update_group``
     - Update a group's name or member list
   * - ``delete_group``
     - Delete a peer group

Policies
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_policies``
     - List all access control policies with their rules
   * - ``create_policy``
     - Create a new policy with protocol, port, and direction control
   * - ``delete_policy``
     - Delete an access control policy

Networks
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_networks``
     - List all networks with their resources and routers
   * - ``get_network``
     - Get a network with its resources and routers included

Setup Keys
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_setup_keys``
     - List all setup keys with validity and usage stats
   * - ``create_setup_key``
     - Create a setup key for enrolling new peers

DNS
~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_nameservers``
     - List all DNS nameserver groups
   * - ``get_dns_settings``
     - Get the global DNS settings for the account

Posture Checks & Audit
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``list_posture_checks``
     - List all device posture checks (compliance policies)
   * - ``get_audit_events``
     - Get recent audit log events showing account activity

Diagrams
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tool
     - Description
   * - ``generate_network_diagram``
     - Generate a network topology diagram (Mermaid, Graphviz, or Diagrams)

Example Conversations
---------------------

Once connected to Claude Desktop, you can ask questions like:

.. code-block:: text

   "List all peers and show which ones are currently connected"

   "Create a policy called 'SSH Access' allowing the DevOps group
    to reach port 22 on the Servers group"

   "Generate a Mermaid diagram of the current network topology"

   "Create a reusable setup key called 'Office-Onboarding' that expires
    in 7 days and auto-assigns peers to the Office group"

   "Show me all audit events from the last 24 hours"

   "Which peers can the peer named 'laptop-01' access?"

API Reference
-------------

.. automodule:: netbird.mcp.server
   :members:
   :undoc-members:
   :show-inheritance:
