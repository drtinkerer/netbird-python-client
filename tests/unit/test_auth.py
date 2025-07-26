"""
Unit tests for authentication modules.
"""

import pytest

from netbird.auth import TokenAuth


class TestTokenAuth:
    """Test cases for TokenAuth class."""
    
    def test_token_auth_initialization(self):
        """Test TokenAuth initialization."""
        auth = TokenAuth("test-token-123")
        assert auth.token == "test-token-123"
    
    def test_token_auth_empty_token_raises_error(self):
        """Test that empty token raises ValueError."""
        with pytest.raises(ValueError, match="Token cannot be empty"):
            TokenAuth("")
    
    def test_token_auth_whitespace_token_stripped(self):
        """Test that whitespace in token is stripped."""
        auth = TokenAuth("  test-token-123  ")
        assert auth.token == "test-token-123"
    
    def test_get_auth_headers(self):
        """Test getting authentication headers."""
        auth = TokenAuth("test-token-123")
        headers = auth.get_auth_headers()
        
        expected = {"Authorization": "Token test-token-123"}
        assert headers == expected
    
    def test_repr(self):
        """Test string representation."""
        auth = TokenAuth("test-token-123456789")
        repr_str = repr(auth)
        
        assert "TokenAuth" in repr_str
        assert "test-tok..." in repr_str  # Should be masked
        assert "123456789" not in repr_str  # Full token should not be visible
    
    def test_repr_short_token(self):
        """Test string representation with short token."""
        auth = TokenAuth("short")
        repr_str = repr(auth)
        
        assert "TokenAuth" in repr_str
        assert "***" in repr_str  # Short tokens should show ***


