#!/usr/bin/env python3
""" UserSession module"""
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """ UserSession model to store user sessions """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession instance with user_id and session_id """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def save(self):
        """ Save the UserSession instance to the DATA dictionary """
        if not hasattr(self, 'id'):
            self.id = self.session_id
        super().save()

    def remove(self):
        """ Remove the UserSession instance from the DATA dictionary """
        if hasattr(self, 'id'):
            del DATA[UserSession.__name__][self.id]
