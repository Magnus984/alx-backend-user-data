#!/usr/bin/env python3
"""Module for hashing password.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes input password.
    """
    password_to_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_to_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Regsiters new user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password_hashed = _hash_password(password)
            new_user = self._db.add_user(email, password_hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if login is valid
        """
        try:
            user = self._db.find_user_by(email=email)
            password_to_byte = password.encode('utf-8')
            password_hashed = _hash_password(password)
            return bcrypt.checkpw(password_to_byte, password_hashed)
        except NoResultFound:
            return False

    def __generate_uuid(self) -> str:
        """Returns the string representation of a new UUID
        """
        return str(uuid.uuid4())
