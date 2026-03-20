# NetBird Python Client — Full API Parity Upgrade

**Date**: 2026-03-21
**Current version**: 1.1.0
**Strategy**: Phased releases (3 phases), backward-compatible throughout

## Decisions

- **Pydantic `extra` policy**: Switch from `extra="forbid"` to `extra="allow"` globally
- **Cloud endpoints**: Namespaced under `client.cloud` (not flat top-level)
- **Tests**: One test file per resource
- **Routes**: Keep with deprecation warning (no removal planned)
- **Phase 4 (2.0 breaking cleanup)**: Skipped — no breaking changes needed

---

## Phase 1 — v1.2.0: Foundation + Existing Resource Gaps

### 1.1 Global Model Config

Change `src/netbird/models/common.py` `BaseModel`:
```python
extra="forbid"  →  extra="allow"
```

Backward-compatible: existing code sending known fields still works. Unknown fields from API responses pass through silently.

### 1.2 Update Existing Models (New Optional Fields)

All additions are optional with defaults — no breaking changes.

**AccountSettings** — add:
- `peer_inactivity_expiration: Optional[int] = None`
- `routing_peer_dns_resolution_enabled: Optional[bool] = None`
- `network_range: Optional[str] = None`
- `peer_expose_enabled: Optional[bool] = None`
- `peer_expose_groups: Optional[List[str]] = None`
- `auto_update_version: Optional[str] = None`
- `embedded_idp_enabled: Optional[bool] = None`
- `local_auth_disabled: Optional[bool] = None`
- `extra_settings: Optional[Dict[str, Any]] = Field(default=None, alias="extra")` (peer_approval, user_approval, traffic_logs, packet_counter) — renamed to avoid collision with Pydantic's `extra` config when using `extra="allow"`

**Account** — add:
- `onboarding: Optional[Dict[str, Any]] = None`

**PeerUpdate** — add:
- `ip: Optional[str] = None`

**PolicyRule** — add:
- `port_ranges: Optional[List[Dict[str, Any]]] = None`
- `authorized_groups: Optional[Dict[str, Any]] = None`
- `source_resource: Optional[Dict[str, Any]] = Field(default=None, alias="sourceResource")`
- `destination_resource: Optional[Dict[str, Any]] = Field(default=None, alias="destinationResource")`

### 1.3 New Endpoints on Existing Resources

**UsersResource** — 9 new methods:
| Method | HTTP | Path |
|--------|------|------|
| `approve(user_id)` | POST | `/users/{id}/approve` |
| `reject(user_id)` | DELETE | `/users/{id}/reject` |
| `change_password(user_id, old_password, new_password)` | PUT | `/users/{id}/password` |
| `list_invites()` | GET | `/users/invites` |
| `create_invite(invite_data)` | POST | `/users/invites` |
| `delete_invite(invite_id)` | DELETE | `/users/invites/{id}` |
| `regenerate_invite(invite_id, expires_in)` | POST | `/users/invites/{id}/regenerate` |
| `get_invite_info(token)` | GET | `/users/invites/{token}` |
| `accept_invite(token, password)` | POST | `/users/invites/{token}/accept` |

**PeersResource** — 1 new method:
| Method | HTTP | Path |
|--------|------|------|
| `create_temporary_access(peer_id, data)` | POST | `/peers/{id}/temporary-access` |

**EventsResource** — 1 new method:
| Method | HTTP | Path |
|--------|------|------|
| `get_proxy_events(**filters)` | GET | `/events/proxy` |

Supported filters: `page`, `page_size`, `sort_by`, `sort_order`, `search`, `source_ip`, `host`, `path`, `user_id`, `user_email`, `user_name`, `method`, `status`, `status_code`, `start_date`, `end_date`

**NetworksResource** — 1 new method:
| Method | HTTP | Path |
|--------|------|------|
| `list_all_routers()` | GET | `/networks/routers` |

