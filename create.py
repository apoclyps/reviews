from dexi import config
from dexi.datasource.client import DBClient


def prepare_database():
    sql_create_pull_requests_table = """ CREATE TABLE IF NOT EXISTS pull_requests (
                                            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                                            title       TEXT        NOT NULL,
                                            created_at  TEXT        NOT NULL,
                                            updated_at  TEXT        NOT NULL,
                                            approved    INTEGER     DEFAULT 0
                                        ); """

    client = DBClient(path=config.DATA_PATH, filename=config.FILENAME)
    if client.connection:
        client.create_table(sql_create_pull_requests_table)
    else:
        print("Error! cannot create the database connection.")

    
"""INSERT INTO pull_requests (title, created_at, updated_at, approved) VALUES ('Example PR', '2019-09-07T-15:50+00', '2019-09-07T-15:50+00', 0);"""

