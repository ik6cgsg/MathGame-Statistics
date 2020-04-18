import copy
from typing import List, Dict

import psycopg2
from prettytable import PrettyTable
from psycopg2.extras import DictCursor


class MathDataBaseException(Exception):
    pass


class MathDataBase(object):
    def __init__(self):
        self.database: str = "postgres"
        self.user: str = "mathhelperreader"
        self.password: str = "mathhelperreader"
        self.host: str = "mathhelper.space"
        self.port: str = "5432"
        self.connection = None
        self.cursor = None

    def __del__(self):
        if self.cursor is not None and self.connection is not None:
            self.cursor.close()
            self.connection.close()
            print("DB closed: %s" % self.connection.closed)

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        except psycopg2.Error as e:
            raise MathDataBaseException("Connection error: %s" % e)
        print("DB connected successfully!")

    def execute(self, query: str, output: bool = False) -> List[Dict[str, str]]:
        try:
            self.cursor.execute(query)
        except Exception as e:
            raise MathDataBaseException("Cursor execute error: %s" % e)
        result = list(self.cursor)
        if output:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ V Query result table V ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            table = PrettyTable()
            for row in result:
                table.add_row(row)
            print(table)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ^ Query result table ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return result
