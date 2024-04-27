#!/usr/bin/env python3
""" This module defines a class called User
    that inherits from Base class from SQLAlchemy
    and defines the table called users and its columns
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ This function takes in a string password
    and returns a hashed version of the password
    """
    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """ This function returns a string representation of a new UUID
    """
    UUID = uuid4()
    return str(UUID)


class Auth:
    """ Auth class
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """  This method takes in an email and password
        and returns a new User object
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ This method takes in an email and password
        and returns true if the password is valid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        plain_password = user.hashed_password
        encoded_password = password.encode()

        if bcrypt.checkpw(encoded_password, plain_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """ This method takes in an email and returns a session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ This method takes in a session ID and returns a User object
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """ This method takes in a user_id and returns None
        after updating the user's session ID to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """ This method takes in an email and returns a reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = _generate_uuid()

        self._db.update_user(user.id, reset_token=token)

        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ This method takes in a reset token and a password
        and returns None after updating the user's password
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
