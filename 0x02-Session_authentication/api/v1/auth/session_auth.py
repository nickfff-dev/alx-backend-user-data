#!/usr/bin/env python3
"""Session authentication module."""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for a user.

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
        """
        Retrieve the user ID for a given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if the session ID exists, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
