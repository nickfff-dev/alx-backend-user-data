#!/usr/bin/env python3
"""Auth module."""
from typing import List, TypeVar
from flask import request
import os

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
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths:
            return False
        else:
            for excluded_path in excluded_paths:
                if excluded_path.startswith(path):
                    return False
                if path.startswith(excluded_path):
                    return False
                if excluded_path[-1] == '*':
                    if path.startswith(excluded_path[:-1]):
                        return False
        return True

    def current_user(self, request=None) -> User:
        """Placeholder method to retrieve
        the current user from the request."""
        return None

    def authorization_header(self, request=None) -> str:
        """
        Extracts the Authorization header from the request.

        Parameters:
        - request: The request object.

        Returns:
        - The value of the Authorization header if it exists, otherwise None.
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def session_cookie(self, request=None) -> str:
        """
        Retrieve the session cookie value from a request.

        Parameters:
        - request: The request object.

        Returns:
        - The value of the session cookie if it exists, otherwise None.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
