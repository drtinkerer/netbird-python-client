Exceptions
==========

.. module:: netbird.exceptions

The NetBird client provides a hierarchy of exception types for precise error handling.

Exception Hierarchy
-------------------

.. code-block:: text

   Exception
   └── NetBirdAPIError
       ├── NetBirdAuthenticationError   (401)
       ├── NetBirdValidationError       (400)
       ├── NetBirdNotFoundError         (404)
       ├── NetBirdRateLimitError        (429)
       └── NetBirdServerError           (5xx)

Base Exception
--------------

.. autoclass:: NetBirdAPIError
   :members:
   :show-inheritance:

   Base exception for all NetBird API errors.

   .. attribute:: message
      :type: str

      Human-readable error message.

   .. attribute:: status_code
      :type: int | None

      HTTP status code, if available.

   .. attribute:: response_data
      :type: dict

      Raw response data from the API.

Authentication Errors
---------------------

.. autoclass:: NetBirdAuthenticationError
   :members:
   :show-inheritance:

   Raised for **401 Unauthorized** responses.

   Common causes:

   - Invalid or expired API token
   - Missing Authorization header
   - Token lacks required permissions

Validation Errors
-----------------

.. autoclass:: NetBirdValidationError
   :members:
   :show-inheritance:

   Raised for **400 Bad Request** responses.

   Common causes:

   - Missing required parameters
   - Invalid parameter values
   - Malformed request body

Not Found Errors
----------------

.. autoclass:: NetBirdNotFoundError
   :members:
   :show-inheritance:

   Raised for **404 Not Found** responses.

   Common causes:

   - Resource ID does not exist
   - Resource has been deleted
   - Insufficient permissions to access resource

Rate Limit Errors
-----------------

.. autoclass:: NetBirdRateLimitError
   :members:
   :show-inheritance:

   Raised for **429 Too Many Requests** responses.

   .. attribute:: retry_after
      :type: int | None

      Number of seconds to wait before retrying.

Server Errors
-------------

.. autoclass:: NetBirdServerError
   :members:
   :show-inheritance:

   Raised for **5xx** server errors.

   Common causes:

   - Temporary server issues
   - Database connectivity problems
   - Internal service failures

Usage Example
-------------

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
       print("Check your API token")
   except NetBirdValidationError as e:
       print(f"Invalid request: {e.message}")
   except NetBirdRateLimitError as e:
       if e.retry_after:
           time.sleep(e.retry_after)
   except NetBirdServerError:
       print("Server error - try again later")
   except NetBirdAPIError as e:
       print(f"API error ({e.status_code}): {e.message}")
