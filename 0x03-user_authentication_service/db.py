#!/usr/bin/env python3
"""DB module
"""
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoResultFound

from user import Base

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id',
                'reset_token']


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

    def add_user(self, email: str, hashed_password: str) -> Union[User, None]:
        """Add a new user to the database
        """
        if not email or not hashed_password:
            return None
        newUser = User(email=email,
                       hashed_password=hashed_password)
        session = self._session
        session.add(newUser)
        session.commit()
        return newUser

    def find_user_by(self, **kwargs) -> User:
        """
        Retrieves a user from the database based on the provided keyword
        arguments.

        Args:
            **kwargs: Keyword arguments to filter the user by.

        Returns:
            User
        """
        if not kwargs or any(field not in VALID_FIELDS for field in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            resFound = session.query(User).filter_by(**kwargs).first()

            if not resFound:
                raise NoResultFound
            return resFound
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's information in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments to update the user's attributes.

        Raises:
            ValueError: If the user ID is invalid or if an invalid attribute is provided.

        Returns:
            None
        """
        updateMe = self.find_user_by(id=user_id)
        if not updateMe:
            raise ValueError
        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError
            setattr(updateMe, key, value)
        self._session.commit()
