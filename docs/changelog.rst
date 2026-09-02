Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.4.0] - 2026-09-02
---------------------

Added
~~~~~

- **Bearer-token authentication** — ``APIClient(host=..., api_token=..., auth_scheme="Bearer")``
  (and ``TokenAuth(token, scheme="Bearer")``) sends ``Authorization: Bearer <token>``
  instead of the default ``Authorization: Token <token>``, for OAuth2 / OIDC access
  tokens. ``auth_scheme`` accepts ``"Token"`` (default) or ``"Bearer"``; any other
  value raises ``ValueError``. New ``netbird.auth.AuthScheme`` type alias.
- **``viz`` optional dependency group** — ``pip install "netbird[viz]"`` installs
  ``graphviz>=0.20.0`` and ``diagrams>=0.23.0`` for Graphviz / Python-Diagrams
  diagram output. The Graphviz system binary is still required separately.
- **New model fields tracking recent NetBird API revisions:**

  - ``AccountSettings`` — ``network_range_v6``, ``dns_domain``,
    ``regular_users_view_blocked``, ``groups_propagation_enabled``,
    ``jwt_allow_groups``, ``auto_update_always``, ``metrics_push_enabled``,
    ``agent_network_only``, ``dashboard_features``, ``local_mfa_enabled``,
    ``ipv6_enabled_groups``
  - ``RouteCreate`` / ``RouteUpdate`` — ``skip_auto_apply``
  - ``PeerUpdate`` — ``ipv6``
  - ``Job`` — ``created_at``, ``completed_at``, ``triggered_by``, ``failed_reason``
  - ``User`` — ``password`` (returned only immediately after creation),
    ``pending_approval``, ``idp_id``
  - ``UserInvite`` — ``auto_groups``, ``created_at``, ``expired``, ``invite_token``
  - ``UserStatus`` — new ``BLOCKED`` member

- Python 3.14 added to the tested matrix and PyPI trove classifiers.

Changed
~~~~~~~

- **Event streaming endpoint path** — ``client.cloud.event_streaming`` methods now
  target ``/api/event-streaming`` (previously ``/api/integrations/event-streaming``),
  matching the current NetBird OpenAPI specification.
- ``mypy`` now loads the ``pydantic.mypy`` plugin; optional ``graphviz`` /
  ``diagrams`` imports use an ``ignore_missing_imports`` override instead of inline
  ``# type: ignore`` comments.

Fixed
~~~~~

- **Paginated event responses** — ``get_audit_events()``,
  ``get_network_traffic_events()`` and ``get_proxy_events()`` accept both the legacy
  bare-list response and the newer paginated envelope
  (``{"data": [...], "page": ..., "total_records": ...}``). The envelope form
  previously raised ``ValueError: Expected list response``.
- **``GeoLocationsResource.list_countries()``** returns a clean list of 2-letter ISO
  code strings for both response shapes: a bare list of codes (per the OpenAPI spec)
  and deployments that return ``{"country_code", "country_name"}`` objects.
  Previously the object form was stringified into unusable entries. A non-list
  response now raises ``ValueError``.
- **Non-dict API error bodies** — ``APIClient._handle_response()`` no longer assumes
  the parsed error body is a ``dict`` when building the exception message; list or
  scalar bodies fall back to ``HTTP <status>``.
- **``TokenAuth``** rejects whitespace-only tokens (previously only wholly-empty
  strings raised).

Dependencies
~~~~~~~~~~~~

- ``mcp[cli]`` constrained to ``>=1.0.0,<2.0.0`` to stay on the compatible 1.x API.

Documentation
~~~~~~~~~~~~~

- Diagram install instructions updated to ``pip install "netbird[viz]"`` across the
  README and Sphinx docs.
- ``auth_scheme`` shown in the Quick Start example.
- Minimum supported Python corrected to 3.10 in the contributing guide.

[1.3.0] - 2026-03-31
---------------------

Added
~~~~~

