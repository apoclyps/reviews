import sqlite3
from sqlite3 import Error


class DBClient:
    """create and manage database connections to the SQLite database"""

    def __init__(self, path, filename):
        self.database = f"{path}/{filename}"
        self.connection = self.create_connection()

    def create_connection(self):
        """create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        return sqlite3.connect(self.database)

    def create_table(self, create_table_sql):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """

        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_sql)
        except Error as exc:
            print(exc)
            raise exc

    def query(self, sql, data=None):
        """Query for data"""
        with self.connection as db:
            cursor = db.cursor()

            cursor.execute("PRAGMA Foreign_Keys = ON")
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

            return cursor.fetchall()

    def select_all(self, table_name):
        "show all the data of table from db"
        sql = "SELECT * FROM {0}".format(table_name)
        return self.query(sql, ())

    # def insert(
    #     self, table_name, firstname, lastname, street, town, postcode, telephone, email
    # ):
    #     "insert new data"
    #     sql = """
    #             INSERT INTO {0}(FirstName, LastName, Street, Town, PostCode, TelephoneNumber, EMailAddress)
    #             VALUES (?,?,?,?,?,?,?)
    #             """.format(
    #         table_name
    #     )
    #     query(
    #         sql=sql,
    #         data=(
    #             firstname,
    #             lastname,
    #             street,
    #             town,
    #             postcode,
    #             telephone,
    #             email,
    #         ),
    #     )

    # def update(
    #     self,
    #     table_name,
    #     customerid,
    #     firstname,
    #     lastname,
    #     street,
    #     town,
    #     postcode,
    #     telephone,
    #     email,
    # ):
    #     "update the product"
    #     sql = """
    #             UPDATE {0} SET FirstName=?, LastName=?, Street=?, Town=?, PostCode=?, TelephoneNumber=?, EMailAddress=?
    #             WHERE CustomerID=?
    #             """.format(
    #         table_name
    #     )
    #     query(
    #         sql=sql,
    #         data=(
    #             firstname,
    #             lastname,
    #             street,
    #             town,
    #             postcode,
    #             telephone,
    #             email,
    #             customerid,
    #         ),
    #     )

    # def delete(db_name, table_name, customerid):
    #     "delete the product from the table"
    #     sql = "DELETE FROM {0} WHERE CustomerID=?".format(table_name)
    #     query(db_name, sql, (customerid,))
