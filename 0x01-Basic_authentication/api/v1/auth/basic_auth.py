#!/usr/bin/env python3
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User
import base64
import binascii
from typing import List, TypeVar


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        try:
            if base64_authorization_header is None:
                return None
            elif not isinstance(base64_authorization_header, str):
                return None
            utf8_encoded_string = base64_authorization_header.encode('utf-8')
            coded_string = base64.b64decode(utf8_encoded_string)
            return coded_string.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user, pwd = decoded_base64_authorization_header.split(':', 1)
        return user, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
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
        header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
            header)
        decoded_base64_authorization_header = self.decode_base64_authorization_header(
            base64_authorization_header)
        user_mail, user_pass = self.extract_user_credentials(
            decoded_base64_authorization_header)
        user_res = self.user_object_from_credentials(user_mail, user_pass)
        return user_res
