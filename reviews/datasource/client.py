import sqlite3
from sqlite3 import Connection, Error
from typing import Any, List, Optional


class SQLClient:
    """create and manage database connections to the SQLite database"""

    database: str
    connection: Connection

    def __init__(
        self,
        path: str = "",
        filename: str = "",
        connection: Optional[Connection] = None,
    ) -> None:
        self.database = f"{path}/{filename}"
        if connection:
            self.connection = connection
        else:
            self.connection = self.create_connection()

    def create_connection(self) -> Connection:
        """create a database connection to the SQLite database specified by db_file."""
        return sqlite3.connect(self.database)

    def create_table(self, create_table_sql: str) -> None:
        """create a table from the create_table_sql statement."""

        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_sql)
        except Error as exc:
            print(exc)
            raise exc

    def query(self, sql: str, data=None) -> List[Any]:
        """query a table from a given sql statement."""

        with self.connection as db:
            cursor = db.cursor()

            cursor.execute("PRAGMA Foreign_Keys = ON")
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

            return cursor.fetchall()

    def insert(self, sql: str, data=None) -> int:
        """query a table from a given sql statement."""

        with self.connection as db:
            cursor = db.cursor()

            cursor.execute("PRAGMA Foreign_Keys = ON")
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

            return cursor.lastrowid
