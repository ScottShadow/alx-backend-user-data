#!/usr/bin/env python3
"""
SessionDBAuth class that uses UserSession for session management
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class that uses UserSession for session management """

    def __init__(self) -> None:
        """ Initialize SessionDBAuth with session_duration from
        the environment """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session ID and store it in UserSession """
        if not user_id or not isinstance(user_id, str):
            return None

        # Create session ID using the parent method
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_data = {
            'user_id': user_id,
            'session_id': session_id,
            'created_at': datetime.now().strftime(TIMESTAMP_FORMAT)
        }
        # Create a new UserSession and save it
        user_session = UserSession(**session_data)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve user ID based on session ID from UserSession """
        if not session_id:
            return None
        try:
            # Search for the UserSession based on session_id
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not user_session:
            return None

        user_session = user_session[0]

        # Check session expiration if applicable
        if self.session_duration > 0:
            if (datetime.now() - user_session.created_at)\
                    .total_seconds() > self.session_duration:
                return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy session by removing UserSession entry """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Find and remove the UserSession
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True

        return False
