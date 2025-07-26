"""
Base resource class for NetBird API resources.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from ..client import APIClient

T = TypeVar("T", bound=BaseModel)


class BaseResource:
    """Base class for all API resource handlers.
    
    Provides common functionality for CRUD operations and API interaction.
    """
    
    def __init__(self, client: "APIClient") -> None:
        self.client = client
    
    def _parse_response(self, data: Any, model_class: Type[T]) -> T:
        """Parse API response data into a Pydantic model."""
        if isinstance(data, dict):
            return model_class.model_validate(data)
        elif isinstance(data, list):
            return [model_class.model_validate(item) for item in data]
        else:
            return data
    
    def _parse_list_response(self, data: Any, model_class: Type[T]) -> List[T]:
        """Parse API response data into a list of Pydantic models."""
        if not isinstance(data, list):
            raise ValueError("Expected list response")
        return [model_class.model_validate(item) for item in data]