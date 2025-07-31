"""
NetBird Network Map Generator

This module provides functionality to generate enriched network maps from NetBird API data.
It enriches networks with detailed resource and policy information for visualization purposes.
"""

from typing import List, Dict, Any, Optional
from .client import APIClient
from .exceptions import NetBirdAPIError, NetBirdAuthenticationError


def generate_full_network_map(
    client: APIClient,
    include_routers: bool = True,
    include_policies: bool = True,
    include_resources: bool = True
) -> List[Dict[str, Any]]:
    """
    Generate a comprehensive network map with enriched data from NetBird API.
    
    This function fetches all networks and enriches them with:
    - Detailed resource information (replacing resource IDs with full objects)
    - Complete policy data (replacing policy IDs with full policy objects)
    - Router information with enhanced metadata
    
    Args:
        client: Authenticated NetBird API client
        include_routers: Whether to include router information (default: True)
        include_policies: Whether to include policy information (default: True)
        include_resources: Whether to include resource information (default: True)
    
    Returns:
        List of enriched network dictionaries containing full object data
        instead of just IDs.
    
    Raises:
        NetBirdAuthenticationError: If authentication fails
        NetBirdAPIError: If API requests fail
        
    Example:
        >>> from netbird import APIClient
        >>> from netbird.network_map import generate_full_network_map
        >>> 
        >>> client = APIClient(host="api.netbird.io", api_token="your-token")
        >>> networks = generate_full_network_map(client)
        >>> 
        >>> # Access enriched data
        >>> for network in networks:
        ...     print(f"Network: {network['name']}")
        ...     for resource in network.get('resources', []):
        ...         print(f"  Resource: {resource['name']} - {resource['address']}")
        ...     for policy in network.get('policies', []):
        ...         print(f"  Policy: {policy['name']}")
    """
    try:
        # List all networks
        networks = client.networks.list()
        
        if not networks:
            return []
        
        # Enrich networks with detailed information
        enriched_networks = []
        
        for network in networks:
            enriched_network = network.copy()
            
            # Enrich with detailed resource information
            if include_resources and 'resources' in network and network['resources']:
                try:
                    detailed_resources = client.networks.list_resources(network['id'])
                    enriched_network['resources'] = detailed_resources
                except Exception as e:
                    print(f"Warning: Could not fetch resources for network {network['name']}: {e}")
                    enriched_network['resources'] = []
            elif not include_resources:
                enriched_network['resources'] = []
            
            # Enrich with full policy objects
            if include_policies and 'policies' in network and network['policies']:
                detailed_policies = []
                for policy_id in network['policies']:
                    try:
                        policy_data = client.policies.get(policy_id)
                        detailed_policies.append(policy_data)
                    except Exception as e:
                        print(f"Warning: Could not fetch policy {policy_id}: {e}")
                        detailed_policies.append({"id": policy_id, "error": str(e)})
                enriched_network['policies'] = detailed_policies
            elif not include_policies:
                enriched_network['policies'] = []
            else:
                enriched_network['policies'] = []
            
            # Enrich with detailed router information
            if include_routers and 'routers' in network and network['routers']:
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
                            'original_id': router.get('id', ''),
                        }
                        enriched_routers.append(enriched_router)
                    
                    enriched_network['routers'] = enriched_routers
                except Exception as e:
                    print(f"Warning: Could not fetch routers for network {network['name']}: {e}")
                    enriched_network['routers'] = []
            elif not include_routers:
                enriched_network['routers'] = []
            
            enriched_networks.append(enriched_network)
        
        return enriched_networks
        
    except NetBirdAuthenticationError:
        raise NetBirdAuthenticationError("Authentication failed. Please check your API token.")
    except NetBirdAPIError as e:
        raise NetBirdAPIError(f"API Error: {e.message}", status_code=e.status_code)
    except Exception as e:
        raise NetBirdAPIError(f"Unexpected error while generating network map: {e}")


