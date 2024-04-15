#!/usr/bin/env python3
"""Auth module."""
from typing import List, TypeVar
from flask import request

# Define a type variable for the User type
User = TypeVar('User')


class Auth:
    """Template for all authentication systems."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Placeholder method to check if authentication is required for a
        given path."""
        # Return True if path is None
        if path is None:
            return True

        # Return True if excluded_paths is None or empty
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Normalize path by ensuring it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check if path is in excluded_paths
        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Placeholder method to retrieve the authorization header from the
        request."""
        return None

    def current_user(self, request=None) -> User:
        """Placeholder method to retrieve the current user from the request."""
        return None