### 1.4 New Models

**`src/netbird/models/user.py`** — add:
- `UserInviteCreate(name, email, role, auto_groups, expires_in)`
- `UserInvite(id, email, name, role, expires_at, token, invited_by, valid)`

Note on invite identifiers: `delete_invite(invite_id)` and `regenerate_invite(invite_id)` use the invite's `id` field. `get_invite_info(token)` and `accept_invite(token)` use the invite's `token` field. These are different path parameters for different endpoints.

### 1.5 Version

- Bump `__version__` to `1.2.0` in `src/netbird/__init__.py`

### 1.6 Tests (Phase 1)

New test files:
- `tests/unit/test_users.py` — all User endpoints including approve/reject/password/invites
- `tests/unit/test_peers.py` — all Peer endpoints including temporary-access
- `tests/unit/test_events.py` — all Event endpoints including proxy
- `tests/unit/test_networks.py` — all Network endpoints including list_all_routers
- `tests/unit/test_models.py` — model field additions, `extra="allow"` behavior

Existing test files (`test_client.py`, `test_client_comprehensive.py`, `test_coverage_improvements.py`) are kept as-is. New per-resource test files cover the new methods and avoid duplication with existing tests.

---

## Phase 2 — v1.3.0: New Core Resources

### 2.1 Posture Checks

**Resource**: `src/netbird/resources/posture_checks.py` → `PostureChecksResource`
**Models**: `src/netbird/models/posture_check.py`
- `PostureCheck(id, name, description, checks)`
- `PostureCheckCreate(name, description, checks)` — `checks` is Dict with optional keys: `nb_version_check`, `os_version_check`, `geo_location_check`, `peer_network_range_check`, `process_check`
- `PostureCheckUpdate(name, description, checks)`

**Client property**: `client.posture_checks`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/posture-checks` |
| `create(data)` | POST | `/posture-checks` |
| `get(id)` | GET | `/posture-checks/{id}` |
| `update(id, data)` | PUT | `/posture-checks/{id}` |
| `delete(id)` | DELETE | `/posture-checks/{id}` |

### 2.2 Geo Locations

**Resource**: `src/netbird/resources/geo_locations.py` → `GeoLocationsResource`
**Models**: None — returns simple lists/dicts

**Client property**: `client.geo_locations`

| Method | HTTP | Path |
|--------|------|------|
| `list_countries()` | GET | `/locations/countries` |
| `list_cities(country_code)` | GET | `/locations/countries/{country}/cities` |

### 2.3 DNS Zones + Records

> **Note**: DNS Zones (`/dns/zones`) is a separate API concept from DNS Nameserver Groups (`/dns/nameservers`). The existing `client.dns` resource manages nameserver groups and DNS settings — it remains unchanged. `client.dns_zones` is a new, distinct resource for zone and record management. There is no overlap or deprecation.

**Resource**: `src/netbird/resources/dns_zones.py` → `DNSZonesResource`
**Models**: `src/netbird/models/dns_zone.py`
- `DNSZone(id, name, domain, enabled, enable_search_domain, distribution_groups)`
- `DNSZoneCreate(name, domain, enabled, enable_search_domain, distribution_groups)`
- `DNSZoneUpdate(name, domain, enabled, enable_search_domain, distribution_groups)`
- `DNSRecord(id, name, type, content, ttl)`
- `DNSRecordCreate(name, type, content, ttl)`
- `DNSRecordUpdate(name, type, content, ttl)`

**Client property**: `client.dns_zones`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/dns/zones` |
| `create(data)` | POST | `/dns/zones` |
| `get(zone_id)` | GET | `/dns/zones/{id}` |
| `update(zone_id, data)` | PUT | `/dns/zones/{id}` |
| `delete(zone_id)` | DELETE | `/dns/zones/{id}` |
| `list_records(zone_id)` | GET | `/dns/zones/{id}/records` |
| `create_record(zone_id, data)` | POST | `/dns/zones/{id}/records` |
| `get_record(zone_id, record_id)` | GET | `/dns/zones/{id}/records/{rid}` |
| `update_record(zone_id, record_id, data)` | PUT | `/dns/zones/{id}/records/{rid}` |
| `delete_record(zone_id, record_id)` | DELETE | `/dns/zones/{id}/records/{rid}` |

