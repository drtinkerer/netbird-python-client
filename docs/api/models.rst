Models
======

Pydantic models provide type-safe input validation for API requests. All models
inherit from ``BaseModel`` with ``extra="allow"`` for forward compatibility.

.. module:: netbird.models

Base Model
----------

.. autoclass:: netbird.models.common.BaseModel
   :members:
   :show-inheritance:

All models use these configurations:

- ``extra="allow"`` - Accepts unknown fields from newer API versions
- ``validate_assignment=True`` - Validates field assignments after creation
- ``use_enum_values=True`` - Uses enum values instead of enum instances
- ``populate_by_name=True`` - Allows populating by field name or alias

Enumerations
------------

.. autoclass:: netbird.models.common.UserRole
   :members:
   :undoc-members:

   Values: ``admin``, ``user``, ``owner``

.. autoclass:: netbird.models.common.UserStatus
   :members:
   :undoc-members:

   Values: ``active``, ``disabled``, ``invited``

.. autoclass:: netbird.models.common.SetupKeyType
   :members:
   :undoc-members:

   Values: ``reusable``, ``one-off``

.. autoclass:: netbird.models.common.NetworkType
   :members:
   :undoc-members:

   Values: ``ipv4``, ``ipv6``, ``domain``

.. autoclass:: netbird.models.common.Protocol
   :members:
   :undoc-members:

   Values: ``tcp``, ``udp``, ``icmp``, ``all``

.. autoclass:: netbird.models.common.PolicyAction
   :members:
   :undoc-members:

   Values: ``accept``, ``drop``

.. autoclass:: netbird.models.common.TrafficDirection
   :members:
   :undoc-members:

   Values: ``sent``, ``received``

.. autoclass:: netbird.models.common.ConnectionType
   :members:
   :undoc-members:

   Values: ``relay``, ``p2p``

Account Models
--------------

.. autoclass:: netbird.models.account.Account
   :members:
   :undoc-members:

.. autoclass:: netbird.models.account.AccountSettings
   :members:
   :undoc-members:

User Models
-----------

.. autoclass:: netbird.models.user.User
   :members:
   :undoc-members:

.. autoclass:: netbird.models.user.UserCreate
   :members:
   :undoc-members:

   .. code-block:: python

      from netbird.models import UserCreate

      user = UserCreate(
          email="alice@company.com",
          name="Alice",
          role="admin",           # or UserRole.ADMIN
          is_service_user=False,
          auto_groups=["default-group"]
      )

.. autoclass:: netbird.models.user.UserUpdate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.user.UserInvite
   :members:
   :undoc-members:

.. autoclass:: netbird.models.user.UserInviteCreate
   :members:
   :undoc-members:

Token Models
------------

.. autoclass:: netbird.models.token.Token
   :members:
   :undoc-members:

.. autoclass:: netbird.models.token.TokenCreate
   :members:
   :undoc-members:

   ``expires_in`` must be between 1 and 365 days.

Peer Models
-----------

.. autoclass:: netbird.models.peer.Peer
   :members:
   :undoc-members:

.. autoclass:: netbird.models.peer.PeerUpdate
   :members:
   :undoc-members:

Setup Key Models
----------------

.. autoclass:: netbird.models.setup_key.SetupKey
   :members:
   :undoc-members:

.. autoclass:: netbird.models.setup_key.SetupKeyCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.setup_key.SetupKeyUpdate
   :members:
   :undoc-members:

Group Models
------------

.. autoclass:: netbird.models.group.Group
   :members:
   :undoc-members:

.. autoclass:: netbird.models.group.GroupCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.group.GroupUpdate
   :members:
   :undoc-members:

Network Models
--------------

.. autoclass:: netbird.models.network.Network
   :members:
   :undoc-members:

.. autoclass:: netbird.models.network.NetworkCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.network.NetworkUpdate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.network.NetworkResource
   :members:
   :undoc-members:

.. autoclass:: netbird.models.network.NetworkRouter
   :members:
   :undoc-members:

Policy Models
-------------

.. autoclass:: netbird.models.policy.Policy
   :members:
   :undoc-members:

.. autoclass:: netbird.models.policy.PolicyCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.policy.PolicyRule
   :members:
   :undoc-members:

.. autoclass:: netbird.models.policy.PolicyUpdate
   :members:
   :undoc-members:

Route Models
------------

.. deprecated::
   Routes are deprecated. Use Networks API instead.

.. autoclass:: netbird.models.route.Route
   :members:
   :undoc-members:

.. autoclass:: netbird.models.route.RouteCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.route.RouteUpdate
   :members:
   :undoc-members:

DNS Models
----------

.. autoclass:: netbird.models.dns.DNSNameserverGroup
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns.DNSSettings
   :members:
   :undoc-members:

DNS Zone Models
---------------

.. autoclass:: netbird.models.dns_zone.DNSZone
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns_zone.DNSZoneCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns_zone.DNSZoneUpdate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns_zone.DNSRecord
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns_zone.DNSRecordCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.dns_zone.DNSRecordUpdate
   :members:
   :undoc-members:

Event Models
------------

.. autoclass:: netbird.models.event.AuditEvent
   :members:
   :undoc-members:

.. autoclass:: netbird.models.event.NetworkTrafficEvent
   :members:
   :undoc-members:

Posture Check Models
--------------------

.. autoclass:: netbird.models.posture_check.PostureCheck
   :members:
   :undoc-members:

.. autoclass:: netbird.models.posture_check.PostureCheckCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.posture_check.PostureCheckUpdate
   :members:
   :undoc-members:

Identity Provider Models
------------------------

.. autoclass:: netbird.models.identity_provider.IdentityProvider
   :members:
   :undoc-members:

.. autoclass:: netbird.models.identity_provider.IdentityProviderCreate
   :members:
   :undoc-members:

.. autoclass:: netbird.models.identity_provider.IdentityProviderUpdate
   :members:
   :undoc-members:

Job Models
----------

.. autoclass:: netbird.models.job.Job
   :members:
   :undoc-members:

.. autoclass:: netbird.models.job.JobCreate
   :members:
   :undoc-members:

Type Aliases
------------

- ``ResourceId`` - String type for resource identifiers
- ``Timestamp`` - Datetime type for timestamps
