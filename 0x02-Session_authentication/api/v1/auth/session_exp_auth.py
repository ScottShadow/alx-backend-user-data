#!/usr/bin/env python3
"""SessionExpAuth Module"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth Class"""

    def __init__(self):
        """Initialize the SessionExpAuth with session duration."""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID and store the session information."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_data = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Return the user ID if the session is still valid."""
        # Validate the session_id
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        # Retrieve the session information
        session_info = self.user_id_by_session_id.get(session_id)

        # Check if session_info is valid
        if session_info is None:
            return None

        # Get the session creation time
        session_created_at = session_info.get('created_at')

        # Validate the creation time
        if session_created_at is None:
            return None

        # Check if the session has expired
        if datetime.now() > session_created_at + timedelta(
                seconds=self.session_duration):
            # If the session is expired, delete it
            del self.user_id_by_session_id[session_id]
            return None

        # If the session is valid, return the user ID
        return session_info.get('user_id')
