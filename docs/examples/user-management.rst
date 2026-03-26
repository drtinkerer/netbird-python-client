User Management
===============

Examples for managing users, tokens, and authentication.

List All Users
--------------

.. code-block:: python

   users = client.users.list()
   for user in users:
       print(f"{user['name']:20s} {user['email']:30s} {user['role']}")

   # Filter service users
   service_users = [u for u in users if u.get('is_service_user')]
   print(f"\nService users: {len(service_users)}")

Get Current User
----------------

.. code-block:: python

   me = client.users.get_current()
   print(f"Name: {me['name']}")
   print(f"Email: {me['email']}")
   print(f"Role: {me['role']}")
   print(f"Status: {me['status']}")

Create Users
------------

.. code-block:: python

   from netbird.models import UserCreate

   # Create a regular user
   user = client.users.create(UserCreate(
       email="alice@company.com",
       name="Alice Smith",
       role="user",
       auto_groups=["default-group"]
   ))
   print(f"Created: {user['name']} ({user['id']})")

   # Create an admin user
   admin = client.users.create(UserCreate(
       email="admin@company.com",
       name="Admin User",
       role="admin",
   ))

   # Create a service user for automation
   bot = client.users.create(UserCreate(
       email="bot@company.com",
       name="CI/CD Bot",
       is_service_user=True,
       role="admin",
   ))

Update User Role
----------------

.. code-block:: python

   from netbird.models import UserUpdate

   updated = client.users.update("user-id", UserUpdate(
       role="admin"
   ))
   print(f"Updated {updated['name']} role to {updated['role']}")

Approve or Reject Users
------------------------

.. code-block:: python

   # List all users and find pending ones
   users = client.users.list()
   pending = [u for u in users if u.get('status') == 'invited']

   for user in pending:
       print(f"Pending: {user['name']} ({user['email']})")
       # Approve the user
       client.users.approve(user['id'])
       print(f"  Approved!")

   # Or reject a user
   # client.users.reject("user-id")

User Invites
------------

.. code-block:: python

   from netbird.models import UserInviteCreate

   # List pending invites
   invites = client.users.list_invites()
   for invite in invites:
       print(f"Invite: {invite['id']} - {invite.get('email', 'N/A')}")

   # Create a new invite
   invite = client.users.create_invite(UserInviteCreate(
       email="newuser@company.com",
       name="New User",
       role="user",
   ))
   print(f"Invite created: {invite['id']}")

   # Regenerate invite link
   new_invite = client.users.regenerate_invite("invite-id")

   # Delete an invite
   client.users.delete_invite("invite-id")

Token Management
----------------

.. code-block:: python

   from netbird.models import TokenCreate

   # List tokens for a user
   tokens = client.tokens.list(user_id="user-id")
   for token in tokens:
       print(f"{token['name']}: expires {token['expiration_date']}")

   # Create a new token
   new_token = client.tokens.create(
       user_id="user-id",
       data=TokenCreate(name="api-access", expires_in=30)  # 30 days
   )
   print(f"Token: {new_token['plain_token']}")
   # Save this token - it won't be shown again!

   # Delete a token
   client.tokens.delete(user_id="user-id", token_id="token-id")

Bulk User Operations
--------------------

.. code-block:: python

   from netbird.models import UserCreate

   # Bulk create users from a list
   team_members = [
       ("Alice", "alice@company.com"),
       ("Bob", "bob@company.com"),
       ("Charlie", "charlie@company.com"),
   ]

   created_users = []
   for name, email in team_members:
       user = client.users.create(UserCreate(
           email=email,
           name=name,
           role="user",
           auto_groups=["engineering"]
       ))
       created_users.append(user)
       print(f"Created: {user['name']}")

   print(f"\nCreated {len(created_users)} users")

Block/Unblock Users
-------------------

.. code-block:: python

   from netbird.models import UserUpdate

   # Block a user
   client.users.update("user-id", UserUpdate(is_blocked=True))
   print("User blocked")

   # Unblock a user
   client.users.update("user-id", UserUpdate(is_blocked=False))
   print("User unblocked")

Delete Users
------------

.. code-block:: python

   # Delete a specific user
   client.users.delete("user-id")
   print("User deleted")

   # Delete all service users (be careful!)
   users = client.users.list()
   for user in users:
       if user.get('is_service_user') and user['name'] == 'old-bot':
           client.users.delete(user['id'])
           print(f"Deleted service user: {user['name']}")
