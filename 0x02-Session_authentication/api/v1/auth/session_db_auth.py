#!/usr/bin/env python3
"""Session authentication with database storage module."""
import os
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with database storage."""

    def create_session(self, user_id=None):
        """Create a session for a user with expiration and store it in the
        database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        kwags = {
            'user_id': user_id,
            'session_id': session_id
        }
        user = UserSession(**kwags)
        user.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID for a given session ID from the database."""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        user_session = user_session[0]
        expiration_date = user_session.created_at + timedelta(
            seconds=self.session_duration)

        if expiration_date < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the user session based on the Session ID from the request
        cookie."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session = user_session[0]
            user_session.remove()
            UserSession.save_to_file()
            return True
        return False