### 2.4 Identity Providers

**Resource**: `src/netbird/resources/identity_providers.py` → `IdentityProvidersResource`
**Models**: `src/netbird/models/identity_provider.py`
- `IdentityProvider(id, type, name, issuer, client_id)`
- `IdentityProviderCreate(type, name, issuer, client_id, client_secret)`
- `IdentityProviderUpdate(type, name, issuer, client_id, client_secret)`

Note: `client_secret` only in input models, never in read model.

**Client property**: `client.identity_providers`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/identity-providers` |
| `create(data)` | POST | `/identity-providers` |
| `get(id)` | GET | `/identity-providers/{id}` |
| `update(id, data)` | PUT | `/identity-providers/{id}` |
| `delete(id)` | DELETE | `/identity-providers/{id}` |

### 2.5 Instance

**Resource**: `src/netbird/resources/instance.py` → `InstanceResource`
**Models**: None — returns simple dicts

**Client property**: `client.instance`

| Method | HTTP | Path |
|--------|------|------|
| `get_status()` | GET | `/instance` |
| `get_version()` | GET | `/instance/version` |
| `setup(email, password, name)` | POST | `/setup` |

Note: These endpoints do not require authentication. The `APIClient` will still send auth headers (the server ignores them). No special handling needed — existing `_request()` works as-is.

### 2.6 Jobs (on PeersResource)

Jobs are scoped under peers in the API, so they belong on `PeersResource` rather than as a standalone resource. This follows the same pattern as Tokens on `UsersResource`.

**Models**: `src/netbird/models/job.py`
- `Job(id, workload, status)`
- `JobCreate(workload)`

**Added to `PeersResource`**:

| Method | HTTP | Path |
|--------|------|------|
| `list_jobs(peer_id)` | GET | `/peers/{id}/jobs` |
| `create_job(peer_id, data)` | POST | `/peers/{id}/jobs` |
| `get_job(peer_id, job_id)` | GET | `/peers/{id}/jobs/{jid}` |

### 2.7 Routes Deprecation Warning

Add to all `RoutesResource` methods:
```python
import warnings
warnings.warn(
    "Routes are deprecated by NetBird. Use Networks instead.",
    DeprecationWarning,
    stacklevel=2,
)
```

No functionality removed — warning only.

### 2.8 Version & Exports

- Bump `__version__` to `1.3.0`
- Add to `resources/__init__.py`: `PostureChecksResource`, `GeoLocationsResource`, `DNSZonesResource`, `IdentityProvidersResource`, `InstanceResource`
- Add to `models/__init__.py`: all new model classes (including `Job`, `JobCreate`)
- Add lazy properties to `APIClient`: `posture_checks`, `geo_locations`, `dns_zones`, `identity_providers`, `instance`
- Jobs methods added directly to existing `PeersResource` (no new lazy property needed)

### 2.9 Tests (Phase 2)

New test files:
- `tests/unit/test_posture_checks.py`
- `tests/unit/test_geo_locations.py`
- `tests/unit/test_dns_zones.py`
- `tests/unit/test_identity_providers.py`
- `tests/unit/test_instance.py`
- `tests/unit/test_jobs.py`

---

## Phase 3 — v1.4.0: Cloud Namespace

### 3.1 Architecture

New files:
- `src/netbird/cloud.py` — `CloudResources` and `EDRResources` namespace classes
- `src/netbird/resources/cloud/` — cloud resource modules
- `src/netbird/models/cloud/` — cloud model modules

**Client property**: `client.cloud` → `CloudResources`

`CloudResources` and `EDRResources` use the same lazy-loading pattern as `APIClient`. Both receive the `APIClient` reference via `__init__` and pass it to child resources:

```python
class CloudResources:
    def __init__(self, client: "APIClient") -> None:
        self.client = client
        self._edr: Optional["EDRResources"] = None

    @property
    def edr(self) -> "EDRResources":
        if self._edr is None:
            self._edr = EDRResources(self.client)
        return self._edr

