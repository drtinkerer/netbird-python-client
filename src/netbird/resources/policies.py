"""
Policies resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models import PolicyCreate, PolicyUpdate
from .base import BaseResource


class PoliciesResource(BaseResource):
    """Handler for NetBird policies API endpoints.

    Provides methods to manage NetBird access control policies including
    listing, creating, retrieving, updating, and deleting policies.
    """

    def list(self) -> List[Dict[str, Any]]:
        """List all policies.

        Returns:
            List of policy dictionaries

        Example:
            >>> policies = client.policies.list()
            >>> for policy in policies:
            ...     print(f"Policy: {policy['name']} (Enabled: {policy['enabled']})")
        """
        data = self.client.get("policies")
        return self._parse_list_response(data)

    def create(self, policy_data: PolicyCreate) -> Dict[str, Any]:
        """Create a new policy.

        Args:
            policy_data: Policy creation data

        Returns:
            Created policy dictionary

        Example:
            >>> from netbird.models import PolicyRule, PolicyCreate
            >>> rule = PolicyRule(
            ...     name="Allow SSH",
            ...     action="accept",
            ...     protocol="tcp",
            ...     ports=["22"],
            ...     sources=["group-dev"],
            ...     destinations=["group-servers"]
            ... )
            >>> policy_data = PolicyCreate(
            ...     name="Development Access",
            ...     description="Allow developers to access servers",
            ...     rules=[rule]
            ... )
            >>> policy = client.policies.create(policy_data)
        """
        data = self.client.post(
            "policies", data=policy_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def get(self, policy_id: str) -> Dict[str, Any]:
        """Retrieve a specific policy.

        Args:
            policy_id: Unique policy identifier

        Returns:
            Policy dictionary

        Example:
            >>> policy = client.policies.get("policy-123")
            >>> print(f"Policy: {policy['name']}")
        """
        data = self.client.get(f"policies/{policy_id}")
        return self._parse_response(data)

    def update(self, policy_id: str, policy_data: PolicyUpdate) -> Dict[str, Any]:
        """Update a policy.

        Args:
            policy_id: Unique policy identifier
            policy_data: Policy update data

        Returns:
            Updated policy dictionary

        Example:
            >>> policy_data = PolicyUpdate(
            ...     enabled=False,
            ...     description="Disabled for maintenance"
            ... )
            >>> policy = client.policies.update("policy-123", policy_data)
        """
        data = self.client.put(
            f"policies/{policy_id}", data=policy_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def delete(self, policy_id: str) -> None:
        """Delete a policy.

        Args:
            policy_id: Unique policy identifier

        Example:
            >>> client.policies.delete("policy-123")
        """
        self.client.delete(f"policies/{policy_id}")
