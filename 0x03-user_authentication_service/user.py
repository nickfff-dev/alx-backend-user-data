#!/usr/bin/env python3
""" This module defines a class called User
    that inherits from Base class from SQLAlchemy
    and defines the table called users and its columns
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """ This class defines a table called users and its columns """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
