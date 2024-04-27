#!/usr/bin/env python3
"""UserSession model module."""
from models.base import Base


class UserSession(Base):
    """UserSession model to store session information."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a new UserSession instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
