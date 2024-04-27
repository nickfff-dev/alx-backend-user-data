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

        return authorization_header.split(" ")[-1]

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
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[1 + len(email):]
        return (email, password)

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
        if user_email is None or user_pwd is None:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        if len(users) == 0:
            return None

        # Check if the password is valid for the found user
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance for a request.

        Parameters:
        - request: The request object.

        Returns:
        - The User instance if the request is authenticated, otherwise None.
        """
        if request is None:
            return None

        # Extract the Authorization header
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        # Extract the Base64 part of the Authorization header
        base64_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_header is None:
            return None

        # Decode the Base64 encoded string
        decoded_base64_header = \
            self.decode_base64_authorization_header(base64_header)
        if decoded_base64_header is None:
            return None

        # Extract the user credentials
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the User instance from the database
        return self.user_object_from_credentials(user_email, user_pwd)
