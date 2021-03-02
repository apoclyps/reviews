from dexi import config
from dexi.datasource.client import create_connection, create_table


def prepare_database():
    database = config.DATA_PATH + "/" + config.FILENAME

    sql_create_pull_requests_table = """ CREATE TABLE IF NOT EXISTS pull_requests (
                                            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                                            title       TEXT        NOT NULL,
                                            created_at  TEXT        NOT NULL,
                                            updated_at  TEXT        NOT NULL,
                                            approved    INTEGER     DEFAULT 0
                                        ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_pull_requests_table)
    else:
        print("Error! cannot create the database connection.")

    
"""INSERT INTO pull_requests (title, created_at, updated_at, approved) VALUES ('Example PR', '2019-09-07T-15:50+00', '2019-09-07T-15:50+00', 0);"""

# if __name__ == '__main__':
#     prepare_database()