def get_network_topology_data(
    client: APIClient,
    optimize_connections: bool = True
) -> Dict[str, Any]:
    """
    Generate network topology data optimized for visualization.
    
    This function creates a comprehensive data structure that includes:
    - All source groups from policies
    - Resource-to-group mappings
    - Connection mappings (both group-based and direct)
    - Optimized connection data to reduce visual clutter
    
    Args:
        client: Authenticated NetBird API client
        optimize_connections: Whether to optimize connections for visualization (default: True)
    
    Returns:
        Dictionary containing:
        - networks: List of enriched networks
        - all_source_groups: Set of all source group names
        - group_connections: Mapping of group-based connections
        - direct_connections: Mapping of direct resource connections  
        - resource_mappings: Resource ID to node mappings
        - group_mappings: Group name to resource node mappings
    
    Example:
        >>> topology = get_network_topology_data(client)
        >>> print(f"Found {len(topology['all_source_groups'])} source groups")
        >>> print(f"Found {len(topology['group_connections'])} group connections")
    """
    # Get enriched network data
    networks = generate_full_network_map(client)
    
    if optimize_connections:
        # Use the same optimization logic from the unified diagram
        return _collect_optimized_connections(networks)
    else:
        # Return raw data without optimization
        return {
            'networks': networks,
            'all_source_groups': set(),
            'group_connections': {},
            'direct_connections': {},
            'resource_mappings': {},
            'group_mappings': {}
        }


def _collect_optimized_connections(networks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Internal function to collect and optimize connections for visualization.
    
    This reduces visual clutter by merging duplicate connections and organizing
    them by source group and destination.
    """
    group_connections = {}  # {(source, dest_group): [policy_names]}
    direct_connections = {}  # {(source, dest_node): [policy_names]}
    all_source_groups = set()
    resource_id_to_node = {}
    group_name_to_nodes = {}
    
    # First pass: collect all source groups and build mappings
    for network_idx, network in enumerate(networks):
        resources = network.get('resources', [])
        
        # Build resource mappings
        for res_idx, resource in enumerate(resources):
            resource_id = resource.get('id', None)
            resource_groups = resource.get('groups', [])
            resource_node_name = f'res_{network_idx}_{res_idx}'
            
            # Map resource ID to node
            if resource_id:
                resource_id_to_node[resource_id] = resource_node_name
            
            # Map group names to nodes
            if resource_groups:
                for group in resource_groups:
                    if isinstance(group, dict):
                        group_name = group.get('name', group.get('id', 'Unknown'))
                    else:
                        group_name = str(group)
                    
                    if group_name not in group_name_to_nodes:
                        group_name_to_nodes[group_name] = []
                    group_name_to_nodes[group_name].append(resource_node_name)
        
        # Collect source groups from policies
        policies = network.get('policies', [])
        for policy in policies:
            if isinstance(policy, dict):
                rules = policy.get('rules', [])
                for rule in rules:
                    sources = rule.get('sources', []) or []
                    for source in sources:
                        if isinstance(source, dict):
                            source_name = source.get('name', source.get('id', 'Unknown'))
                            all_source_groups.add(source_name)
                        else:
                            all_source_groups.add(str(source))
    
    # Second pass: collect connections
    for network in networks:
        policies = network.get('policies', [])
        for policy in policies:
            if isinstance(policy, dict):
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
                    
                    # Collect group connections
                    if destinations:
                        for dest_group_obj in destinations:
                            if isinstance(dest_group_obj, dict):
                                dest_group_name = dest_group_obj.get('name', dest_group_obj.get('id', 'Unknown'))
                                if dest_group_name in group_name_to_nodes:
                                    for source_name in source_names:
                                        key = (source_name, dest_group_name)
                                        if key not in group_connections:
                                            group_connections[key] = []
                                        group_connections[key].append(policy_name)
                            elif isinstance(dest_group_obj, str) and dest_group_obj in group_name_to_nodes:
                                for source_name in source_names:
                                    key = (source_name, dest_group_obj)
                                    if key not in group_connections:
                                        group_connections[key] = []
                                    group_connections[key].append(policy_name)
                    
                    # Collect direct connections
                    if isinstance(destination_resource, dict):
                        dest_resource_id = destination_resource.get('id')
                        if dest_resource_id and dest_resource_id in resource_id_to_node:
                            dest_node = resource_id_to_node[dest_resource_id]
                            for source_name in source_names:
                                key = (source_name, dest_node)
                                if key not in direct_connections:
                                    direct_connections[key] = []
                                direct_connections[key].append(policy_name)
    
    return {
        'networks': networks,
        'group_connections': group_connections,
        'direct_connections': direct_connections,
        'all_source_groups': all_source_groups,
        'resource_id_to_node': resource_id_to_node,
        'group_name_to_nodes': group_name_to_nodes
    }