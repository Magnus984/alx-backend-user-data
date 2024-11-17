#!/usr/bin/env python3
"""Session authentication module"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Session authentication class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> User:
        """
        Returns a User instance based on a cookie.
        """
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Log User out.
        """
        if request is None:
            return False
        cookie_value = self.session_cookie(request)
        if cookie_value is None:
            return False
        if not self.user_id_for_session_id(cookie_value):
            return false
        if cookie_value in self.user_id_by_session_id:
            del self.user_id_by_session_id[cookie_value]
        return True
