"""
Test fixtures for NetBird Python Client tests.

This module provides utilities for loading test data from fixture files.
Industry standard approach for managing test data.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml


class FixtureLoader:
    """Utility class for loading test fixtures from files."""

    def __init__(self):
        self.fixtures_dir = Path(__file__).parent

    def load_json(self, filename: str) -> Union[Dict[str, Any], List[Any]]:
        """Load JSON fixture file.

        Args:
            filename: Path relative to fixtures directory (e.g., 'api_responses/user.json')

        Returns:
            Parsed JSON data
        """
        file_path = self.fixtures_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Fixture file not found: {filename}")

        with open(file_path, "r") as f:
            return json.load(f)

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML fixture file.

        Args:
            filename: Path relative to fixtures directory (e.g., 'mock_configs/netbird.yaml')

        Returns:
            Parsed YAML data
        """
        file_path = self.fixtures_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Fixture file not found: {filename}")

        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def load_text(self, filename: str) -> str:
        """Load text fixture file.

        Args:
            filename: Path relative to fixtures directory

        Returns:
            File contents as string
        """
        file_path = self.fixtures_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Fixture file not found: {filename}")

        with open(file_path, "r") as f:
            return f.read()


# Global fixture loader instance
fixtures = FixtureLoader()


# Convenience functions for common fixture types
def load_api_response(endpoint: str) -> Union[Dict[str, Any], List[Any]]:
    """Load API response fixture.

    Args:
        endpoint: API endpoint name (e.g., 'users', 'peers', 'groups')

    Returns:
        Mock API response data
    """
    return fixtures.load_json(f"api_responses/{endpoint}.json")


def load_sample_data(resource: str) -> Dict[str, Any]:
    """Load sample data fixture.

    Args:
        resource: Resource name (e.g., 'user', 'peer', 'group')

    Returns:
        Sample resource data
    """
    return fixtures.load_json(f"sample_data/{resource}.json")


def load_mock_config(config_name: str) -> Dict[str, Any]:
    """Load mock configuration fixture.

    Args:
        config_name: Configuration name (e.g., 'client', 'auth')

    Returns:
        Mock configuration data
    """
    return fixtures.load_yaml(f"mock_configs/{config_name}.yaml")
