---
layout: page
title: Examples
description: Practical examples and common use cases for the NetBird Python client
---

# Examples

Practical examples and common use cases for the NetBird Python client.

## Getting Started Examples

### Basic Client Setup

```python
import os
from netbird import APIClient
from netbird.exceptions import NetBirdAPIError

# Initialize client with environment variables
client = APIClient(
    host=os.getenv("NETBIRD_HOST", "api.netbird.io"),
    api_token=os.getenv("NETBIRD_API_TOKEN")
)

# Test the connection
try:
    user = client.users.get_current()
    print(f"✅ Connected as: {user['name']} ({user['email']})")
except NetBirdAPIError as e:
    print(f"❌ Connection failed: {e}")
```

### Environment Configuration

Create a `.env` file for your project:

```bash
# .env
NETBIRD_HOST=api.netbird.io
NETBIRD_API_TOKEN=your-api-token-here
```

Load environment variables:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = APIClient(
    host=os.getenv("NETBIRD_HOST"),
    api_token=os.getenv("NETBIRD_API_TOKEN")
)
```

## User Management Examples

### List and Filter Users

```python
# Get all users
users = client.users.list()
print(f"Total users: {len(users)}")

# Filter users by role
admins = [user for user in users if user['role'] == 'admin']
regular_users = [user for user in users if user['role'] == 'user']

print(f"Admins: {len(admins)}")
print(f"Regular users: {len(regular_users)}")

# Find users by email domain
company_users = [
    user for user in users 
    if user.get('email', '').endswith('@yourcompany.com')
]
```

### Create and Manage Users

```python
from netbird.models import UserCreate, UserUpdate, UserRole

# Create a new user
user_data = UserCreate(
    email="new.user@company.com",
    name="New User",
    role=UserRole.USER,
    auto_groups=["default-group-id"]
)

try:
    new_user = client.users.create(user_data)
    print(f"Created user: {new_user['name']} (ID: {new_user['id']})")
    
    # Update user role to admin
    update_data = UserUpdate(role=UserRole.ADMIN)
    updated_user = client.users.update(new_user['id'], update_data)
    print(f"Updated role to: {updated_user['role']}")
    
    # Send invitation
    client.users.invite(new_user['id'])
    print("Invitation sent")
    
except NetBirdAPIError as e:
    print(f"Error managing user: {e}")
```

## Network Management Examples

### Peer Discovery and Monitoring

```python
# Get detailed peer information
peers = client.peers.list()

print("🖥️  Peer Status Report")
print("=" * 50)

online_peers = []
offline_peers = []

for peer in peers:
    status = "🟢 Online" if peer['connected'] else "🔴 Offline"
    
    print(f"{status} {peer['name']}")
    print(f"   IP: {peer['ip']}")
    print(f"   OS: {peer['os']}")
    print(f"   Version: {peer['version']}")
    
    if peer.get('city_name') and peer.get('country_code'):
        print(f"   Location: {peer['city_name']}, {peer['country_code']}")
    
    print(f"   Last Seen: {peer['last_seen']}")
    print()
    
    if peer['connected']:
        online_peers.append(peer)
    else:
        offline_peers.append(peer)

print(f"Summary: {len(online_peers)} online, {len(offline_peers)} offline")
```

### Group Management

```python
from netbird.models import GroupCreate, GroupUpdate

# Create groups for different teams
teams = ["engineering", "marketing", "sales", "support"]

created_groups = {}
for team in teams:
    group_data = GroupCreate(
        name=f"{team}-team",
        peers=[]  # Start empty, add peers later
    )
    
    try:
        group = client.groups.create(group_data)
        created_groups[team] = group
        print(f"✅ Created group: {group['name']}")
    except NetBirdAPIError as e:
        print(f"❌ Failed to create {team} group: {e}")

# Add peers to groups based on naming convention
peers = client.peers.list()
for peer in peers:
    peer_name = peer['name'].lower()
    
    # Auto-assign peers to groups based on hostname
    for team in teams:
        if team in peer_name:
            group_id = created_groups[team]['id']
            
            # Update group to include this peer
            current_group = client.groups.get(group_id)
            current_peers = [p['id'] for p in current_group.get('peers', [])]
            current_peers.append(peer['id'])
            
            update_data = GroupUpdate(peers=current_peers)
            client.groups.update(group_id, update_data)
            print(f"Added {peer['name']} to {team} team")
            break
```

## Security and Access Control

### Policy Management

```python
from netbird.models import PolicyCreate, PolicyRule

# Create a policy for SSH access
ssh_rule = PolicyRule(
    name="Allow SSH",
    action="accept",
    protocol="tcp",
    ports=["22"],
    sources=["admin-group-id"],
    destinations=["server-group-id"]
)

ssh_policy = PolicyCreate(
    name="Admin SSH Access",
    description="Allow administrators SSH access to servers",
    enabled=True,
    rules=[ssh_rule]
)