- **MCP Server** (``netbird.mcp.server``) — 25 NetBird management tools exposed via `Model Context Protocol <https://modelcontextprotocol.io>`_

  - AI assistants (Claude Desktop, etc.) can now manage NetBird resources through natural language
  - Tools cover: account, users, peers, groups, policies, networks, setup keys, DNS, posture checks, audit events, network diagrams
  - See :doc:`user-guide/mcp-server` for setup instructions

- **``mcp`` optional dependency** — compatible MCP 1.x release via ``pip install "netbird[mcp]"``
- **``netbird-mcp`` CLI entry point** — Start the MCP server from the command line

[1.2.1] - 2026-03-28
---------------------

Fixed
~~~~~

- **PolicyRule** ``sources`` / ``destinations`` — Changed type from ``List[Dict]`` to ``List[Union[str, Dict]]``. The NetBird API expects plain string group IDs on writes (POST/PUT) but returns full objects on reads (GET).

[1.2.0] - 2026-03-27
---------------------

Added
~~~~~

**New Resources:**

- **Posture Checks** (``client.posture_checks``) - Device compliance verification
- **Geo Locations** (``client.geo_locations``) - Geographic data queries
- **DNS Zones** (``client.dns_zones``) - Custom DNS zone and record management
- **Identity Providers** (``client.identity_providers``) - OAuth2/OIDC provider management
- **Instance** (``client.instance``) - Instance status, version, and setup

**Cloud Namespace** (``client.cloud.*``):

- **Services** - Reverse proxy service and domain management
- **Ingress** - Ingress port allocation and peer management
- **EDR** - Endpoint Detection & Response integrations:

  - ``client.cloud.edr.peers`` - EDR peer bypass management
  - ``client.cloud.edr.falcon`` - CrowdStrike Falcon
  - ``client.cloud.edr.huntress`` - Huntress
  - ``client.cloud.edr.intune`` - Microsoft Intune
  - ``client.cloud.edr.sentinelone`` - SentinelOne

- **MSP** - Multi-tenant management for MSPs
- **Invoices** - Billing invoice retrieval (PDF/CSV)
- **Usage** - Billing usage statistics
- **Event Streaming** - Event streaming integrations (Datadog, S3, etc.)
- **IDP/SCIM** - SCIM identity provider integrations

**Existing Resource Enhancements:**

- **Users** - ``approve``, ``reject``, ``change_password``, invite management
- **Peers** - ``create_temporary_access``, job management
- **Events** - ``get_proxy_events`` with 16 filter parameters
- **Networks** - ``list_all_routers`` for global router listing
- **Account Settings** - New fields for peer inactivity, DNS resolution, network range
- **PolicyRule** - ``port_ranges``, ``authorized_groups``, resource fields with camelCase aliases

Changed
~~~~~~~
- **BaseModel** - Changed Pydantic ``extra`` from ``"forbid"`` to ``"allow"`` for forward compatibility
- **Routes API** - All methods now emit ``DeprecationWarning`` (use Networks API instead)
- **_parse_list_response** - Handles ``null`` API responses gracefully
- Cloud-only endpoint detection with ``UserWarning`` for self-hosted instances

Fixed
~~~~~
- Event Streaming endpoint path (``event-streaming`` -> ``integrations/event-streaming``)
- Null list responses from API now return empty lists

[1.1.0] - 2026-03-21
---------------------

Changed
~~~~~~~
- Removed ``use_ssl`` parameter (always uses HTTPS, pass ``http://`` prefix for non-SSL)
- Switched documentation from Jekyll to Sphinx with Furo theme
- Cleaned up diagram test files

[1.0.0] - 2026-03-20
---------------------

Added
~~~~~
- Initial release of NetBird Python Client
- Complete API coverage for 11 NetBird API resources
- Pydantic models for type-safe input validation
- Comprehensive error handling with specific exception types
- Network topology visualization (Mermaid, Graphviz, Python Diagrams)
- Token-based authentication
- Python 3.9+ compatibility
- 98% test coverage
