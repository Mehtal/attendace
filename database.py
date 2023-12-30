import sqlite3
from typing import Protocol


class Basedb(Protocol):
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def _table_create(self):
        pass

    def _create(self, data: dict):
        pass

    def _read(self, id: int):
        pass

    def _update(self, id: int, data: dict):
        pass

    def _delete(self, id: int):
        pass

    def _list(self):
        pass

    def close(self):
        self.conn.close()