try:
    policy = client.policies.create(ssh_policy)
    print(f"Created SSH policy: {policy['name']}")
except NetBirdAPIError as e:
    print(f"Failed to create policy: {e}")

# Create a policy for web traffic
web_rule = PolicyRule(
    name="Allow HTTP/HTTPS",
    action="accept",
    protocol="tcp",
    ports=["80", "443"],
    sources=["all-users-group-id"],
    destinations=["web-servers-group-id"]
)

web_policy = PolicyCreate(
    name="Web Access",
    description="Allow all users to access web servers",
    enabled=True,
    rules=[web_rule]
)

policy = client.policies.create(web_policy)
print(f"Created web policy: {policy['name']}")
```

### Setup Key Management

```python
from netbird.models import SetupKeyCreate
import datetime

# Create setup keys for different purposes
setup_keys = []

# Temporary key for contractors
contractor_key = SetupKeyCreate(
    name="Contractor Access - Q1 2024",
    type="one-off",
    expires_in=30 * 24 * 3600,  # 30 days
    usage_limit=1,
    auto_groups=["contractor-group-id"]
)

# Permanent key for new employees
employee_key = SetupKeyCreate(
    name="New Employee Onboarding",
    type="reusable",
    expires_in=365 * 24 * 3600,  # 1 year
    usage_limit=50,
    auto_groups=["employee-group-id", "default-group-id"]
)

# Development environment key
dev_key = SetupKeyCreate(
    name="Development Environment",
    type="reusable",
    expires_in=90 * 24 * 3600,  # 90 days
    usage_limit=20,
    auto_groups=["developer-group-id"]
)

for key_data in [contractor_key, employee_key, dev_key]:
    try:
        key = client.setup_keys.create(key_data)
        setup_keys.append(key)
        print(f"✅ Created setup key: {key['name']}")
        print(f"   Key: {key['key']}")
        print(f"   Valid until: {key['expires']}")
        print()
    except NetBirdAPIError as e:
        print(f"❌ Failed to create key '{key_data.name}': {e}")
```

## Monitoring and Reporting

### Network Activity Report

```python
import json
from datetime import datetime, timedelta

def generate_network_report():
    """Generate a comprehensive network activity report."""
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {},
        "peers": {},
        "groups": {},
        "policies": {},
        "recent_activity": []
    }
    
    # Collect data
    users = client.users.list()
    peers = client.peers.list()
    groups = client.groups.list()
    policies = client.policies.list()
    events = client.events.get_audit_events()
    
    # Summary statistics
    report["summary"] = {
        "total_users": len(users),
        "total_peers": len(peers),
        "online_peers": len([p for p in peers if p['connected']]),
        "offline_peers": len([p for p in peers if not p['connected']]),
        "total_groups": len(groups),
        "active_policies": len([p for p in policies if p['enabled']]),
        "admin_users": len([u for u in users if u['role'] == 'admin'])
    }
    
    # Peer details
    for peer in peers:
        report["peers"][peer['id']] = {
            "name": peer['name'],
            "ip": peer['ip'],
            "connected": peer['connected'],
            "os": peer['os'],
            "version": peer['version'],
            "last_seen": peer['last_seen'],
            "location": f"{peer.get('city_name', '')}, {peer.get('country_code', '')}"
        }
    
    # Group membership
    for group in groups:
        report["groups"][group['id']] = {
            "name": group['name'],
            "peer_count": group['peers_count'],
            "resource_count": group.get('resources_count', 0)
        }
    
    # Policy status
    for policy in policies:
        report["policies"][policy['id']] = {
            "name": policy['name'],
            "enabled": policy['enabled'],
            "rule_count": len(policy.get('rules', []))
        }
    
    # Recent activity (last 24 hours)
    recent_events = [
        {
            "timestamp": event['timestamp'],
            "activity": event['activity'],
            "initiator": event.get('initiator_name', 'System')
        }
        for event in events[:50]  # Last 50 events
    ]
    report["recent_activity"] = recent_events
    
    return report

# Generate and save report
report = generate_network_report()

