import sqlite3


class HoraireProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query = """
        CREATE TABLE IF NOT EXISTS horaire (
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        entree TEXT NOT NULL,
        sortie TEXT NOT NULL,
        code_rotation INTEGER,
        FOREIGN KEY(code_rotation) REFERENCES rotation(code)
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query = """
                INSERT INTO horaire(entree, sortie, code_rotation)
                VALUES(?, ?, ?)
                """
                self.cursor.execute(
                    query,
                    (
                        data["entree"],
                        data["sortie"],
                        data["code_rotation"],
                    ),
                )

                self.conn.commit()
                lastrowid = str(self.cursor.lastrowid)
                query = "SELECT * FROM horaire WHERE code=?"
                cursor = self.cursor.execute(query, (lastrowid,))
                created_horaire = cursor.fetchone()
                return created_horaire
        except Exception as e:
            print(e)

    def _read(self, code: int):
        query = "SELECT * FROM horaire WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_horaire = cursor.fetchone()
        return fetched_horaire

    def _update(self, code: int, data: dict):
        query = """
        UPDATE horaire
        SET entree = ?,
            sortie = ?,
            code_rotation = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["entree"],
                data["sortie"],
                data["code_rotation"],
                code,
            ),
        )
        self.conn.commit()
        updated_horaire = cursor.fetchone()
        return updated_horaire

    def _delete(self, code: int):
        query = "DELETE FROM horaire WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query = """
        SELECT *
        FROM horaire
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Horaire:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = HoraireProtocol()

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
        entree,
        sortie,
        code_rotation,
    ):
        self.data = {
            "entree": entree,
            "sortie": sortie,
            "code_rotation": code_rotation,
        }
