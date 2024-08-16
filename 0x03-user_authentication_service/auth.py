#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password using the bcrypt algorithm.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The hashed password as bytes.

        """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """
    Generates a random UUID.

    Returns:
        str: A random UUID as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """
        Initializes an instance of the Auth class.

        Sets the instance's _db attribute to an instance of the DB class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User, None]:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User

        """
        try:
            register_me = self._db.find_user_by(email=email)
            if register_me:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_password = _hash_password(password)
            register_me = self._db.add_user(
                email, hashed_password)
            return register_me

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials.

        Args:
            email (str): The email of the user to validate.
            password (str): The password of the user to validate.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user or user is None:
                return False
            if not bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password):
                # raise ValueError("Invalid email or password")
                return False
            return True
        except (NoResultFound, ValueError):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for a user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID if the user is found and the session is
            created successfully.
                 None if the user is not found.
        """
        try:
            session_id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def login_user(self, email: str, password: str) -> Union[str, None]:
        """
        Logs in a user with the given email and password.

        Args:
            email (str): The email of the user to log in.
            password (str): The password of the user to log in.

        Returns:
            str: The user object if the login is successful, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user or user is None:
                return None
            if not bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password):
                return None
            return user
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves a user object from the database based on a given session ID.

        Args:
            session_id (str): The ID of the session to retrieve the user from.

        Returns:
            User: The user object associated with the session ID,
            or None if no user is found.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user:
                return None
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user session by updating the user's session ID to None.

        Args:
            user_id (int): The ID of the user whose session is to be destroyed.

        Returns:
            None
        """
        if not user_id:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for a user with the given email.

        Args:
            email (str): The email of the user to generate a reset password
            token for.

        Returns:
            str: A reset password token if the user is found, otherwise raises
            a ValueError.

        Raises:
            ValueError: If the user is not found or an error occurs while
            generating the reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
            new_reset_token = _generate_uuid()
            if user is None:
                raise ValueError("Error user not found")
            self._db.update_user(user.id, reset_token=new_reset_token)
            return new_reset_token
        except Exception:
            raise ValueError("Error failed to generate reset token")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token used to identify the user.
            password (str): The new password to be updated.

        Returns:
            None

        Raises:
            ValueError: If the user is not found or an error occurs while
            updating the password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError("Error user not found")
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None,
                session_id=None)
        except Exception:
            raise ValueError("Error failed to update password")

        return None
