#!/usr/bin/env python3
"""
Script to list all networks using NetBird API client.
"""

import json
import os
import sys
from typing import List, Dict, Any

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError, NetBirdAuthenticationError

# Configuration
NETBIRD_HOST = os.getenv("NETBIRD_HOST", "api.netbird.io")
NETBIRD_TOKEN = os.getenv("NETBIRD_API_TOKEN")


def main():
    """Main function to list all networks."""
    if not NETBIRD_TOKEN:
        print("❌ Error: NETBIRD_API_TOKEN environment variable is required")
        sys.exit(1)

    # Initialize the NetBird client
    client = APIClient(
        host=NETBIRD_HOST,
        api_token=NETBIRD_TOKEN
    )

    try:
        print("=== NetBird Networks ===\n")
        
        # List all networks
        networks: List[Dict[str, Any]] = client.networks.list()
        
        if not networks:
            print("No networks found.")
            return
        
        print(f"Found {len(networks)} network(s):\n")
        
        # Helper function to clean up the data structure
        def clean_data_structure(obj, parent_key=None):
            if isinstance(obj, dict):
                new_obj = {}
                for key, value in obj.items():
                    # Skip id fields except in destinationResource objects
                    if key == "id" and parent_key != "destinationResource":
                        continue
                    elif key == "destinationResource" and isinstance(value, dict):
                        # For destinationResource, keep id and type
                        new_obj[key] = {
                            "id": value.get("id", ""),
                            "type": value.get("type", "")
                        }
                    elif key == "groups" and isinstance(value, list):
                        # Replace group objects with just names
                        new_obj[key] = [group.get("name", group.get("id", "Unknown")) if isinstance(group, dict) else group for group in value]
                    elif key in ["sources", "destinations"] and isinstance(value, list):
                        # For sources and destinations, keep only name field
                        new_obj[key] = [item.get("name", "Unknown") if isinstance(item, dict) else item for item in value]
                    else:
                        new_obj[key] = clean_data_structure(value, key)
                return new_obj
            elif isinstance(obj, list):
                return [clean_data_structure(item, parent_key) for item in obj]
            else:
                return obj
        
        # Enrich networks with detailed resource and policy information
        enriched_networks = []
        
        for network in networks:
            enriched_network = network.copy()
            
            # Replace resource IDs with actual resource data
            if 'resources' in network and network['resources']:
                try:
                    detailed_resources = client.networks.list_resources(network['id'])
                    enriched_network['resources'] = detailed_resources
                except Exception as e:
                    print(f"Warning: Could not fetch resources for network {network['name']}: {e}")
                    enriched_network['resources'] = network['resources']  # Keep original IDs
            
            # Replace policy IDs with full policy objects
            if 'policies' in network and network['policies']:
                detailed_policies = []
                for policy_id in network['policies']:
                    try:
                        policy_data = client.policies.get(policy_id)
                        detailed_policies.append(policy_data)
                    except Exception as e:
                        print(f"Warning: Could not fetch policy {policy_id}: {e}")
                        detailed_policies.append({"id": policy_id, "error": str(e)})
                enriched_network['policies'] = detailed_policies
            else:
                enriched_network['policies'] = []
            
            # Replace router IDs with detailed router data
            if 'routers' in network and network['routers']:
                try:
                    detailed_routers = client.networks.list_routers(network['id'])
                    enriched_routers = []
                    
                    for i, router in enumerate(detailed_routers):
                        enriched_router = {
                            'name': f"{network['name']}-router-{i+1}",
                            'enabled': router.get('enabled', True),
                            'masquerade': router.get('masquerade', False),
                            'metric': router.get('metric', 9999),
                            'peer': router.get('peer', ''),
                            'peer_groups': []
                        }
                        
                        # Replace peer_groups IDs with group names
                        if router.get('peer_groups'):
                            for group_id in router['peer_groups']:
                                try:
                                    group_data = client.groups.get(group_id)
                                    enriched_router['peer_groups'].append(group_data.get('name', group_id))
                                except Exception as e:
                                    print(f"Warning: Could not fetch group {group_id}: {e}")
                                    enriched_router['peer_groups'].append(group_id)
                        
                        enriched_routers.append(enriched_router)
                    
                    enriched_network['routers'] = enriched_routers
                except Exception as e:
                    print(f"Warning: Could not fetch routers for network {network['name']}: {e}")
                    enriched_network['routers'] = []
            
            # Clean up the data structure (remove IDs, replace groups with names)
            enriched_network = clean_data_structure(enriched_network)
            
            enriched_networks.append(enriched_network)
        
        # Show complete JSON structure with enriched data
        print("=== Complete JSON Response (All Networks with Detailed Resources/Policies) ===")
        print(json.dumps(enriched_networks, indent=2, default=str))
            
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