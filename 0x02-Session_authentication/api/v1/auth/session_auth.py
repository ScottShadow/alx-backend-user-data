#!/usr/bin/env python3
""""
Session Authentication Module
"""

from api.v1.auth.auth import Auth
import uuid
from models.base import Base
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication class
    """
    user_id_by_session_id = {}
    # user_id_by_session_id = {"SessionID": "UserID"}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        A function that creates a session ID for a given user ID.

        Parameters:
            user_id (str): The user ID for which the session ID is created.
            Defaults to None.

        Returns:
            str: The generated session ID.
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with the given session ID.

        Parameters:
            session_id (str, optional): The session ID for which to
            retrieve the user ID. Defaults to None.

        Returns:
            str: The user ID associated with the session ID, or None if
            the session ID is not found or not a string.
        """
        user_id = None
        if session_id and isinstance(session_id, str):
            user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session ID stored in
        the request cookies.

        Parameters:
            request (Request, optional): The request object containing
            the cookies. Defaults to None.

        Returns:
            User
        """
        current_user_id = None
        current_user = None
        session_id = request.cookies.get("_my_session_id")
        current_user_id = self.user_id_for_session_id(session_id)
        if current_user_id:
            current_user = User.search({"id": current_user_id})[0]
        return current_user

    def destroy_session(self, request=None):
        """
        Destroys a session for the given request.

        Args:
            request (Request, optional): The request object. Defaults
            to None.

        Returns:
            bool: True if the session was successfully destroyed, False
            otherwise.
        """

        if request and self.session_cookie(request) is not None:
            user_cookie = self.session_cookie(request)
            user_id = self.user_id_for_session_id(user_cookie)
            if user_id:
                del self.user_id_by_session_id[user_cookie]
                return True

        return False
