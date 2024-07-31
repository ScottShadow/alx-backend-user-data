#!/usr/bin/env python3
import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = PII_FIELDS):
        self.FIELDS = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.FIELDS, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    logger = logging.Logger("user_data", 20)  # 20 = logging.INFO level
    # logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def filter_datum(fields, redaction, message, separator):
    pattern = r'=(.*)'
    # print(message)
    content = message.split(separator)
    # print(content)
    new_content = []
    for i in content:
        # print(i)
        v = i.split("=")
        # print(v)
        if i:
            if v[0] in fields:
                new_content.append(re.sub(pattern, "="+redaction, i))
            else:
                new_content.append(i)
    # print(new_content)
    res_string = separator.join(new_content)
    # print(res_string)
    return (res_string+";")


def get_db():
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main() -> None:
    """ Implement a main function
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        # print(message)
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
