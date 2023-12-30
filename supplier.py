import sqlite3

from database import Basedb


class SupplierProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self):
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS forniseur(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        telephone TEXT NOT NULL,
        adresse TEXT NOT NULL)
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO forniseur(nom,telephone,adresse)
                VALUES(?,?,?)
                """
                self.cursor.execute(
                    query, (data["nom"], data["telephone"], data["adresse"])
                )

                self.conn.commit()
                query = "SELECT * FROM forniseur WHERE code=?"
                lastrowid = self.cursor.lastrowid
                cursor = self.cursor.execute(
                    query,
                    (lastrowid,),
                )
                created_supplier = cursor.fetchone()
                return created_supplier
        except Exception as e:
            print(e)

    def _read(self, id: str):
        query: str = "SELECT * FROM forniseur WHERE code=?"
        cursor = self.cursor.execute(query, (id,))
        fetched_supplier = cursor.fetchone()
        return fetched_supplier

    def _update(self, id: str, data: dict):
        query = """
        UPDATE forniseur
        SET nom = ?, telephone = ?,adresse = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                data["telephone"],
                data["adresse"],
                id,
            ),
        )
        self.conn.commit()
        updated_supplier = cursor.fetchone()
        return updated_supplier

    def _delete(self, id: str) -> None:
        query = "DELETE FROM forniseur WHERE code= ? "
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def _list(self) -> list:
        query: str = "SELECT * FROM forniseur"
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data

    def _close(self):
        self.conn.close()


class Supplier:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = SupplierProtocol()

    def _create(self):
        return self.db._create(self.data)

    def _read(self, id: str):
        return self.db._read(id)

    def _update(self, id: str):
        return self.db._update(id, self.data)

    def _delete(self, id: str):
        return self.db._delete(id)

    def _list(self):
        return self.db._list()

    def set_data(self, nom, telephone, adresse):
        self.data = {"nom": nom, "telephone": telephone, "adresse": adresse}
        self._create()
        print(self._list())
