#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User

my_db = DB()
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print("________")
user_1.id
print("________+")

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print("________")
user_2.id
print("________+")
session = my_db._session
for instance in session.query(User).order_by(User.id):
    print(instance.id, instance.email)
