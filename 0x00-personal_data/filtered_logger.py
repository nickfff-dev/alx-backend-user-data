#!/usr/bin/env python3
"""Module for filtering sensitive data from log messages."""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in a log message using a single regex
    substitution.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace field values with.
        message (str): The log message to filter.
        separator (str): Character separating fields in the log message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    regex = separator.join([f"(?<={field}=)[^;]*" for field in fields])
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_format,
                            self.SEPARATOR)
