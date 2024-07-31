#!/usr/bin/env python3
"""
 Hashes a password using the bcrypt algorithm.
 Check if a given password matches a hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password as bytes.

    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a given password matches a hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
