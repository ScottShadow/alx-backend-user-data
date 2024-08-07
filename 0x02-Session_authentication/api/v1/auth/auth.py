#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """
    Class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if the given `path` is excluded from authentication based on
        the list of `excluded_paths`.

        Parameters:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication.

        Returns:
            bool: True if the `path` is not excluded from authentication,
            False otherwise.
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
            if excluded_path.startswith(path):
                return False
            if fnmatch.fnmatchcase(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the given request object.

        Args:
            request (Optional[flask.Request]): The Flask request object.
            Defaults to None.

        Returns:
            str: The authorization header value if it exists in the request
            headers, otherwise None.
        """
        if request is None:
            return None
        if request.headers.get('Authorization', None) is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the given request.

        Args:
            request (Optional[Request]): The request object. Defaults to None.

        Returns:
            TypeVar('User'): The current user object.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the given request object.

        Args:
            request (Optional[flask.Request]): The Flask request object.
            Defaults to None.

        Returns:
            str: The session cookie value if it exists in the request
            cookies,
            otherwise None.

        This function retrieves the session cookie value from the given
        request object.
        """
        _my_session_id = os.getenv('SESSION_NAME', 'session_id')
        cookie_value = None
        if request:
            cookie_value = request.cookies.get(_my_session_id)
            return cookie_value

        return None
