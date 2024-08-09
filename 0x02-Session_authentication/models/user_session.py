#!/usr/bin/env python3
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """ UserSession model to store user sessions """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession instance with user_id and session_id """
        print("UserSession __init__ args: {}".format(args))
        print("UserSession __init__ kwargs: {}".format(kwargs))
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        print("UserSession __init__ self.user_id: {}".format(self.user_id))
        self.session_id = kwargs.get('session_id')
        print("UserSession __init__ self.session_id: {}".format(self.session_id))

    def save(self):
        """ Save the UserSession instance to the DATA dictionary """
        print("Saving UserSession instance...")
        print("UserSession instance has session_id: {}".format(self.session_id))
        if not hasattr(self, 'id'):
            print("Setting UserSession instance id to session_id...")
            self.id = self.session_id
        print("UserSession instance will be saved with id: {}".format(self.id))
        super().save()

    def remove(self):
        """ Remove the UserSession instance from the DATA dictionary """
        if hasattr(self, 'id'):
            del DATA[UserSession.__name__][self.id]
