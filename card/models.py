import sqlite3


class CardProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS card(
        code INTEGER PRIMARY KEY AUTOINCREMENT ,
        code_equipe INTEGER NOT NULL ,
        FOREIGN KEY (code_equipe) REFERENCES equipe(code) ON DELETE CASCADE
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO card(code,code_equipe)
                VALUES(?,?)
                """
                self.cursor.execute(
                    query,
                    (data["code"], data["code_equipe"]),
                )

                self.conn.commit()
                query = "SELECT * FROM card WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_card = cursor.fetchone()
                return created_card

        except Exception as e:
            print(e)

    def _read(self, code: int):
        query: str = "SELECT * FROM card WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_card = cursor.fetchone()
        return fetched_card

    def _update(self, code: int, data: dict):
        query = """
        UPDATE card
        SET code_equipe = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["code_equipe"],
                code,
            ),
        )
        self.conn.commit()
        updated_card = cursor.fetchone()
        return updated_card

    def _delete(self, code: int):
        query = "DELETE FROM card WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = """
        SELECT *
        FROM card
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Card:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = CardProtocol()

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

    def set_data(self, code, code_equipe):
        self.data = {"code": code, "code_equipe": code_equipe}
