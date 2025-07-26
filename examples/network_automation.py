#!/usr/bin/env python3
"""
NetBird API Client - Network Automation Example

This example demonstrates:
- Creating and managing networks
- Setting up peer groups
- Configuring access policies
- Managing network routes
- DNS configuration
"""

import os
import sys
from typing import List

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError
from netbird.models import (
    GroupCreate,
    NetworkCreate,
    PolicyCreate,
    PolicyRule,
    RouteCreate,
    SetupKeyCreate,
)


def main():
    """Main network automation example."""
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
        print("=== NetBird Network Automation Example ===\\n")
        
        # 1. Create peer groups for different environments
        print("1. Creating peer groups...")
        
        groups_to_create = [
            {"name": "web-servers", "description": "Web server peers"},
            {"name": "database-servers", "description": "Database server peers"},
            {"name": "developers", "description": "Developer workstations"},
            {"name": "admins", "description": "System administrators"}
        ]
        
        created_groups = {}
        
        for group_info in groups_to_create:
            try:
                # First check if group exists
                existing_groups = client.groups.list()
                existing_group = next(
                    (g for g in existing_groups if g.name == group_info["name"]), 
                    None
                )
                
                if existing_group:
                    print(f"   ℹ️  Group '{group_info['name']}' already exists")
                    created_groups[group_info["name"]] = existing_group.id
                else:
                    group_data = GroupCreate(name=group_info["name"])
                    group = client.groups.create(group_data)
                    created_groups[group_info["name"]] = group.id
                    print(f"   ✅ Created group: {group.name}")
                    
            except NetBirdAPIError as e:
                print(f"   ❌ Failed to create group {group_info['name']}: {e}")
        
        # 2. Create a production network
        print("\\n2. Creating production network...")
        try:
            # Check if network exists
            existing_networks = client.networks.list()
            prod_network = next(
                (n for n in existing_networks if n.name == "Production Environment"), 
                None
            )
            
            if prod_network:
                print("   ℹ️  Production network already exists")
                network_id = prod_network.id
            else:
                network_data = NetworkCreate(
                    name="Production Environment",
                    description="Main production network for web and database servers"
                )
                network = client.networks.create(network_data)
                network_id = network.id
                print(f"   ✅ Created network: {network.name}")
                
        except NetBirdAPIError as e:
            print(f"   ❌ Failed to create network: {e}")
            network_id = None
        
        # 3. Create access policies
        print("\\n3. Creating access policies...")
        
        policies_to_create = [
            {
                "name": "Allow SSH Access",
                "description": "Allow administrators SSH access to servers",
                "rules": [
                    {
                        "name": "Admin SSH to Web Servers",
                        "action": "accept",
                        "protocol": "tcp",
                        "ports": ["22"],
                        "sources": ["admins"],
                        "destinations": ["web-servers"]
                    },
                    {
                        "name": "Admin SSH to DB Servers", 
                        "action": "accept",
                        "protocol": "tcp",
                        "ports": ["22"],
                        "sources": ["admins"],
                        "destinations": ["database-servers"]
                    }
                ]
            },
            {
                "name": "Web to Database Access",
                "description": "Allow web servers to connect to database servers",
                "rules": [
                    {
                        "name": "Web to MySQL",
                        "action": "accept",
                        "protocol": "tcp",
                        "ports": ["3306"],
                        "sources": ["web-servers"],
                        "destinations": ["database-servers"]
                    },
                    {
                        "name": "Web to PostgreSQL",
                        "action": "accept", 
                        "protocol": "tcp",
                        "ports": ["5432"],
                        "sources": ["web-servers"],
                        "destinations": ["database-servers"]
                    }
                ]
            },
            {
                "name": "Developer Access",
                "description": "Allow developers limited access to development resources",
                "rules": [
                    {
                        "name": "Dev HTTP Access",
                        "action": "accept",
                        "protocol": "tcp",
                        "ports": ["80", "443", "8080", "3000"],
                        "sources": ["developers"],
                        "destinations": ["web-servers"]
                    }
                ]
            }
        ]
        
        for policy_info in policies_to_create:
            try:
                # Check if policy exists
                existing_policies = client.policies.list()
                existing_policy = next(
                    (p for p in existing_policies if p.name == policy_info["name"]), 
                    None
                )
                
                if existing_policy:
                    print(f"   ℹ️  Policy '{policy_info['name']}' already exists")
                    continue
                
                # Create policy rules
                rules = []
                for rule_info in policy_info["rules"]:
                    # Map group names to IDs
                    source_ids = [created_groups.get(name, name) for name in rule_info["sources"]]
                    dest_ids = [created_groups.get(name, name) for name in rule_info["destinations"]]
                    
                    rule = PolicyRule(
                        name=rule_info["name"],
                        action=rule_info["action"],
                        protocol=rule_info["protocol"],
                        ports=rule_info["ports"],
                        sources=source_ids,
                        destinations=dest_ids
                    )
                    rules.append(rule)
                
                policy_data = PolicyCreate(
                    name=policy_info["name"],
                    description=policy_info["description"],
                    enabled=True,
                    rules=rules
                )
                
                policy = client.policies.create(policy_data)
                print(f"   ✅ Created policy: {policy.name} ({len(policy.rules)} rules)")
                
            except NetBirdAPIError as e:
                print(f"   ❌ Failed to create policy {policy_info['name']}: {e}")
        
        # 4. Create network routes
        print("\\n4. Creating network routes...")
        
        routes_to_create = [
            {
                "description": "Internal web network",
                "network_id": "10.1.0.0/24",
                "network_type": "ipv4",
                "metric": 100,
                "groups": ["web-servers"]
            },
            {
                "description": "Database network",
                "network_id": "10.2.0.0/24", 
                "network_type": "ipv4",
                "metric": 100,
                "groups": ["database-servers"]
            }
        ]
        
        for route_info in routes_to_create:
            try:
                # Check if similar route exists
                existing_routes = client.routes.list()
                existing_route = next(
                    (r for r in existing_routes if r.network == route_info["network_id"]), 
                    None
                )
                
                if existing_route:
                    print(f"   ℹ️  Route for {route_info['network_id']} already exists")
                    continue
                
                # Map group names to IDs
                group_ids = [created_groups.get(name, name) for name in route_info.get("groups", [])]
                
                route_data = RouteCreate(
                    description=route_info["description"],
                    network_id=route_info["network_id"],
                    network_type=route_info["network_type"],
                    metric=route_info["metric"],
                    enabled=True,
                    groups=group_ids
                )
                
                route = client.routes.create(route_data)
                print(f"   ✅ Created route: {route.network} (Metric: {route.metric})")
                
            except NetBirdAPIError as e:
                print(f"   ❌ Failed to create route {route_info['network_id']}: {e}")
        
        # 5. Create setup keys for different environments
        print("\\n5. Creating setup keys...")
        
        setup_keys_to_create = [
            {
                "name": "Web Server Setup Key",
                "type": "reusable",
                "expires_in": 86400 * 7,  # 7 days
                "usage_limit": 10,
                "auto_groups": ["web-servers"]
            },
            {
                "name": "Database Server Setup Key",
                "type": "reusable", 
                "expires_in": 86400 * 7,  # 7 days
                "usage_limit": 5,
                "auto_groups": ["database-servers"]
            },
            {
                "name": "Developer Workstation Key",
                "type": "reusable",
                "expires_in": 86400 * 30,  # 30 days
                "usage_limit": 50,
                "auto_groups": ["developers"]
            }
        ]
        
        for key_info in setup_keys_to_create:
            try:
                # Check if setup key exists
                existing_keys = client.setup_keys.list()
                existing_key = next(
                    (k for k in existing_keys if k.name == key_info["name"]), 
                    None
                )
                
                if existing_key:
                    print(f"   ℹ️  Setup key '{key_info['name']}' already exists")
                    continue
                
                # Map group names to IDs
                group_ids = [created_groups.get(name, name) for name in key_info["auto_groups"]]
                
                key_data = SetupKeyCreate(
                    name=key_info["name"],
                    type=key_info["type"],
                    expires_in=key_info["expires_in"],
                    usage_limit=key_info["usage_limit"],
                    auto_groups=group_ids
                )
                
                setup_key = client.setup_keys.create(key_data)
                print(f"   ✅ Created setup key: {setup_key.name}")
                print(f"      🔑 Key: {setup_key.key}")
                
            except NetBirdAPIError as e:
                print(f"   ❌ Failed to create setup key {key_info['name']}: {e}")
        
        # 6. Show network summary
        print("\\n6. Network configuration summary...")
        
        print("\\n   📊 Groups:")
        groups = client.groups.list()
        for group in groups:
            print(f"   📁 {group.name} - {group.peers_count} peers")
        
        print("\\n   🛡️  Policies:")
        policies = client.policies.list()
        for policy in policies:
            status = "✅ Enabled" if policy.enabled else "❌ Disabled"
            print(f"   🛡️  {policy.name} - {status} ({len(policy.rules)} rules)")
        
        print("\\n   🛣️  Routes:")
        routes = client.routes.list()
        for route in routes:
            status = "✅ Enabled" if route.enabled else "❌ Disabled"
            print(f"   🛣️  {route.network or 'N/A'} - {status}")
        
        print("\\n   🔑 Setup Keys:")
        setup_keys = client.setup_keys.list()
        for key in setup_keys:
            status = "✅ Valid" if key.valid and not key.revoked else "❌ Invalid"
            print(f"   🔑 {key.name} - {status} (Used: {key.used_times})")
        
        print("\\n✅ Network automation example completed successfully!")
        print("\\n🎉 Your NetBird network is now configured with:")
        print("   • Organized peer groups")
        print("   • Security policies for access control")
        print("   • Network routes for traffic management")
        print("   • Setup keys for easy peer onboarding")
        
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