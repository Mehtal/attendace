import sqlite3


class PointageProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query = """
        CREATE TABLE IF NOT EXISTS pointage (
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        card INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        entring INTEGER DEFAULT 0,
        rotation_start TEXT ,
        FOREIGN KEY(card) REFERENCES card(code)
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query = """
                INSERT INTO pointage(card, timestamp,entring,rotation_start)
                VALUES(?, ?,?,?)
                """
                self.cursor.execute(
                    query,
                    (
                        data["card"],
                        data["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                        data["entring"],
                        data["rotation_start"],
                    ),
                )

                self.conn.commit()
                lastrowid = str(self.cursor.lastrowid)
                query = "SELECT * FROM pointage WHERE code=?"
                cursor = self.cursor.execute(query, (lastrowid,))
                created_pointage = cursor.fetchone()
                return created_pointage
        except Exception as e:
            print(e)

    def _read(self, code: int):
        query = "SELECT * FROM pointage WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_pointage = cursor.fetchone()
        if fetched_pointage:
            fetched_pointage["timestamp"] = datetime.strptime(
                fetched_pointage["timestamp"], "%Y-%m-%d %H:%M:%S"
            )
        return fetched_pointage

    def _update(self, code: int, data: dict):
        query = """
        UPDATE pointage
        SET card = ?,
            timestamp = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["card"],
                data["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                code,
            ),
        )
        self.conn.commit()
        updated_pointage = cursor.fetchone()
        if updated_pointage:
            updated_pointage["timestamp"] = datetime.strptime(
                updated_pointage["timestamp"], "%Y-%m-%d %H:%M:%S"
            )
        return updated_pointage

    def _delete(self, code: int):
        query = "DELETE FROM pointage WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query = """
        SELECT *
        FROM pointage
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Pointage:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = PointageProtocol()

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

    def set_data(self, card, timestamp, entring=0, rotation_start=""):
        self.data = {
            "card": card,
            "timestamp": timestamp,
            "entring": entring,
            "rotation_start": rotation_start,
        }
