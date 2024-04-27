#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """ DB"""

    def __init__(self):
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ this method adds a new user to the database
        and returns the corresponding User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """ This method takes in arbitrary keyword arguments
        and returns the first row found in the users table
        """
        if not kwargs:
            raise InvalidRequestError

        fields = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in fields:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ This method takes a required integer argument
        user_id and arbitrary keyword arguments, and returns None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f'User with id {user_id} not found')

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f'User has no attribute {key}')
            setattr(user, key, value)
        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError('Invalid request')