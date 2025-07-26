#!/usr/bin/env python3
"""
NetBird API Client - Basic Usage Example

This example demonstrates:
- Client initialization
- Basic CRUD operations
- Error handling
- Working with different resources
"""

import os
import sys
from typing import List

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError, NetBirdAuthenticationError
from netbird.models import User, Peer, Group


def main():
    """Main example function."""
    # Get API token from environment variable
    api_token = os.getenv("NETBIRD_API_TOKEN")
    if not api_token:
        print("Please set NETBIRD_API_TOKEN environment variable")
        sys.exit(1)
    
    # Initialize the client
    # For self-hosted: use your own host and port
    client = APIClient(
        host="api.netbird.io",  # or "your-netbird-host.com:33073"
        api_token=api_token
    )
    
    try:
        print("=== NetBird Python Client - Basic Usage ===\\n")
        
        # Get current user information
        print("1. Getting current user...")
        current_user = client.users.get_current()
        print(f"   Logged in as: {current_user.name} ({current_user.email})")
        print(f"   Role: {current_user.role}")
        print()
        
        # List all users
        print("2. Listing all users...")
        users: List[User] = client.users.list()
        print(f"   Found {len(users)} users:")
        for user in users[:5]:  # Show first 5 users
            status_emoji = "✅" if user.status == "active" else "❌"
            print(f"   {status_emoji} {user.name} ({user.email}) - {user.role}")
        if len(users) > 5:
            print(f"   ... and {len(users) - 5} more")
        print()
        
        # List all peers
        print("3. Listing all peers...")
        peers: List[Peer] = client.peers.list()
        print(f"   Found {len(peers)} peers:")
        for peer in peers[:5]:  # Show first 5 peers
            status_emoji = "🟢" if peer.connected else "🔴"
            print(f"   {status_emoji} {peer.name} ({peer.ip}) - {peer.os or 'Unknown OS'}")
        if len(peers) > 5:
            print(f"   ... and {len(peers) - 5} more")
        print()
        
        # List all groups
        print("4. Listing all groups...")
        groups: List[Group] = client.groups.list()
        print(f"   Found {len(groups)} groups:")
        for group in groups:
            print(f"   📁 {group.name} - {group.peers_count} peers")
        print()
        
        # List account information
        print("5. Getting account information...")
        accounts = client.accounts.list()
        if accounts:
            account = accounts[0]  # Usually just one account
            print(f"   Account ID: {account.id}")
            print(f"   Domain: {account.domain}")
        print()
        
        # List setup keys
        print("6. Listing setup keys...")
        setup_keys = client.setup_keys.list()
        print(f"   Found {len(setup_keys)} setup keys:")
        for key in setup_keys[:3]:  # Show first 3 keys
            status = "✅ Valid" if key.valid and not key.revoked else "❌ Invalid"
            print(f"   🔑 {key.name} - {status} (Used {key.used_times} times)")
        print()
        
        # List policies
        print("7. Listing access policies...")
        policies = client.policies.list()
        print(f"   Found {len(policies)} policies:")
        for policy in policies[:3]:  # Show first 3 policies  
            status = "✅ Enabled" if policy.enabled else "❌ Disabled"
            print(f"   🛡️  {policy.name} - {status} ({len(policy.rules)} rules)")
        print()
        
        # List routes
        print("8. Listing network routes...")
        routes = client.routes.list()
        print(f"   Found {len(routes)} routes:")
        for route in routes[:3]:  # Show first 3 routes
            status = "✅ Enabled" if route.enabled else "❌ Disabled"
            network = route.network or "N/A"
            print(f"   🛣️  {network} - {status} (Metric: {route.metric})")
        print()
        
        print("✅ Basic usage example completed successfully!")
        
    except NetBirdAuthenticationError:
        print("❌ Authentication failed. Please check your API token.")
        sys.exit(1)
    except NetBirdAPIError as e:
        print(f"❌ API Error: {e.message}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Clean up the client
        client.close()


if __name__ == "__main__":
    main()