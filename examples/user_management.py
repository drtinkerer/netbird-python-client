#!/usr/bin/env python3
"""
NetBird API Client - User Management Example

This example demonstrates:
- Creating and managing users
- Working with user roles and permissions
- Managing user tokens
- Handling user invitations
"""

import os
import sys
from datetime import datetime, timedelta

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError, NetBirdNotFoundError
from netbird.models import UserCreate, UserUpdate, UserRole, TokenCreate


def main():
    """Main user management example."""
    # Get API token from environment variable
    api_token = os.getenv("NETBIRD_API_TOKEN")
    if not api_token:
        print("Please set NETBIRD_API_TOKEN environment variable")
        sys.exit(1)
    
    client = APIClient(
        host="api.netbird.io",
        api_token=api_token
    )
    
    try:
        print("=== NetBird User Management Example ===\\n")
        
        # 1. Create a new service user
        print("1. Creating a new service user...")
        user_data = UserCreate(
            email="api-service@example.com",
            name="API Service Account", 
            role=UserRole.USER,
            is_service_user=True,
            auto_groups=[]  # Add group IDs if needed
        )
        
        try:
            new_user = client.users.create(user_data)
            print(f"   ✅ Created user: {new_user.name} (ID: {new_user.id})")
            service_user_id = new_user.id
        except NetBirdAPIError as e:
            if "already exists" in str(e):
                print("   ℹ️  Service user already exists, finding existing user...")
                users = client.users.list()
                service_user = next(
                    (u for u in users if u.email == "api-service@example.com"), 
                    None
                )
                if service_user:
                    service_user_id = service_user.id
                    print(f"   ✅ Found existing user: {service_user.name}")
                else:
                    raise e
            else:
                raise e
        
        # 2. Create an API token for the service user
        print("\\n2. Creating API token for service user...")
        token_data = TokenCreate(
            name="Automation Token",
            expires_in=30  # 30 days
        )
        
        try:
            token = client.tokens.create(service_user_id, token_data)
            print(f"   ✅ Created token: {token.name}")
            print(f"   🔑 Token ID: {token.id}")
            print(f"   📅 Expires: {token.expiration_date}")
        except NetBirdAPIError as e:
            print(f"   ❌ Failed to create token: {e}")
        
        # 3. List all tokens for the service user
        print("\\n3. Listing tokens for service user...")
        try:
            tokens = client.tokens.list(service_user_id)
            print(f"   Found {len(tokens)} tokens:")
            for token in tokens:
                status = "🟢 Active" if token.expiration_date > datetime.now() else "🔴 Expired"
                last_used = token.last_used.strftime("%Y-%m-%d") if token.last_used else "Never"
                print(f"   🔑 {token.name} - {status} (Last used: {last_used})")
        except NetBirdAPIError as e:
            print(f"   ❌ Failed to list tokens: {e}")
        
        # 4. Update user information
        print("\\n4. Updating user information...")
        try:
            update_data = UserUpdate(
                name="Updated API Service Account",
                # Note: You might want to add auto_groups or change other properties
            )
            updated_user = client.users.update(service_user_id, update_data)
            print(f"   ✅ Updated user name to: {updated_user.name}")
        except NetBirdAPIError as e:
            print(f"   ❌ Failed to update user: {e}")
        
        # 5. List all users with their roles
        print("\\n5. Listing all users with roles...")
        users = client.users.list()
        
        # Group users by role
        users_by_role = {}
        for user in users:
            role = user.role
            if role not in users_by_role:
                users_by_role[role] = []
            users_by_role[role].append(user)
        
        for role, role_users in users_by_role.items():
            print(f"\\n   {role.upper()} users ({len(role_users)}):")
            for user in role_users[:5]:  # Show first 5 users per role
                status_emoji = "✅" if user.status == "active" else "❌"
                user_type = "🤖 Service" if user.is_service_user else "👤 Regular"
                print(f"   {status_emoji} {user_type} {user.name} ({user.email})")
            
            if len(role_users) > 5:
                print(f"   ... and {len(role_users) - 5} more {role} users")
        
        # 6. Demonstrate user invitation (for regular users)
        print("\\n6. Managing user invitations...")
        
        # Find users with "invited" status
        invited_users = [u for u in users if u.status == "invited"]
        
        if invited_users:
            print(f"   Found {len(invited_users)} users with pending invitations:")
            for user in invited_users[:3]:  # Show first 3
                print(f"   📧 {user.name} ({user.email})")
                
                # Optionally resend invitation
                try:
                    client.users.invite(user.id)
                    print(f"      ✅ Resent invitation to {user.email}")
                except NetBirdAPIError as e:
                    print(f"      ❌ Failed to resend invitation: {e}")
        else:
            print("   ℹ️  No pending invitations found")
        
        # 7. Get current user permissions
        print("\\n7. Checking current user permissions...")
        try:
            current_user = client.users.get_current()
            print(f"   Current user: {current_user.name} ({current_user.role})")
            if current_user.permissions:
                print("   Permissions:")
                for perm, value in current_user.permissions.items():
                    status = "✅" if value else "❌"
                    print(f"   {status} {perm}")
            else:
                print("   ℹ️  No specific permissions data available")
        except NetBirdAPIError as e:
            print(f"   ❌ Failed to get current user: {e}")
        
        print("\\n✅ User management example completed successfully!")
        
        # Cleanup note
        print("\\n📝 Note: Created service user and tokens are left for your review.")
        print("   You may want to delete them manually if they're not needed.")
        
    except NetBirdAPIError as e:
        print(f"❌ API Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    main()