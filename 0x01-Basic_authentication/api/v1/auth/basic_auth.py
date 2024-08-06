#!/usr/bin/env python3
"""
Basic Auth module
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """
    class BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
         returns the Base64 part of the Authorization
         header for a Basic Authentication
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic")):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64
        string base64_authorization_header
        """
        b64_auth_header = base64_authorization_header
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encode = b64_auth_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        decoded_64 = decoded_base64_authorization_header
        if (decoded_64 and isinstance(decoded_64, str) and
                ":" in decoded_64):
            res = decoded_64.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Validates the user credentials and returns the corresponding User
        object.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            TypeVar('User'): The User object if the credentials are valid,
            None otherwise.
        """
        if user_email and not isinstance(user_email, str):
            return None
        if user_pwd and not isinstance(user_pwd, str):
            return None
        if User.count() == 0:
            return None
        current_user = User.search({'email': user_email})

        if current_user is None or len(current_user) == 0:
            return None
        current_user = current_user[0]
        if current_user.is_valid_password(user_pwd):
            # print(f"{current_user.display_name()}+++++")
            return current_user
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64header)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_creds)
