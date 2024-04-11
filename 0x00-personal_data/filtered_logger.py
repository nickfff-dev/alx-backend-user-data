#!/usr/bin/env python3
"""Module for filtering sensitive data from log messages."""

import logging
import os
import mysql.connector
import re
from typing import List

# Define the fields considered as PII data
PII_FIELDS = ("email", "ssn", "password", "phone", "ip")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in a log message using a single regex
    sub."""
    regex = separator.join([f"(?<={field}=)[^;]*" for field in fields])
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes a RedactingFormatter object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values from the log message using filter_datum."""
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_format,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and returns a logger with a specific configuration."""
    # Create a logger object
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler with specific formatting
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a MySQL database using environment variables.

    Returns a MySQLConnection object.
    """
    # Retrieve environment variables with default values
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    # Establish and return a database connection
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
