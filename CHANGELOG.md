# Changelog

All notable changes to the NetBird Python Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
