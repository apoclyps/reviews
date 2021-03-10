import sqlite3
from sqlite3 import Error

from dexi import config


class DBClient:
    def __init__(self, path, filename):
        self.database = f"{path}/{filename}"
        self.connection = None

        try:
            self.connection = self.create_connection()
        except:
            print("Error")
        finally:
            pass

    def create_connection(self):
        """create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.connection = sqlite3.connect(self.database)

    def create_table(self, create_table_sql):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