class EDRResources:
    def __init__(self, client: "APIClient") -> None:
        self.client = client
```

Access patterns:
```
client.cloud.services          → ServicesResource
client.cloud.ingress           → IngressResource
client.cloud.edr               → EDRResources
client.cloud.edr.peers         → EDRPeersResource
client.cloud.edr.falcon        → EDRFalconResource
client.cloud.edr.huntress      → EDRHuntressResource
client.cloud.edr.intune        → EDRIntuneResource
client.cloud.edr.sentinelone   → EDRSentinelOneResource
client.cloud.msp               → MSPResource
client.cloud.invoices           → InvoiceResource
client.cloud.usage             → UsageResource
client.cloud.event_streaming   → EventStreamingResource
client.cloud.idp_scim          → IDPScimResource
```

### 3.2 Services (Reverse Proxy)

**Resource**: `src/netbird/resources/cloud/services.py` → `ServicesResource`
**Models**: `src/netbird/models/cloud/service.py`
- `Service`, `ServiceCreate`, `ServiceUpdate` — fields: name, domain, targets, enabled, pass_host_header, rewrite_redirects, auth
- `ServiceDomain`, `ServiceDomainCreate`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/reverse-proxies/services` |
| `create(data)` | POST | `/reverse-proxies/services` |
| `get(service_id)` | GET | `/reverse-proxies/services/{id}` |
| `update(service_id, data)` | PUT | `/reverse-proxies/services/{id}` |
| `delete(service_id)` | DELETE | `/reverse-proxies/services/{id}` |
| `list_clusters()` | GET | `/reverse-proxies/clusters` |
| `list_domains()` | GET | `/reverse-proxies/domains` |
| `create_domain(data)` | POST | `/reverse-proxies/domains` |
| `delete_domain(domain_id)` | DELETE | `/reverse-proxies/domains/{id}` |
| `validate_domain(domain_id)` | GET | `/reverse-proxies/domains/{id}/validate` |

### 3.3 Ingress Ports

**Resource**: `src/netbird/resources/cloud/ingress.py` → `IngressResource`
**Models**: `src/netbird/models/cloud/ingress.py`
- `PortAllocation`, `PortAllocationCreate`, `PortAllocationUpdate`
- `IngressPeer`, `IngressPeerCreate`, `IngressPeerUpdate`

| Method | HTTP | Path |
|--------|------|------|
| `list_ports(peer_id)` | GET | `/peers/{id}/ingress/ports` |
| `create_port(peer_id, data)` | POST | `/peers/{id}/ingress/ports` |
| `get_port(peer_id, alloc_id)` | GET | `/peers/{id}/ingress/ports/{aid}` |
| `update_port(peer_id, alloc_id, data)` | PUT | `/peers/{id}/ingress/ports/{aid}` |
| `delete_port(peer_id, alloc_id)` | DELETE | `/peers/{id}/ingress/ports/{aid}` |
| `list_peers()` | GET | `/ingress/peers` |
| `create_peer(data)` | POST | `/ingress/peers` |
| `get_peer(ingress_peer_id)` | GET | `/ingress/peers/{id}` |
| `update_peer(ingress_peer_id, data)` | PUT | `/ingress/peers/{id}` |
| `delete_peer(ingress_peer_id)` | DELETE | `/ingress/peers/{id}` |

### 3.4 EDR — Peer Bypass

