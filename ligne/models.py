import sqlite3


class LigneProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS ligne(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO ligne(nom)
                VALUES(?)
                """
                self.cursor.execute(
                    query,
                    (data["nom"],),
                )

                self.conn.commit()
                query = "SELECT * FROM ligne WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_ligne = cursor.fetchone()
                return created_ligne

        except Exception as e:
            print(e)

    def _read(self, code: int):
        query: str = "SELECT * FROM ligne WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_ligne = cursor.fetchone()
        return fetched_ligne

    def _update(self, code: int, data: dict):
        query = """
        UPDATE ligne
        SET nom = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                code,
            ),
        )
        self.conn.commit()
        updated_ligne = cursor.fetchone()
        return updated_ligne

    def _delete(self, code: int):
        query = "DELETE FROM ligne WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = """
        SELECT *
        FROM ligne
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Ligne:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = LigneProtocol()

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

    def set_data(
        self,
        nom,
    ):
        self.data = {"nom": nom}
