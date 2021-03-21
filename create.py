from pathlib import Path

from app import config
from app.datasource import PullRequestManager, SQLClient


def prepare_database():
    """Setup Database"""
    Path(config.DATA_PATH).mkdir(parents=True, exist_ok=True)

    client = SQLClient(path=config.DATA_PATH, filename=config.FILENAME)
    if client.connection:
        manager = PullRequestManager(client=client)
        # manager.drop_table()
        manager.create_table()
    else:
        print("Error! cannot create the database connection.")
