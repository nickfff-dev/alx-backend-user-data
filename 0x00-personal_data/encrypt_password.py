#!/usr/bin/env python3
"""Module that provides a function to hash passwords securely using bcrypt."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password for storing.

    :param password: The password to hash.
    :return: A salted, hashed password as a byte string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Create a hashed password
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check that a provided password matches the hashed password.

    :param hashed_password: The hashed password.
    :param password: The password to validate.
    :return: True if the password matches the hashed password, otherwise
        False.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
