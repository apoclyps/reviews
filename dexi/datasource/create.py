# import os

# import sqlite3
# from dexi import config

# os.makedirs(config.data_path, exist_ok=True)

# db = sqlite3.connect(config.DATA_PATH + config.FILENAME + '.sqlite3')
# db.execute('CREATE TABLE IF NOT EXISTS PullRequests (id INTEGER PRIMARY KEY, number INTEGER)')
# db.close()