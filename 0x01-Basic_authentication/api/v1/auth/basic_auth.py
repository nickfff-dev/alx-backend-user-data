#!/usr/bin/env python3
"""Basic authentication module."""
from .auth import Auth
import base64
from typing import List, TypeVar, Union, Tuple
from models.user import User


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

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> Union[TypeVar('User'), None]:
        """
        Returns the User instance based on his email and password.

        Parameters:
        - user_email: The user's email.
        - user_pwd: The user's password.

        Returns:
        - The User instance if the email and password match, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({'email': user_email})
        if not users:
            return None

        # Check if the password is valid for the found user
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
