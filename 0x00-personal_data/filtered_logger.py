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
    """Obfuscates specified fields in a log message using a single regex."""
    for field in fields:
        message = re.sub(f"{field}=(.*?){separator}",
                         f"{field}={redaction}{separator}", message)
    return message


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
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


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
    cnctn = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=database
    )
    return cnctn


def main():
    """Fetch a db connection from get_db and select all rows in
    the users table
    and display each row under a filtered format."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    csv_headers = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        logger.info(
            "{}".format(
                "; ".join(
                    f"{csv_headers[i]}={str(row[i])}" for i in range(
                        len(row)))))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
