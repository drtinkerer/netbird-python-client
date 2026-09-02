# Changelog

All notable changes to the NetBird Python Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2026-09-02

### Added

- **Bearer-token authentication.** `APIClient(host=..., api_token=..., auth_scheme="Bearer")`
  (and `TokenAuth(token, scheme="Bearer")`) now sends `Authorization: Bearer <token>`
  instead of the default `Authorization: Token <token>`, for OAuth2 / OIDC access
  tokens. `auth_scheme` accepts `"Token"` (default) or `"Bearer"`; any other value
  raises `ValueError`. New `netbird.auth.AuthScheme` type alias.
- **`viz` optional dependency group.** `pip install "netbird[viz]"` installs
  `graphviz>=0.20.0` and `diagrams>=0.23.0` for Graphviz / Python-Diagrams diagram
  output. The Graphviz system binary is still required separately
  (e.g. `brew install graphviz`).
- **New model fields tracking recent NetBird API revisions:**
  - `AccountSettings`: `network_range_v6`, `dns_domain`, `regular_users_view_blocked`,
    `groups_propagation_enabled`, `jwt_allow_groups`, `auto_update_always`,
    `metrics_push_enabled`, `agent_network_only`, `dashboard_features`,
    `local_mfa_enabled`, `ipv6_enabled_groups`
  - `RouteCreate` / `RouteUpdate`: `skip_auto_apply`
  - `PeerUpdate`: `ipv6`
  - `Job`: `created_at`, `completed_at`, `triggered_by`, `failed_reason`
  - `User`: `password` (returned only immediately after creation), `pending_approval`,
    `idp_id`
  - `UserInvite`: `auto_groups`, `created_at`, `expired`, `invite_token`
  - `UserStatus`: new `BLOCKED` member
- Python 3.14 added to the tested matrix (CI, publish workflow) and to the PyPI
  trove classifiers.

### Changed

- **Event streaming endpoint path.** `client.cloud.event_streaming.list()`,
  `create()`, `get()`, `update()` and `delete()` now target `/api/event-streaming`
  (previously `/api/integrations/event-streaming`), matching the current NetBird
  OpenAPI specification.
- `mypy` configuration now loads the `pydantic.mypy` plugin, and the optional
  `graphviz` / `diagrams` imports use an `ignore_missing_imports` override instead
  of inline `# type: ignore[import-untyped]` comments.

### Fixed

- **Paginated event responses.** `EventsResource.get_audit_events()`,
  `get_network_traffic_events()` and `get_proxy_events()` now accept both the
  legacy bare-list response and the newer paginated envelope
  (`{"data": [...], "page": ..., "total_records": ...}`). The envelope form
  previously raised `ValueError: Expected list response`.
- **`GeoLocationsResource.list_countries()`** now returns a clean `List[str]` of
  2-letter ISO codes for both response shapes: a bare list of code strings (per
  the OpenAPI spec) and deployments that return
  `{"country_code": ..., "country_name": ...}` objects. Previously the object form
  was stringified into unusable `"{'country_code': ...}"` entries. A non-list
  response now raises `ValueError` instead of being returned unchecked.
- **Non-dict API error bodies.** `APIClient._handle_response()` no longer assumes
  the parsed error body is a `dict` when building the exception message; list or
  scalar bodies fall back to `HTTP <status>`.
- **`TokenAuth`** now rejects whitespace-only tokens (previously only wholly-empty
  strings raised `ValueError`).

### Dependencies

- `mcp[cli]` constrained to `>=1.0.0,<2.0.0` to stay on the compatible 1.x API
  surface.

### Documentation

- Diagram install instructions updated to `pip install "netbird[viz]"` across the
  README and Sphinx docs.
- `auth_scheme` shown in the Quick Start example.
- Minimum supported Python corrected to 3.10 in the contributing guide; test-count
  and coverage phrasing refreshed.

## [1.3.0] - 2026-03-31

### Added
- **MCP Server** (`netbird.mcp.server`) - 25 NetBird management tools exposed via Model Context Protocol
  - AI assistants (Claude Desktop, etc.) can now manage NetBird resources through natural language
  - Tools cover: account, users, peers, groups, policies, networks, setup keys, DNS, posture checks, audit events, network diagrams
  - Install with `pip install "netbird[mcp]"` and run with `netbird-mcp` CLI entry point
  - Configure via `NETBIRD_HOST` and `NETBIRD_API_TOKEN` environment variables
- **`mcp` optional dependency** - compatible MCP 1.x release available via `pip install "netbird[mcp]"`
- **`netbird-mcp` CLI entry point** - Start the MCP server from the command line

## [1.2.1] - 2026-03-28

