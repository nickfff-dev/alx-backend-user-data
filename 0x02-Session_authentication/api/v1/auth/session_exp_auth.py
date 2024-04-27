#!/usr/bin/env python3
""" Session expiration authentication module.
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration."""

    def __init__(self):
        """Initialize the SessionExpAuth class."""
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Create a session for a user with expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID for a
        given session ID with expiration check."""
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id, None)
        if session_info is None:
            return None

        if self.session_duration <= 0:
            return session_info['user_id']

        created_at = session_info.get('created_at', None)
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None

        return session_info['user_id']
