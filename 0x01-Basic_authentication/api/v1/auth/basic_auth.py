#!/usr/bin/env python3
"""Basic authentication module."""
from .auth import Auth
import base64
from typing import List, TypeVar, Union, Tuple


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a Base64 encoded string and returns the decoded value as a
        UTF-8 string.

        Parameters:
        - base64_authorization_header: The Base64 encoded string.

        Returns:
        - The decoded value as a UTF-8 string if the input is valid,
        otherwise None.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts the user email and password from the Base64 decoded value.

        Parameters:
        - decoded_base64_authorization_header: The decoded Base64 string.

        Returns:
        - A tuple containing the user email and password if the input is valid,
        otherwise (None, None).
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password
