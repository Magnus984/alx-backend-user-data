#!/usr/bin/env python3
"""
Module for authentication
"""
from flask import request
from typing import List, TypeVar
import re
from os import getenv
cookie_name = getenv('SESSION_NAME', '_my_session_id')


class Auth:
    """
    Manage API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if path requires authentication
        """
        if path is not None and excluded_paths is not None:
            for excluded_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if excluded_path[-1] == '*':
                    pattern = '{}.*'.format(excluded_path[0:-1])
                elif excluded_path[-1] == '/':
                    pattern = '{}/*'.format(excluded_path[0:-1])
                else:
                    pattern = '{}/*'.format(excluded_path[0:-1])
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets authorization header field from request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets current user from request
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.
        """
        if request is None:
            return None
        cookie = request.cookies.get(cookie_name)
        return cookie