**Resource**: `src/netbird/resources/cloud/edr_peers.py` → `EDRPeersResource`

| Method | HTTP | Path |
|--------|------|------|
| `bypass(peer_id)` | POST | `/peers/{id}/edr/bypass` |
| `revoke_bypass(peer_id)` | DELETE | `/peers/{id}/edr/bypass` |
| `list_bypassed()` | GET | `/peers/edr/bypassed` |

### 3.5 EDR — Falcon

**Resource**: `src/netbird/resources/cloud/edr_falcon.py` → `EDRFalconResource`
**Model** (in `src/netbird/models/cloud/edr.py`):
- `EDRFalconConfig(client_id, secret, cloud_id, groups, zta_score_threshold, enabled)`

| Method | HTTP | Path |
|--------|------|------|
| `create(data)` | POST | `/integrations/edr/falcon` |
| `get()` | GET | `/integrations/edr/falcon` |
| `update(data)` | PUT | `/integrations/edr/falcon` |
| `delete()` | DELETE | `/integrations/edr/falcon` |

### 3.6 EDR — Huntress

**Resource**: `src/netbird/resources/cloud/edr_huntress.py` → `EDRHuntressResource`
**Model**: `EDRHuntressConfig(api_key, api_secret, groups, last_synced_interval, enabled, match_attributes)`

Same 4 singleton endpoints at `/integrations/edr/huntress`.

### 3.7 EDR — Intune

**Resource**: `src/netbird/resources/cloud/edr_intune.py` → `EDRIntuneResource`
**Model**: `EDRIntuneConfig(client_id, tenant_id, secret, groups, last_synced_interval, enabled)`

Same 4 singleton endpoints at `/integrations/edr/intune`.

### 3.8 EDR — SentinelOne

**Resource**: `src/netbird/resources/cloud/edr_sentinelone.py` → `EDRSentinelOneResource`
**Model**: `EDRSentinelOneConfig(api_token, api_url, groups, last_synced_interval, enabled, match_attributes)`

Same 4 singleton endpoints at `/integrations/edr/sentinelone`.

### 3.9 MSP

**Resource**: `src/netbird/resources/cloud/msp.py` → `MSPResource`
**Models**: `src/netbird/models/cloud/msp.py`
- `MSPTenant(id, name, domain, groups, status)`
- `MSPTenantCreate(name, domain, groups)`
- `MSPTenantUpdate(name, groups)`

| Method | HTTP | Path |
|--------|------|------|
| `list_tenants()` | GET | `/integrations/msp/tenants` |
| `create_tenant(data)` | POST | `/integrations/msp/tenants` |
| `get_tenant(id)` | GET | `/integrations/msp/tenants/{id}` |
| `update_tenant(id, data)` | PUT | `/integrations/msp/tenants/{id}` |
| `unlink_tenant(id, owner)` | POST | `/integrations/msp/tenants/{id}/unlink` |
| `verify_domain(id)` | POST | `/integrations/msp/tenants/{id}/dns` |
| `create_subscription(id, price_id)` | POST | `/integrations/msp/tenants/{id}/subscription` |
| `invite_tenant(id)` | POST | `/integrations/msp/tenants/{id}/invite` |
| `respond_to_invite(id, value)` | PUT | `/integrations/msp/tenants/{id}/invite` |

### 3.10 Invoice