# Save to file
with open(f"netbird_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
    json.dump(report, f, indent=2)

# Print summary
print("📊 NetBird Network Report")
print("=" * 40)
print(f"Users: {report['summary']['total_users']} ({report['summary']['admin_users']} admins)")
print(f"Peers: {report['summary']['online_peers']} online, {report['summary']['offline_peers']} offline")
print(f"Groups: {report['summary']['total_groups']}")
print(f"Active Policies: {report['summary']['active_policies']}")
print(f"Recent Events: {len(report['recent_activity'])}")
```

## Advanced Usage Examples

### Bulk Operations

```python
# Bulk user creation from CSV
import csv

def bulk_create_users(csv_file):
    """Create users in bulk from a CSV file."""
    
    created_users = []
    errors = []
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            user_data = UserCreate(
                email=row['email'],
                name=row['name'],
                role=row.get('role', 'user'),
                auto_groups=row.get('groups', '').split(',') if row.get('groups') else []
            )
            
            try:
                user = client.users.create(user_data)
                created_users.append(user)
                print(f"✅ Created: {user['name']}")
                
                # Send invitation if requested
                if row.get('send_invite', '').lower() == 'true':
                    client.users.invite(user['id'])
                    print(f"   📧 Invitation sent to {user['email']}")
                    
            except NetBirdAPIError as e:
                error = f"Failed to create {row['name']}: {e}"
                errors.append(error)
                print(f"❌ {error}")
    
    print(f"\nSummary: {len(created_users)} created, {len(errors)} errors")
    return created_users, errors

# Example CSV format:
# name,email,role,groups,send_invite
# John Doe,john@company.com,user,engineering,true
# Jane Smith,jane@company.com,admin,"engineering,management",true
```

### Automated Cleanup

```python
from datetime import datetime, timedelta

def cleanup_inactive_resources():
    """Clean up inactive peers and expired setup keys."""
    
    # Clean up offline peers (offline for more than 30 days)
    cutoff_date = datetime.now() - timedelta(days=30)
    
    peers = client.peers.list()
    inactive_peers = []
    
    for peer in peers:
        if not peer['connected']:
            last_seen = datetime.fromisoformat(peer['last_seen'].replace('Z', '+00:00'))
            if last_seen < cutoff_date:
                inactive_peers.append(peer)
    
    print(f"Found {len(inactive_peers)} inactive peers")
    
    # Ask for confirmation before deletion
    if inactive_peers:
        response = input(f"Delete {len(inactive_peers)} inactive peers? (y/N): ")
        if response.lower() == 'y':
            for peer in inactive_peers:
                try:
                    client.peers.delete(peer['id'])
                    print(f"🗑️  Deleted inactive peer: {peer['name']}")
                except NetBirdAPIError as e:
                    print(f"❌ Failed to delete {peer['name']}: {e}")
    
    # Clean up expired setup keys
    setup_keys = client.setup_keys.list()
    expired_keys = [key for key in setup_keys if not key['valid']]
    
    print(f"Found {len(expired_keys)} expired setup keys")
    
    if expired_keys:
        response = input(f"Delete {len(expired_keys)} expired keys? (y/N): ")
        if response.lower() == 'y':
            for key in expired_keys:
                try:
                    client.setup_keys.delete(key['id'])
                    print(f"🗑️  Deleted expired key: {key['name']}")
                except NetBirdAPIError as e:
                    print(f"❌ Failed to delete {key['name']}: {e}")

# Run cleanup
cleanup_inactive_resources()
```

## Integration Examples

### Webhook Handler

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/netbird-webhook', methods=['POST'])
def handle_netbird_webhook():
    """Handle NetBird webhook events."""
    
    # Verify webhook signature (if configured)
    signature = request.headers.get('X-NetBird-Signature')
    if signature:
        webhook_secret = os.getenv('NETBIRD_WEBHOOK_SECRET')
        expected_signature = hmac.new(
            webhook_secret.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return jsonify({'error': 'Invalid signature'}), 401
    
    # Process webhook event
    event = request.json
    event_type = event.get('type')
    
    if event_type == 'peer.connected':
        peer_id = event['data']['peer_id']
        print(f"🟢 Peer connected: {peer_id}")
        
        # Auto-assign to appropriate group based on peer info
        peer = client.peers.get(peer_id)
        auto_assign_peer_to_group(peer)
        
    elif event_type == 'user.created':
        user_id = event['data']['user_id']
        print(f"👤 New user created: {user_id}")
        
        # Send welcome email or slack notification
        send_welcome_notification(user_id)
    
    return jsonify({'status': 'processed'})

def auto_assign_peer_to_group(peer):
    """Automatically assign peer to appropriate group."""
    hostname = peer['name'].lower()
    
    # Assign based on hostname patterns
    if 'server' in hostname:
        group_name = 'servers'
    elif 'laptop' in hostname or 'desktop' in hostname:
        group_name = 'workstations'
    elif 'mobile' in hostname:
        group_name = 'mobile-devices'
    else:
        group_name = 'default'
    
    # Find the group and add peer
    groups = client.groups.list()
    target_group = next((g for g in groups if g['name'] == group_name), None)
    
    if target_group:
        # Add peer to group (implementation depends on your group management strategy)
        print(f"Would assign {peer['name']} to {group_name} group")

if __name__ == '__main__':
    app.run(debug=True)
```

## Next Steps

- Check out the [API Reference](../api/) for detailed method documentation
- Learn about [error handling best practices](../guides/error-handling/)
- Explore [testing strategies](../guides/testing/)
- Read about [production deployment](../guides/deployment/)