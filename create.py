from dexi import config
from dexi.datasource.client import SQLClient
from dexi.datasource.managers import PullRequestManager


def prepare_database():
    """Setup Database"""
    client = SQLClient(path=config.DATA_PATH, filename=config.FILENAME)
    if client.connection:
        manager = PullRequestManager(client=client)
        # manager.drop_table()
        manager.create_table()
    else:
        print("Error! cannot create the database connection.")
