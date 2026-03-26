Error Handling
==============

The NetBird Python client provides a hierarchy of specific exception types for different
API error conditions, making it easy to handle errors precisely.

Exception Hierarchy
-------------------

.. code-block:: text

   Exception
   └── NetBirdAPIError              (base for all API errors)
       ├── NetBirdAuthenticationError   (401 Unauthorized)
       ├── NetBirdValidationError       (400 Bad Request)
       ├── NetBirdNotFoundError         (404 Not Found)
       ├── NetBirdRateLimitError        (429 Too Many Requests)
       └── NetBirdServerError           (5xx Server Errors)

All exceptions are importable from ``netbird.exceptions``:

.. code-block:: python

   from netbird.exceptions import (
       NetBirdAPIError,
       NetBirdAuthenticationError,
       NetBirdValidationError,
       NetBirdNotFoundError,
       NetBirdRateLimitError,
       NetBirdServerError,
   )

Exception Details
-----------------

NetBirdAPIError
~~~~~~~~~~~~~~~

Base exception for all API errors. All other exceptions inherit from this.

.. list-table::
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``message``
     - ``str``
     - Human-readable error message
   * - ``status_code``
     - ``int | None``
     - HTTP status code
   * - ``response_data``
     - ``dict``
     - Raw response data from the API

NetBirdAuthenticationError
~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised for **401 Unauthorized** responses. Indicates invalid, expired, or missing API token.

.. code-block:: python

   try:
       client.peers.list()
   except NetBirdAuthenticationError:
       print("Invalid API token. Please check your credentials.")

NetBirdValidationError
~~~~~~~~~~~~~~~~~~~~~~

Raised for **400 Bad Request** responses. Indicates malformed request data.

.. code-block:: python

   try:
       client.users.create(user_data)
   except NetBirdValidationError as e:
       print(f"Validation error: {e.message}")
       print(f"Details: {e.response_data}")

NetBirdNotFoundError
~~~~~~~~~~~~~~~~~~~~

Raised for **404 Not Found** responses. Resource doesn't exist or insufficient permissions.

.. code-block:: python

   try:
       peer = client.peers.get("nonexistent-id")
   except NetBirdNotFoundError:
       print("Peer not found")

NetBirdRateLimitError
~~~~~~~~~~~~~~~~~~~~~

Raised for **429 Too Many Requests** responses. Includes ``retry_after`` seconds.

.. code-block:: python

   import time

   try:
       result = client.peers.list()
   except NetBirdRateLimitError as e:
       if e.retry_after:
           print(f"Rate limited. Retrying in {e.retry_after}s...")
           time.sleep(e.retry_after)
           result = client.peers.list()

NetBirdServerError
~~~~~~~~~~~~~~~~~~

Raised for **5xx** server errors. Indicates temporary server issues.

.. code-block:: python

   try:
       result = client.peers.list()
   except NetBirdServerError:
       print("Server error. Try again later.")

Comprehensive Error Handling
----------------------------

Handle errors from most specific to most general:

.. code-block:: python

   from netbird.exceptions import (
       NetBirdAPIError,
       NetBirdAuthenticationError,
       NetBirdNotFoundError,
       NetBirdRateLimitError,
       NetBirdServerError,
       NetBirdValidationError,
   )

   try:
       peer = client.peers.get(peer_id)
   except NetBirdNotFoundError:
       print(f"Peer {peer_id} not found")
   except NetBirdAuthenticationError:
       print("Authentication failed - check your API token")
   except NetBirdValidationError as e:
       print(f"Invalid request: {e.message}")
   except NetBirdRateLimitError as e:
       print(f"Rate limited. Retry after {e.retry_after}s")
   except NetBirdServerError:
       print("Server error - try again later")
   except NetBirdAPIError as e:
       print(f"Unexpected API error ({e.status_code}): {e.message}")

Pydantic Validation Errors
---------------------------

Input models raise ``pydantic.ValidationError`` for invalid data before any API call:

.. code-block:: python

   from pydantic import ValidationError
   from netbird.models import UserCreate

   try:
       user = UserCreate(email="not-an-email", name="Test")
   except ValidationError as e:
       for error in e.errors():
           print(f"Field: {error['loc']}, Error: {error['msg']}")

This catches errors before making network requests, providing faster feedback.

Cloud-Only Endpoint Warnings
-----------------------------

When accessing cloud-only resources (``client.cloud.*``) from a self-hosted instance,
a ``UserWarning`` is emitted:

.. code-block:: python

   import warnings

   with warnings.catch_warnings(record=True) as w:
       warnings.simplefilter("always")
       client = APIClient(
           host="netbird.mycompany.com",
           api_token="token"
       )
       _ = client.cloud  # Triggers warning
       if w:
           print(f"Warning: {w[0].message}")
