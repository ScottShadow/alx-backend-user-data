#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
            if excluded_path.startswith(path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        if request is None:
            return None
        if request.headers.get('Authorization', None) is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        return None
