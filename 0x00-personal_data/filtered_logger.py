#!/usr/bin/env python3
"""Module for filtering sensitive data from log messages."""

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
    pattern = f"(?:{separator}|^)({'|'.join(fields)})=.*?(?={separator}|$)"
    return re.sub(pattern, r'\1=' + redaction, message)
