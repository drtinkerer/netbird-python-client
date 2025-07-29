#!/usr/bin/env python3
"""
Full Network Diagram - Creates a visual diagram showing all networks and their resources.
"""

import os
import sys
import json
from diagrams import Diagram, Cluster, Node
from diagrams.generic.network import Subnet
from diagrams.generic.compute import Rack
from diagrams.generic.blank import Blank

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError, NetBirdAuthenticationError

# Configuration
NETBIRD_HOST = os.getenv("NETBIRD_HOST", "api.netbird.io")
NETBIRD_TOKEN = os.getenv("NETBIRD_API_TOKEN")


def get_enriched_networks():
    """Get enriched network data from NetBird API."""
    if not NETBIRD_TOKEN:
        print("❌ Error: NETBIRD_API_TOKEN environment variable is required")
        sys.exit(1)

    # Initialize the NetBird client
    client = APIClient(
        host=NETBIRD_HOST,
        api_token=NETBIRD_TOKEN
    )

    try:
        # List all networks
        networks = client.networks.list()
        
        if not networks:
            return []
        
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
        
        return enriched_networks
        
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


def create_network_diagram(networks):
    """Create a visual diagram of all networks and their resources using diagrams library."""
    
    with Diagram("NetBird Network Topology", filename="netbird_networks", show=False, direction="TB", 
                 graph_attr={
                     "splines": "ortho", 
                     "nodesep": "2.5", 
                     "ranksep": "2.5",
                     "fontsize": "12",
                     "labelloc": "t",
                     "pad": "1.0"
                 }):
        
        for network in networks:
            network_name = network['name']
            resources = network.get('resources', [])
            
            with Cluster(f"{network_name}\n({len(resources)} resources)"):
                resource_nodes = []
                
                for i, resource in enumerate(resources):
                    resource_name = resource.get('name', 'Unknown')
                    resource_address = resource.get('address', 'N/A')
                    resource_type = resource.get('type', 'unknown')
                    resource_groups = resource.get('groups', [])
                    
                    # Don't truncate names - let them display fully
                    display_name = resource_name
                    display_address = resource_address
                    
                    # Format groups for display
                    if resource_groups:
                        groups_text = "Groups: " + ", ".join(resource_groups[:2])  # Show max 2 groups
                        if len(resource_groups) > 2:
                            groups_text += f" (+{len(resource_groups)-2} more)"
                    else:
                        groups_text = "No groups"
                    
                    # Create a yellowish box around each resource using a sub-cluster
                    with Cluster(f"{display_name}", 
                               graph_attr={
                                   "style": "filled,rounded", 
                                   "fillcolor": "#FFFFE0", 
                                   "pencolor": "#DAA520",
                                   "penwidth": "2",
                                   "margin": "30",
                                   "fontsize": "11",
                                   "labeljust": "c"
                               }):
                        # Create different icons based on resource type with address below
                        if resource_type == 'subnet':
                            main_node = Subnet(f"{display_address}")
                        else:  # host, domain, etc.
                            main_node = Rack(f"{display_address}")
                        
                        # Create small pink boxes for each group
                        group_nodes = []
                        for group in resource_groups[:3]:  # Show max 3 groups
                            with Cluster(f"{group}", 
                                       graph_attr={
                                           "style": "filled,rounded", 
                                           "fillcolor": "#FFB6C1", 
                                           "pencolor": "#FF69B4",
                                           "penwidth": "1",
                                           "margin": "8",
                                           "fontsize": "9",
                                           "labeljust": "c"
                                       }):
                                group_node = Blank("")
                                group_nodes.append(group_node)
                        
                        resource_nodes.append(main_node)


def main():
    """Main function to create and display the network diagram."""
    print("🔄 Fetching network data from NetBird...")
    
    # Get enriched network data
    networks = get_enriched_networks()
    
    if not networks:
        print("❌ No networks found.")
        return
    
    print(f"✅ Found {len(networks)} networks. Creating diagram...")
    
    # Create the diagram
    create_network_diagram(networks)
    
    print(f"✅ Diagram saved as netbird_networks.png")


if __name__ == "__main__":
    main()