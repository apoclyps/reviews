import sqlite3



class PullRequestManager:
    def __init__(self, client):
        self.client = client


    def query(self, sql, data):
        with self.client as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA Foreign_Keys = ON")
            cursor.execute(sql, data)
            result = cursor.fetchall()
            db.commit()
            return result

    # def show_all_data(db_name, table_name):
    #     "show all the data of table from db"
    #     sql = "SELECT * FROM {0}".format(table_name)
    #     return query(db_name, sql, ())

    # def insert_data(db_name, table_name, firstname, lastname, street, town, postcode, telephone, email):
    #     "insert new data"
    #     sql = """
    #             INSERT INTO {0}(FirstName, LastName, Street, Town, PostCode, TelephoneNumber, EMailAddress)
    #             VALUES (?,?,?,?,?,?,?)
    #             """.format(table_name)
    #     query(db_name, sql, (firstname, lastname, street, town, postcode, telephone, email,))

    # def update_data(db_name, table_name, customerid, firstname, lastname, street, town, postcode, telephone, email):
    #     "update the product"
    #     sql = """
    #             UPDATE {0} SET FirstName=?, LastName=?, Street=?, Town=?, PostCode=?, TelephoneNumber=?, EMailAddress=?
    #             WHERE CustomerID=?
    #             """.format(table_name)
    #     query(db_name, sql, (firstname, lastname, street, town, postcode, telephone, email, customerid,))

    # def delete_data(db_name, table_name, customerid):
    #     "delete the product from the table"
    #     sql = "DELETE FROM {0} WHERE CustomerID=?".format(table_name)
    #     query(db_name, sql, (customerid, ))

    # def print_table(result):
    #     "show the data in a table"
    #     print("""
    #         |{0:^5s}|{1:^13s}|{2:^10s}|{3:^10s}|{4:^10s}|{5:^12s}|{6:^20s}|{7:^20s}|
    #         """.format("ID",
    #                 "FirstName",
    #                 "LastName",
    #                 "Street",
    #                 "Town",
    #                 "PostCode",
    #                 "TelephoneNumber",
    #                 "EMailAddress"))
    #     for entry in result:
    #         customerid, firstname, lastname, street, town, postcode, telephone, email = entry
    #         print("""
    #         {0:^5d} {1:^13s} {2:^10s} {3:^10s} {4:^10s} {5:^12s} {6:^20s} {7:^20s}
    #             """.format(customerid,
    #                     firstname,
    #                     lastname,
    #                     street,
    #                     town,
    #                     postcode,
    #                     telephone,
    #                     email))