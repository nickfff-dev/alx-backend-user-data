#!/usr/bin/env python3
"""Session authentication module."""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session for a user.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve the user ID for a given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if the session ID exists, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Retrieves the User instance for a request based on the session
        cookie.

        Parameters:
        - request: The request object.

        Returns:
        - The User instance if the session cookie is
        valid and corresponds to a user, otherwise None.
        """

        # Retrieve the session cookie value
        session_cookie_value = self.session_cookie(request)
        if session_cookie_value is None:
            return None

        # Retrieve the user ID for the session ID
        user_id = self.user_id_for_session_id(session_cookie_value)
        if user_id is None:
            return None

        # Retrieve the User instance from the database
        try:
            user = User.get(user_id)
            return user
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session / logout.

        Parameters:
        - request: The request object.

        Returns:
        - True if the session cookie is deleted, otherwise False.
        """
        if request is None:
            return False

        session_cookie_value = self.session_cookie(request)
        if session_cookie_value is None:
            return False

        user_id = self.user_id_for_session_id(session_cookie_value)
        if user_id is None:
            return False

        try:
            del self.user_id_by_session_id[session_cookie_value]
            return True
        except Exception:
            pass
