#!/usr/bin/env python3
"""
Excalidraw Network Diagram - Creates a visual diagram using Excalidraw-Interface library.
"""

import os
import sys
import json
from Excalidraw_Interface import SketchBuilder

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
                    enriched_network['resources'] = []
            
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
                        }
                        enriched_routers.append(enriched_router)
                    
                    enriched_network['routers'] = enriched_routers
                except Exception as e:
                    print(f"Warning: Could not fetch routers for network {network['name']}: {e}")
                    enriched_network['routers'] = []
            
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


def create_excalidraw_diagram(networks):
    """Create a network diagram using Excalidraw-Interface."""
    
    sb = SketchBuilder()
    
    # Collect all unique source groups from all policies
    all_source_groups = set()
    for network in networks:
        policies = network.get('policies', [])
        for policy in policies:
            if isinstance(policy, dict):  # Policy object with full data
                rules = policy.get('rules', [])
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    for source in sources:
                        if isinstance(source, dict):
                            source_name = source.get('name', source.get('id', 'Unknown'))
                            all_source_groups.add(source_name)
                        else:
                            all_source_groups.add(str(source))
    
    # Create source group boxes at the top with better spacing
    source_group_elements = {}
    source_groups_list = sorted(all_source_groups)
    total_width = len(source_groups_list) * 220  # 200 width + 20 spacing
    source_x_start = 50
    source_y = 100
    source_spacing = 250  # Increased spacing
    
    for i, source_group in enumerate(source_groups_list):
        x = source_x_start + (i * source_spacing)
        # Create rectangle and text separately for better control
        rect = sb.Rectangle(
            x=x, 
            y=source_y, 
            width=200, 
            height=80, 
            backgroundColor="#FFE4E1", 
            strokeColor="#CD5C5C",
            strokeWidth=2
        )
        text = sb.Text(
            f"👥 {source_group}", 
            x=x, 
            y=source_y, 
            fontSize=16
        )
        source_group_elements[source_group] = rect  # Use rectangle for connections
    
    # Create network clusters with resources - much more spacing
    network_y_start = 400
    network_spacing = 400  # Increased spacing between networks
    resource_id_to_element = {}
    group_name_to_elements = {}  # Map group names to their elements for connections
    
    for network_idx, network in enumerate(networks):
        network_name = network['name']
        resources = network.get('resources', [])
        routers = network.get('routers', [])
        
        # Calculate network position with better spacing
        network_x = 100 + (network_idx * network_spacing)
        network_y = network_y_start
        
        # Create network header with larger size
        network_rect = sb.Rectangle(
            x=network_x,
            y=network_y,
            width=350,
            height=60,
            backgroundColor="#F0F8FF",
            strokeColor="#4169E1",
            strokeWidth=3
        )
        network_text = sb.Text(
            f"🌐 {network_name}",
            x=network_x,
            y=network_y,
            fontSize=18
        )
        
        # Create resources within the network with much more spacing
        resource_y_start = network_y + 100
        resource_spacing = 140  # Increased spacing between resources to account for group names
        
        for res_idx, resource in enumerate(resources):
            resource_name = resource.get('name', 'Unknown')
            resource_address = resource.get('address', 'N/A')
            resource_type = resource.get('type', 'unknown')
            resource_id = resource.get('id', None)
            resource_groups = resource.get('groups', [])
            
            # Choose icon based on resource type
            icon = "🖥️" if resource_type == 'host' else "🌐" if resource_type == 'subnet' else "📁"
            
            resource_y = resource_y_start + (res_idx * resource_spacing)
            
            # Make the resource box taller if there are groups
            box_height = 120 if resource_groups else 80
            
            resource_rect = sb.Rectangle(
                x=network_x + 30,
                y=resource_y,
                width=280,
                height=box_height,
                backgroundColor="#FFFACD",
                strokeColor="#DAA520",
                strokeWidth=2
            )
            resource_text = sb.Text(
                f"{icon} {resource_name}\n{resource_address}",
                x=network_x + 30,
                y=resource_y - 20,
                fontSize=14
            )
            
            # Add group names as separate elements inside the resource box
            if resource_groups:
                group_y_offset = 25
                for i, group in enumerate(resource_groups):
                    # Handle both string and dict groups
                    if isinstance(group, dict):
                        group_name = group.get('name', group.get('id', 'Unknown'))
                    else:
                        group_name = str(group)
                    
                    group_icon = sb.Text(
                        f"🏷️ {group_name}",
                        x=network_x + 30,
                        y=resource_y + group_y_offset + (i * 15),
                        fontSize=12
                    )
                    
                    # Store group elements for connections
                    if group_name not in group_name_to_elements:
                        group_name_to_elements[group_name] = []
                    group_name_to_elements[group_name].append(group_icon)
            
            resource_element = resource_rect
            
            if resource_id:
                resource_id_to_element[resource_id] = resource_element
        
        # Create routers within the network with proper spacing
        router_y_start = resource_y_start + (len(resources) * resource_spacing) + 50
        
        for router_idx, router in enumerate(routers):
            router_name = router.get('name', 'Unknown Router')
            router_y = router_y_start + (router_idx * resource_spacing)
            
            router_rect = sb.Rectangle(
                x=network_x + 30,
                y=router_y,
                width=280,
                height=80,
                backgroundColor="#FFFACD",
                strokeColor="#DAA520",
                strokeWidth=2
            )
            router_text = sb.Text(
                f"🔀 {router_name}",
                x=network_x + 30,
                y=router_y,
                fontSize=14
            )
    
    # Create connections from source groups to destination resources
    for network in networks:
        policies = network.get('policies', [])
        for policy in policies:
            if isinstance(policy, dict):  # Policy object with full data
                rules = policy.get('rules', [])
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    destinations = rule.get('destinations', []) or []
                    destination_resource = rule.get('destinationResource', {})
                    
                    # Get source group names
                    source_names = []
                    for source in sources:
                        if isinstance(source, dict):
                            source_name = source.get('name', source.get('id', 'Unknown'))
                            source_names.append(source_name)
                        else:
                            source_names.append(str(source))
                    
                    # Handle destinations field (group objects) - connect to group elements
                    if destinations:
                        for dest_group_obj in destinations:
                            if isinstance(dest_group_obj, dict):
                                dest_group_name = dest_group_obj.get('name', dest_group_obj.get('id', 'Unknown'))
                                if dest_group_name in group_name_to_elements:
                                    # Connect to all instances of this group name
                                    for group_element in group_name_to_elements[dest_group_name]:
                                        for source_name in source_names:
                                            if source_name in source_group_elements:
                                                sb.create_binding_arrows(
                                                    source_group_elements[source_name], 
                                                    group_element,
                                                    strokeColor="#00CC66",
                                                    strokeWidth=2
                                                )
                            elif isinstance(dest_group_obj, str) and dest_group_obj in group_name_to_elements:
                                # Handle string case as well
                                for group_element in group_name_to_elements[dest_group_obj]:
                                    for source_name in source_names:
                                        if source_name in source_group_elements:
                                            sb.create_binding_arrows(
                                                source_group_elements[source_name], 
                                                group_element,
                                                strokeColor="#00CC66",
                                                strokeWidth=2
                                            )
                    
                    # Also handle destinationResource field - connect to resources
                    if isinstance(destination_resource, dict):
                        dest_resource_id = destination_resource.get('id')
                        if dest_resource_id and dest_resource_id in resource_id_to_element:
                            dest_element = resource_id_to_element[dest_resource_id]
                            
                            # Create arrows from each source to this destination resource
                            for source_name in source_names:
                                if source_name in source_group_elements:
                                    sb.create_binding_arrows(
                                        source_group_elements[source_name], 
                                        dest_element,
                                        strokeColor="#0066CC",
                                        strokeWidth=3
                                    )
    
    # Export the diagram
    output_file = "netbird_networks_excalidraw.excalidraw"
    sb.export_to_file(output_file)
    print(f"✅ Excalidraw diagram saved as {output_file}")
    print(f"💡 You can open this file at https://excalidraw.com/ to view and edit the diagram")


def main():
    """Main function to create and display the network diagram."""
    print("🔄 Fetching network data from NetBird...")
    
    # Get enriched network data
    networks = get_enriched_networks()
    
    if not networks:
        print("❌ No networks found.")
        return
    
    print(f"✅ Found {len(networks)} networks. Creating Excalidraw diagram...")
    
    # Create the diagram
    create_excalidraw_diagram(networks)


if __name__ == "__main__":
    main()