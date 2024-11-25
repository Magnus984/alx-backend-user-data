#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union, NoReturn

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves user to the database
        """
        new_user = User(
            email=email, hashed_password=hashed_password
            )
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: dict) -> Union[User, NoReturn]:
        """Finds user from database
        """
        for key in kwargs.keys():
            if key == "email":
                row = self._session.query(User).filter(
                    User.email == kwargs.get(key)
                    ).first()
                if row is None:
                    raise NoResultFound
                return row
            elif key == "id":
                row = self._session.query(User).filter(
                    User.id == kwargs.get(key)
                    ).first()
                if row is None:
                    raise NoResultFound
                return row
            elif key == "session_id":
                row = self._session.query(User).filter(
                    User.session_id == kwargs.get(key)
                    ).first()
                if row is None:
                    raise NoResultFound
                return row
        raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """Updates user's attributes
        """
        user = self.find_user_by(id=user_id)
        if user:
            for key in kwargs.keys():
                if key == "hashed_password":
                    user.hashed_password = kwargs.get(key)
                    return None
            raise ValueError
