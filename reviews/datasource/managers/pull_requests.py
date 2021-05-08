from typing import Any, List

from reviews.datasource.client import SQLClient
from reviews.datasource.models import PullRequest


class PullRequestManager:
    """Manager for PullRequests Table"""

    client: SQLClient
    table_name: str

    def __init__(self, client: SQLClient) -> None:
        self.client = client
        self.table_name = "pull_requests"

    def create_table(self) -> List[Any]:
        """creates the table."""
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}
             (
                id INTEGER PRIMARY KEY autoincrement,
                number INTEGER,
                title text NOT NULL,
                created_at text NOT NULL,
                updated_at text NOT NULL,
                approved text DEFAULT NULL,
                approved_by_others BOOL DEFAULT FALSE
             );
            """
        return self.client.query(sql=sql)

    def drop_table(self) -> List[Any]:
        """drops the Table."""
        sql = f"""
            DROP TABLE IF EXISTS {self.table_name};
            """
        return self.client.query(sql=sql)

    def all(self) -> List[Any]:
        """fetch all persisted database rows for pull requests."""
        sql = f"""
            SELECT *
            FROM {self.table_name};
        """
        return self.client.query(sql=sql)

    def get_by_id(self, row_id: int) -> List[Any]:
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
        for model in models:
            row = self.insert(model=model)
            inserted.append(row)

        return inserted

    def insert(self, model: PullRequest) -> int:
        """insert pull request into database."""
        sql = f"""
            INSERT INTO {self.table_name}
            (
                    title,
                    created_at,
                    updated_at,
                    approved,
                    approved_by_others,
                    number
            )
            VALUES (?,?,?,?,?,?);
            """

        return self.client.insert(
            sql=sql,
            data=(
                model.title,
                model.created_at,
                model.updated_at,
                model.approved,
                model.approved_by_others,
                model.number,
            ),
        )

    def update(self, row_id: int, model: PullRequest) -> List[Any]:
        """upsert pull request into database."""
        sql = f"""
            UPDATE OR REPLACE {self.table_name}
            SET
                title = ?,
                created_at = ?,
                updated_at = ?,
                approved = ?,
                approved_by_others=?,
                number = ?
            WHERE id = ?;
            """

        return self.client.query(
            sql=sql,
            data=(
                model.title,
                model.created_at,
                model.updated_at,
                model.approved,
                model.approved_by_others,
                model.number,
                row_id,
            ),
        )

    def delete(self, row_id: int) -> List[Any]:
        """delete from the table"""
        sql = f"""
            DELETE FROM {self.table_name}
            WHERE id = ?;
        """
        return self.client.query(
            sql=sql,
            data=(row_id,),
        )

    def exists(self) -> bool:
        """checks if the table exists"""
        sql = f"""
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.table_name}' LIMIT 1;
        """
        result = self.client.query(
            sql=sql,
        )

        # first element in the array, first result in the tuple
        exists = result[0][0]

        return bool(int(exists))
