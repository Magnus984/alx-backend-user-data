#!/usr/bin/env python3
"""
Module for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manage API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if path requires authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Gets authorization header field from request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets current user from request
        """
        return None
