#!/usr/bin/env python3
"""
Personal data
"""

import logging
import os
import re
from typing import List
import mysql.connector
from mysql.connector import MySQLConnection, Error

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Replace fields with redacted values"""
    for field in fields:
        message = re.sub(rf"{field}=(.*?){separator}",
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """RedactingFormatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter"""
        self.fields = fields
        super().__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format log record"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Implement a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """Implement db connectivity"""
    try:
        psw = os.environ["PERSONAL_DATA_DB_PASSWORD"]
        username = os.environ['PERSONAL_DATA_DB_USERNAME']
        host = os.environ['PERSONAL_DATA_DB_HOST']
        db_name = os.environ['PERSONAL_DATA_DB_NAME']
    except KeyError:
        # logger = get_logger()
        # logger.error("Missing required environment variable: %s", e)
        return None
    try:
        conn = mysql.connector.connect(
            host=host,
            database=db_name,
            user=username,
            password=psw
        )
        return conn
    except Error:
        # logger = get_logger()
        # logger.error("Error connecting to database: %s", err)
        return None


def main() -> None:
    """Implement the main function"""
    logger = get_logger()
    db = get_db()
    if db is None:
        # logger.error("Failed to connect to database")
        return

    with db.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM users;")
            for row in cursor:
                message = (f"name={row[0]}; email={row[1]}; phone={row[2]}; "
                           f"ssn={row[3]}; password=REDACTED; ip={row[5]}; "
                           f"last_login={row[6]}; user_agent={row[7]};")
                logger.info(message)
        except Error:
            # logger.error("Error executing query: %s", err)
            pass
    db.close()


if __name__ == '__main__':
    main()
