import sqlite3


class RotationProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS rotation (
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        type_rotation TEXT NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO rotation(nom, type_rotation)
                VALUES(?, ?)
                """
                self.cursor.execute(
                    query,
                    (data["nom"], data["type_rotation"]),
                )

                self.conn.commit()
                lastrowid = self.cursor.lastrowid
                created_rotation = self._read(lastrowid)
                return created_rotation
        except Exception as e:
            print(e)

    def _read(self, code: int):
        query: str = "SELECT * FROM rotation WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_member = cursor.fetchone()
        return fetched_member

    def _update(self, code: int, data: dict):
        query = """
        UPDATE rotation
        SET nom = ?,
            type_rotation = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                data["type_rotation"],
                code,
            ),
        )
        self.conn.commit()
        updated_rotation = self._read(code)
        return updated_rotation

    def _delete(self, code: int):
        query = "DELETE FROM rotation WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = """
        SELECT *
        FROM rotation
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Rotation:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = RotationProtocol()

    def _create(self):
        return self.db._create(self.data)

    def _read(self, code: int):
        return self.db._read(code)

    def _update(self, code: int):
        return self.db._update(code, self.data)

    def _delete(self, code):
        return self.db._delete(code)

    def _list(self):
        return self.db._list()

    def set_data(self, nom, type_rotation):
        self.data = {"nom": nom, "type_rotation": type_rotation}
