#!/usr/bin/env python3
"""Basic authentication module."""
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Parameters:
        - authorization_header: The Authorization header string.

        Returns:
        - The Base64 part of the Authorization
        header if it matches the expected format, otherwise None.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]
