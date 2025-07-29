#!/usr/bin/env python3
"""
Mermaid Network Diagram - Creates a visual diagram using Mermaid syntax.
"""

import os
import sys
from pathlib import Path

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


def sanitize_id(name):
    """Sanitize node ID for Mermaid syntax."""
    return name.replace('-', '_').replace('.', '_').replace('/', '_').replace(' ', '_')


def create_mermaid_diagram(networks):
    """Create a network diagram using Mermaid syntax."""
    
    mermaid_lines = ["graph LR"]
    
    # Define colors for each source group
    source_group_colors = {
        'peers-am-network': '#FF6B6B',      # Red
        'staff-ad-developers': '#4ECDC4',   # Teal
        'staff-am-developers': '#45B7D1',   # Blue
        'staff-am-support': '#96CEB4',      # Green
        'staff-infrastructure': '#FECA57',  # Yellow
        'staff-platform': '#FF9FF3',       # Pink
    }
    
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
    
    # Create source group subgraph
    mermaid_lines.append("    subgraph SG[\"Source Groups\"]")
    for source_group in sorted(all_source_groups):
        safe_id = f"src_{sanitize_id(source_group)}"
        mermaid_lines.append(f"        {safe_id}[\"👥 {source_group}\"]")
    mermaid_lines.append("    end")
    
    # Create networks subgraphs
    resource_id_to_node = {}  # Map resource ID to node name for connections
    group_name_to_nodes = {}  # Map group names to their node names for connections
    
    for network_idx, network in enumerate(networks):
        network_name = network['name']
        safe_network_name = sanitize_id(network_name)
        resources = network.get('resources', [])
        routers = network.get('routers', [])
        
        # Create network subgraph
        mermaid_lines.append(f"    subgraph N{network_idx}[\"🌐 {network_name}\"]")
        
        # Add resources
        for res_idx, resource in enumerate(resources):
            resource_name = resource.get('name', 'Unknown')
            resource_address = resource.get('address', 'N/A')
            resource_type = resource.get('type', 'unknown')
            resource_id = resource.get('id', None)
            resource_groups = resource.get('groups', [])
            
            # Choose icon based on resource type
            icon = "🖥️" if resource_type == 'host' else "🌐" if resource_type == 'subnet' else "📁"
            
            # Create resource node
            resource_node_name = f'res_{network_idx}_{res_idx}'
            resource_label = f"{icon} {resource_name}<br/>{resource_address}"
            
            # Add group information to label
            if resource_groups:
                group_names = []
                for group in resource_groups:
                    if isinstance(group, dict):
                        group_name = group.get('name', group.get('id', 'Unknown'))
                        group_names.append(group_name)
                    else:
                        group_names.append(str(group))
                resource_label += f"<br/>🏷️ {', '.join(group_names)}"
                
                # Store group mappings for connections
                for group_name in group_names:
                    if group_name not in group_name_to_nodes:
                        group_name_to_nodes[group_name] = []
                    group_name_to_nodes[group_name].append(resource_node_name)
            
            mermaid_lines.append(f"        {resource_node_name}[\"{resource_label}\"]")
            
            # Map resource ID to node for connections
            if resource_id:
                resource_id_to_node[resource_id] = resource_node_name
        
        # Add routers
        for router_idx, router in enumerate(routers):
            router_name = router.get('name', 'Unknown Router')
            router_node_name = f'router_{network_idx}_{router_idx}'
            
            mermaid_lines.append(f"        {router_node_name}[\"🔀 {router_name}\"]")
        
        mermaid_lines.append("    end")
    
    # Create connections from source groups to destination resources/groups
    for network in networks:
        policies = network.get('policies', [])
        for policy in policies:
            if isinstance(policy, dict):  # Policy object with full data
                rules = policy.get('rules', [])
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    destinations = rule.get('destinations', []) or []
                    destination_resource = rule.get('destinationResource', {})
                    policy_name = policy.get('name', 'Policy')
                    
                    # Get source group names
                    source_names = []
                    for source in sources:
                        if isinstance(source, dict):
                            source_name = source.get('name', source.get('id', 'Unknown'))
                            source_names.append(source_name)
                        else:
                            source_names.append(str(source))
                    
                    # Handle destinations field (group objects) - connect to group resources
                    if destinations:
                        for dest_group_obj in destinations:
                            if isinstance(dest_group_obj, dict):
                                dest_group_name = dest_group_obj.get('name', dest_group_obj.get('id', 'Unknown'))
                                if dest_group_name in group_name_to_nodes:
                                    # Connect to all resources in this group
                                    for resource_node in group_name_to_nodes[dest_group_name]:
                                        for source_name in source_names:
                                            safe_source = f"src_{sanitize_id(source_name)}"
                                            # Use dashed line for group connections
                                            mermaid_lines.append(f"    {safe_source} -.->|\"Group: {policy_name}\"| {resource_node}")
                            elif isinstance(dest_group_obj, str) and dest_group_obj in group_name_to_nodes:
                                # Handle string case as well
                                for resource_node in group_name_to_nodes[dest_group_obj]:
                                    for source_name in source_names:
                                        safe_source = f"src_{sanitize_id(source_name)}"
                                        mermaid_lines.append(f"    {safe_source} -.->|\"Group: {policy_name}\"| {resource_node}")
                    
                    # Also handle destinationResource field - connect to specific resources
                    if isinstance(destination_resource, dict):
                        dest_resource_id = destination_resource.get('id')
                        if dest_resource_id and dest_resource_id in resource_id_to_node:
                            dest_node = resource_id_to_node[dest_resource_id]
                            
                            # Create connections from each source to this destination resource
                            for source_name in source_names:
                                safe_source = f"src_{sanitize_id(source_name)}"
                                # Use solid line for direct connections
                                mermaid_lines.append(f"    {safe_source} -->|\"Direct: {policy_name}\"| {dest_node}")
    
    # Add styling
    mermaid_lines.append("")
    mermaid_lines.append("    %% Styling")
    
    # Style source groups with their respective colors
    for source_group in sorted(all_source_groups):
        safe_id = f"src_{sanitize_id(source_group)}"
        color = source_group_colors.get(source_group, '#A8E6CF')
        mermaid_lines.append(f"    classDef {safe_id}_style fill:{color},stroke:#333,stroke-width:2px,color:#000")
        mermaid_lines.append(f"    class {safe_id} {safe_id}_style")
    
    # Style networks
    for network_idx, network in enumerate(networks):
        mermaid_lines.append(f"    classDef network{network_idx}_style fill:#E1F5FE,stroke:#0277BD,stroke-width:2px")
        resources = network.get('resources', [])
        routers = network.get('routers', [])
        
        # Apply style to all resources in this network
        for res_idx, resource in enumerate(resources):
            resource_node_name = f'res_{network_idx}_{res_idx}'
            mermaid_lines.append(f"    class {resource_node_name} network{network_idx}_style")
        
        # Apply style to all routers in this network
        for router_idx, router in enumerate(routers):
            router_node_name = f'router_{network_idx}_{router_idx}'
            mermaid_lines.append(f"    class {router_node_name} network{network_idx}_style")
    
    return "\n".join(mermaid_lines)


def main():
    """Main function to create and display the network diagram."""
    print("🔄 Fetching network data from NetBird...")
    
    # Get enriched network data
    networks = get_enriched_networks()
    
    if not networks:
        print("❌ No networks found.")
        return
    
    print(f"✅ Found {len(networks)} networks. Creating Mermaid diagram...")
    
    # Create the diagram
    mermaid_content = create_mermaid_diagram(networks)
    
    # Save as Mermaid file
    output_file = "netbird_networks_mermaid.mmd"
    
    with open(output_file, 'w') as f:
        f.write(mermaid_content)
    
    print(f"✅ Mermaid diagram saved as {output_file}")
    
    # Also save as markdown file for easy viewing
    markdown_file = "netbird_networks_mermaid.md"
    with open(markdown_file, 'w') as f:
        f.write("# NetBird Network Topology\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_content)
        f.write("\n```\n")
    
    print(f"✅ Markdown file with Mermaid diagram saved as {markdown_file}")
    print(f"💡 You can view this in GitHub, GitLab, or any Mermaid-compatible viewer")
    print(f"💡 Online viewer: https://mermaid.live/")


if __name__ == "__main__":
    main()