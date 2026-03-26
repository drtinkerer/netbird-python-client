Authentication
==============

The NetBird Python client uses **Personal Access Tokens (PAT)** for API authentication. This guide covers how to obtain and use tokens securely.

Obtaining an API Token
----------------------

NetBird Cloud
~~~~~~~~~~~~~

1. Log in to the `NetBird Dashboard <https://app.netbird.io>`_
2. Navigate to **Settings** > **API Tokens**
3. Click **Create Token**
4. Copy the generated token immediately (it won't be shown again)

Self-Hosted
~~~~~~~~~~~

1. Access your NetBird management interface
2. Navigate to the API token section
3. Generate a new token with the required permissions

Basic Authentication
--------------------

.. code-block:: python

   from netbird import APIClient

   client = APIClient(
       host="api.netbird.io",
       api_token="nbp_your_token_here"
   )

Environment Variables
---------------------

Store credentials securely using environment variables:

.. code-block:: python

   import os
   from netbird import APIClient

   client = APIClient(
       host=os.environ["NETBIRD_HOST"],
       api_token=os.environ["NETBIRD_API_TOKEN"]
   )

Set them in your shell:

.. code-block:: bash

   export NETBIRD_HOST="api.netbird.io"
   export NETBIRD_API_TOKEN="nbp_your_token_here"

Or use a ``.env`` file with `python-dotenv <https://pypi.org/project/python-dotenv/>`_:

.. code-block:: python

   from dotenv import load_dotenv
   load_dotenv()

   client = APIClient(
       host=os.environ["NETBIRD_HOST"],
       api_token=os.environ["NETBIRD_API_TOKEN"]
   )

Token Management via API
------------------------

You can manage API tokens programmatically:

.. code-block:: python

   # List all tokens for a user
   tokens = client.tokens.list(user_id="user-123")

   # Create a new token
   from netbird.models import TokenCreate
   token_data = TokenCreate(name="ci-token", expires_in=30)  # 30 days
   new_token = client.tokens.create(user_id="user-123", data=token_data)
   print(f"Token: {new_token['plain_token']}")

   # Delete a token
   client.tokens.delete(user_id="user-123", token_id="token-456")

Token Expiration
~~~~~~~~~~~~~~~~

Tokens have a configurable expiration between 1 and 365 days:

.. code-block:: python

   from netbird.models import TokenCreate

   # Short-lived token for CI/CD
   ci_token = TokenCreate(name="ci-pipeline", expires_in=1)  # 1 day

   # Long-lived token for service accounts
   service_token = TokenCreate(name="monitoring", expires_in=365)  # 1 year

Service Users
-------------

For automated workflows, use service user tokens:

.. code-block:: python

   from netbird.models import UserCreate

   # Create a service user
   service_user = UserCreate(
       email="bot@company.com",
       name="Automation Bot",
       is_service_user=True,
       role="admin"
   )
   user = client.users.create(service_user)

   # Create a token for the service user
   from netbird.models import TokenCreate
   token_data = TokenCreate(name="automation", expires_in=365)
   token = client.tokens.create(user_id=user['id'], data=token_data)

Connection Configuration
------------------------

.. code-block:: python

   client = APIClient(
       host="your-netbird-host.com",    # API host
       api_token="your-token",          # PAT token
       timeout=60.0,                    # Request timeout (default: 30s)
       base_path="/api",                # API base path (default: "/api")
   )

HTTPS is used by default. For non-SSL connections (development only):

.. code-block:: python

   client = APIClient(
       host="http://localhost:33073",
       api_token="your-token"
   )

Security Best Practices
-----------------------

1. **Never hardcode tokens** in source code
2. **Use environment variables** or secret management systems
3. **Rotate tokens regularly**, especially after team changes
4. **Use short-lived tokens** for CI/CD pipelines
5. **Use service users** for automated workflows instead of personal tokens
6. **Limit token scope** by using the minimum required permissions
