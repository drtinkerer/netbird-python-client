#!/usr/bin/env python3
"""
Full Network Diagram - Creates a visual diagram showing all networks and their resources.
"""

import os
import sys
import json
from diagrams import Diagram, Cluster, Node, Edge
from diagrams.generic.network import Subnet, Router
from diagrams.generic.compute import Rack
from diagrams.aws.general import Users
from diagrams.aws.security import IAMPermissions
from diagrams.generic.database import SQL

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
            
            # Replace resource IDs with actual resource data (keep IDs for mapping)
            if 'resources' in network and network['resources']:
                try:
                    detailed_resources = client.networks.list_resources(network['id'])
                    enriched_network['resources'] = detailed_resources
                    # Store original resources with IDs for policy mapping
                    enriched_network['_original_resources'] = detailed_resources
                except Exception as e:
                    print(f"Warning: Could not fetch resources for network {network['name']}: {e}")
                    enriched_network['resources'] = network['resources']  # Keep original IDs
                    enriched_network['_original_resources'] = []
            
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
    
    with Diagram("NetBird Network Topology", filename="netbird_networks", show=False, direction="LR", 
                 graph_attr={
                     "splines": "ortho", 
                     "nodesep": "1.5", 
                     "ranksep": "3.0",
                     "fontsize": "12",
                     "fontname": "Arial",
                     "bgcolor": "#FFFFFF",
                     "labelloc": "t",
                     "pad": "1.0",
                     "rankdir": "LR"
                 }):
        
        # Collect all unique source groups from all networks/policies
        all_source_groups = set()
        for network in networks:
            policies = network.get('policies', [])
            for policy in policies:
                rules = policy.get('rules', [])
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    all_source_groups.update(sources)
        
        # Collect all policies from all networks
        all_policies = []
        for network in networks:
            policies = network.get('policies', [])
            for policy in policies:
                policy['_network_name'] = network['name']  # Store network reference
                all_policies.append(policy)
        
        # Create source groups cluster on the left
        source_group_nodes = {}
        with Cluster("Source Groups", 
                   graph_attr={
                       "style": "filled,rounded", 
                       "fillcolor": "#F0F0FF", 
                       "pencolor": "#4169E1",
                       "penwidth": "2",
                       "margin": "20",
                       "fontsize": "12",
                       "labeljust": "c",
                       "rank": "source"
                   }):
            for source_group in sorted(all_source_groups):
                source_node = Users(f"{source_group}")
                source_group_nodes[source_group] = source_node
        
        # Create policies cluster in the middle
        policy_nodes = {}
        with Cluster("Policies", 
                   graph_attr={
                       "style": "filled,rounded", 
                       "fillcolor": "#F0FFF0", 
                       "pencolor": "#228B22",
                       "penwidth": "2",
                       "margin": "20",
                       "fontsize": "12",
                       "labeljust": "c",
                       "rank": "same"
                   }):
            for policy in all_policies:
                policy_name = policy.get('name', 'Unknown Policy')
                policy_enabled = policy.get('enabled', True)
                rules = policy.get('rules', [])
                network_name = policy.get('_network_name', 'Unknown')
                
                policy_info = f"{policy_name}\\n{len(rules)} rules\\nFor: {network_name}"
                policy_node = IAMPermissions(policy_info)
                policy_key = f"{network_name}_{policy_name}"
                policy_nodes[policy_key] = policy_node
        
        # Create networks as simple nodes in horizontal layout (no subclusters)
        network_nodes = {}
        network_list_nodes = []
        
        with Cluster("Networks", 
                   graph_attr={
                       "style": "filled,rounded", 
                       "fillcolor": "#F8F8FF", 
                       "pencolor": "#4169E1",
                       "penwidth": "2",
                       "margin": "20",
                       "fontsize": "12",
                       "labeljust": "c",
                       "rank": "same"
                   }):
            
            for network in networks:
                network_name = network['name']
                resources = network.get('resources', [])
                routers = network.get('routers', [])
                
                # Create single node per network with summary info
                resource_count = len(resources)
                router_count = len(routers)
                network_info = f"{network_name}\\n{resource_count} resources"
                if router_count > 0:
                    network_info += f"\\n{router_count} routers"
                
                network_node = Subnet(network_info)
                network_nodes[network_name] = network_node
                network_list_nodes.append(network_node)
        
        # Force networks to be on same rank (horizontal)
        if len(network_list_nodes) > 1:
            for i in range(len(network_list_nodes) - 1):
                network_list_nodes[i] >> Edge(style="invis", minlen="1") >> network_list_nodes[i + 1]
        
        # Create connections from source groups to policies to networks
        for policy in all_policies:
            policy_name = policy.get('name', 'Unknown Policy')
            network_name = policy.get('_network_name', 'Unknown')
            rules = policy.get('rules', [])
            policy_key = f"{network_name}_{policy_name}"
            
            if policy_key in policy_nodes:
                policy_node = policy_nodes[policy_key]
                
                # Connect sources to this policy
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    for source in sources:
                        if source in source_group_nodes:
                            source_group_nodes[source] >> Edge(color="blue", style="dashed") >> policy_node
                
                # Connect policy to its target network
                if network_name in network_nodes:
                    policy_node >> Edge(color="green", style="solid") >> network_nodes[network_name]


def main():
    """Main function to create and display the network diagram."""
    print("🔄 Fetching network data from NetBird...")
    
    # Get enriched network data
    networks = get_enriched_networks()
    print(networks)
    
    if not networks:
        print("❌ No networks found.")
        return
    
    print(f"✅ Found {len(networks)} networks. Creating diagram...")
    
    # Create the diagram
    create_network_diagram(networks)
    
    print(f"✅ Diagram saved as netbird_networks.png")


if __name__ == "__main__":
    main()