### Fixed
- **PolicyRule `sources` / `destinations`** - Changed type from `List[Dict]` to `List[Union[str, Dict]]`. The NetBird API expects plain string group IDs on writes (POST/PUT) but returns full objects on reads (GET). Sending `[{"id": "..."}]` caused a `400 "couldn't parse JSON request"` error. Correct usage is `sources=["group-id"]`.

## [1.2.0] - 2026-03-27

### Added

#### New Resources
- **Posture Checks** (`client.posture_checks`) - Device compliance verification with CRUD operations
- **Geo Locations** (`client.geo_locations`) - Geographic data queries (countries, cities)
- **DNS Zones** (`client.dns_zones`) - Custom DNS zone and record management (zone CRUD + record CRUD)
- **Identity Providers** (`client.identity_providers`) - OAuth2/OIDC provider management
- **Instance** (`client.instance`) - Instance status, version, and initial setup

#### Cloud Namespace (`client.cloud.*`)
Cloud-only resources accessible via `client.cloud`:
- **Services** (`client.cloud.services`) - Reverse proxy service and domain management
- **Ingress** (`client.cloud.ingress`) - Ingress port allocation and peer management
- **EDR** (`client.cloud.edr`) - Endpoint Detection & Response integrations:
  - `client.cloud.edr.peers` - EDR peer bypass management
  - `client.cloud.edr.falcon` - CrowdStrike Falcon integration
  - `client.cloud.edr.huntress` - Huntress integration
  - `client.cloud.edr.intune` - Microsoft Intune integration
  - `client.cloud.edr.sentinelone` - SentinelOne integration
- **MSP** (`client.cloud.msp`) - Multi-tenant management for MSPs
- **Invoices** (`client.cloud.invoices`) - Billing invoice retrieval (PDF/CSV)
- **Usage** (`client.cloud.usage`) - Billing usage statistics
- **Event Streaming** (`client.cloud.event_streaming`) - Event streaming integrations (Datadog, S3, etc.)
- **IDP/SCIM** (`client.cloud.idp_scim`) - SCIM identity provider integrations

#### Existing Resource Enhancements
- **Users** - Added `approve`, `reject`, `change_password`, `list_invites`, `create_invite`, `delete_invite`, `regenerate_invite`, `get_invite_info`, `accept_invite` methods
- **Peers** - Added `create_temporary_access`, `list_jobs`, `create_job`, `get_job` methods
- **Events** - Added `get_proxy_events` with 16 filter parameters for reverse proxy event logging
- **Networks** - Added `list_all_routers` for global router listing across all networks
- **Account Settings** - Added `peer_inactivity_expiration`, `routing_peer_dns_resolution_enabled`, `network_range`, `peer_expose_enabled`, `peer_expose_groups`, `auto_update_version`, `embedded_idp_enabled`, `local_auth_disabled`, `extra_settings` fields
- **Account** - Added `onboarding` field
- **PeerUpdate** - Added `ip` field
- **PolicyRule** - Added `port_ranges`, `authorized_groups`, `source_resource`, `destination_resource` with camelCase aliases
- **User Models** - Added `UserInviteCreate` and `UserInvite` models

### Changed
- **BaseModel** - Changed Pydantic `extra` config from `"forbid"` to `"allow"` for forward-compatible API responses. Unknown fields from newer API versions are now accepted and included in `model_dump()`.
- **Routes API** - All methods now emit `DeprecationWarning` recommending migration to Networks API
- **`_parse_list_response`** - Now handles `null` API responses (returns `[]` instead of raising `ValueError`)
- Version bumped from 1.1.0 to 1.2.0

### Fixed
- **Event Streaming endpoint path** - Corrected from `event-streaming` to `integrations/event-streaming`
- **Null list responses** - API returns `null` instead of `[]` for empty resource lists; now handled gracefully

## [1.1.0] - 2026-03-21

### Changed
- Removed `use_ssl` parameter (always uses HTTPS by default, pass `http://` prefix for non-SSL)
- Switched documentation from Jekyll to Sphinx
- Cleaned up diagram test files

## [0.1.0] - 2026-03-20

### Added
- Initial release of NetBird Python Client
- Complete API coverage for all 11 NetBird API resources:
  - Accounts, Users, Tokens, Peers, Setup Keys, Groups
  - Networks (with nested Resources/Routers), Policies, Routes, DNS, Events
- Modern Python package structure with pyproject.toml
- Type-safe Pydantic models for all API objects
- Comprehensive error handling with specific exception types
- Network topology visualization (Mermaid, Graphviz, Python Diagrams)
- Flexible authentication support (PAT, service user tokens, bearer tokens)
- Context manager support for resource cleanup
- 98% test coverage with unit and integration tests