**Resource**: `src/netbird/resources/cloud/invoice.py` → `InvoiceResource`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/integrations/billing/invoices` |
| `get_pdf_url(invoice_id)` | GET | `/integrations/billing/invoices/{id}/pdf` |
| `get_csv(invoice_id)` | GET | `/integrations/billing/invoices/{id}/csv` |

### 3.11 Usage

**Resource**: `src/netbird/resources/cloud/usage.py` → `UsageResource`

| Method | HTTP | Path |
|--------|------|------|
| `get()` | GET | `/integrations/billing/usage` |

Returns: `{active_users, total_users, active_peers, total_peers}`

### 3.12 Event Streaming

**Resource**: `src/netbird/resources/cloud/event_streaming.py` → `EventStreamingResource`
**Models**: `src/netbird/models/cloud/event_streaming.py`
- `EventStreamingIntegration(id, platform, config, enabled)`
- `EventStreamingCreate(platform, config, enabled)`
- `EventStreamingUpdate(config, enabled)` — platform is immutable

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/event-streaming` |
| `create(data)` | POST | `/event-streaming` |
| `get(id)` | GET | `/event-streaming/{id}` |
| `update(id, data)` | PUT | `/event-streaming/{id}` |
| `delete(id)` | DELETE | `/event-streaming/{id}` |

### 3.13 IDP / SCIM

**Resource**: `src/netbird/resources/cloud/idp_scim.py` → `IDPScimResource`
**Models**: `src/netbird/models/cloud/idp_scim.py`
- `SCIMIntegration(id, prefix, provider, enabled, group_prefixes, user_group_prefixes)`
- `SCIMIntegrationCreate(prefix, provider, group_prefixes, user_group_prefixes)`
- `SCIMIntegrationUpdate(enabled, group_prefixes, user_group_prefixes)`

| Method | HTTP | Path |
|--------|------|------|
| `list()` | GET | `/integrations/scim-idp` |
| `create(data)` | POST | `/integrations/scim-idp` |
| `get(id)` | GET | `/integrations/scim-idp/{id}` |
| `update(id, data)` | PUT | `/integrations/scim-idp/{id}` |
| `delete(id)` | DELETE | `/integrations/scim-idp/{id}` |
| `regenerate_token(id)` | POST | `/integrations/scim-idp/{id}/token` |
| `get_logs(id)` | GET | `/integrations/scim-idp/{id}/logs` |

### 3.14 File Structure

```
src/netbird/
├── cloud.py                              # CloudResources, EDRResources
├── resources/cloud/
│   ├── __init__.py
│   ├── services.py
│   ├── ingress.py
│   ├── edr_peers.py
│   ├── edr_falcon.py
│   ├── edr_huntress.py
│   ├── edr_intune.py
│   ├── edr_sentinelone.py
│   ├── msp.py
│   ├── invoice.py
│   ├── usage.py
│   ├── event_streaming.py
│   └── idp_scim.py
├── models/cloud/
│   ├── __init__.py
│   ├── service.py
│   ├── ingress.py
│   ├── edr.py                            # All 4 EDR vendor configs
│   ├── msp.py
│   ├── event_streaming.py
│   └── idp_scim.py
tests/unit/cloud/
├── __init__.py
├── test_services.py
├── test_ingress.py
├── test_edr.py                           # All EDR vendors + peer bypass
├── test_msp.py
├── test_invoice.py
├── test_usage.py
├── test_event_streaming.py
└── test_idp_scim.py
```

### 3.15 Version & Exports

- Bump `__version__` to `1.4.0`
- Add `CloudResources` to `src/netbird/__init__.py`
- Cloud models exported from `src/netbird/models/cloud/__init__.py`
- Add `cloud` lazy property to `APIClient`

---

## Endpoint Count Summary

| Phase | New Endpoints | New Resources | New Models | New Test Files |
|-------|:---:|:---:|:---:|:---:|
| Phase 1 (v1.2.0) | 12 | 0 | 2 | 5 |
| Phase 2 (v1.3.0) | 25 | 5 (+Jobs on PeersResource) | 14 | 6 |
| Phase 3 (v1.4.0) | 64 | 13 | 18 | 8 |
| **Total** | **101** | **18+** | **34** | **19** |

## Backward Compatibility

- No existing methods removed or renamed
- No existing model fields removed
- `extra="allow"` only loosens validation
- All new model fields have defaults
- Routes kept with deprecation warning only
- Cloud resources fully additive under new namespace
