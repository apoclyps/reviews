from typing import Any, List

from app.datasource.client import SQLClient
from app.models import PullRequest


class PullRequestManager:
    """Manager for PullRequests Table"""

    client: SQLClient
    table_name: str

    def __init__(self, client: SQLClient) -> None:
        self.client = client
        self.table_name = "pull_requests"

    def create_table(self):
        """creates the table."""
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}
             (
                id INTEGER PRIMARY KEY autoincrement,
                number INTEGER,
                title text NOT NULL,
                created_at text NOT NULL,
                updated_at text NOT NULL,
                approved INTEGER DEFAULT 0
             );
            """
        return self.client.query(sql=sql)

    def drop_table(self):
        """drops the Table."""
        sql = f"""
            DROP TABLE IF EXISTS {self.table_name};
            """
        return self.client.query(sql=sql)

    def all(self):
        """fetch all persisted database rows for pull requests."""
        sql = f"""
            SELECT *
            FROM {self.table_name};
        """
        return self.client.query(sql=sql)

    def get_by_id(self, row_id: int):
        """fetch all persisted database rows for pull requests."""
        sql = f"""
            SELECT *
            FROM   {self.table_name}
            WHERE  id = ?;
        """
        return self.client.query(sql=sql, data=(row_id,))

    def insert_all(self, models: List[PullRequest]) -> List[Any]:
        """inserts a list of models into the database"""
        inserted = []
        for pull_request in models:
            row = self.insert(pull_request=pull_request)
            inserted.append(row)

        return inserted

    def insert(self, pull_request):
        """insert pull request into database."""
        sql = f"""
            INSERT INTO {self.table_name}
            (
                    title,
                    created_at,
                    updated_at,
                    approved,
                    number
            )
            VALUES (?,?,?,?,?);
            """

        return self.client.query(
            sql=sql,
            data=(
                pull_request.title,
                pull_request.created_at,
                pull_request.updated_at,
                pull_request.approved,
                pull_request.number,
            ),
        )

    def update(self, pull_request):
        """upsert pull request into database."""
        sql = f"""
            UPDATE into {self.table_name}
            SET
                title = ?,
                created_at = ?,
                updated_at = ?,
                approved = ?,
                number = ?
            WHERE id = ?;
            """

        return self.client.query(
            sql=sql,
            data=(
                pull_request.title,
                pull_request.created_at,
                pull_request.updated_at,
                pull_request.approved,
                pull_request.number,
            ),
        )

    def delete(self, row_id):
        """delete from the table"""
        sql = f"""
            DELETE FROM {self.table_name}
            WHERE id = ?;
        """
        return self.client.query(
            sql=sql,
            data=(row_id,),
        )
