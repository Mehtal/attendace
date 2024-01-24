import sqlite3


class DriverProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS chauffeur(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        code_fourniseur INTEGER ,
        FOREIGN KEY (code_fourniseur) REFERENCES fourniseur (code)
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _table_info(self):
        self.cursor.execute("PRAGMA table_info(chauffeur)")
        cols = self.cursor.fetchall()
        col_name = [col["name"] for col in cols]
        return col_name

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO chauffeur(nom,prenom,code_fourniseur)
                VALUES(?,?,?)
                """
                self.cursor.execute(
                    query,
                    (
                        data["nom"],
                        data["prenom"],
                        data["code_fourniseur"],
                    ),
                )

                self.conn.commit()
                query = "SELECT * FROM chauffeur WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_chauffeur = cursor.fetchone()
                return created_chauffeur
        except Exception as e:
            print(e)

    def _read(self, code: str):
        query: str = "SELECT * FROM chauffeur WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_chauffeur = cursor.fetchone()
        return fetched_chauffeur

    def _update(self, code: str, data: dict):
        query = """
        UPDATE chauffeur
        SET nom = ?, prenom = ?, code_fourniseur = ?
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                data["prenom"],
                data["code_fourniseur"],
                code,
            ),
        )
        self.conn.commit()
        updated_chauffeur = cursor.fetchone()
        return updated_chauffeur

    def _delete(self, code: str):
        query = "DELETE FROM chauffeur WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = """
            SELECT *,fourniseur.nom as nom_fourniseur
            FROM chauffeur
            JOIN fourniseur ON 
            code_fourniseur = fourniseur.code;
            """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class Driver:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = DriverProtocol()

    def _create(self):
        return self.db._create(self.data)

    def _read(self, code: str):
        return self.db._read(code)

    def _update(self, code: str):
        return self.db._update(code, self.data)

    def _delete(self, code):
        return self.db._delete(code)

    def _list(self):
        return self.db._list()

    def _table_info(self):
        return self.db._table_info()

    def set_data(
        self,
        nom,
        prenom,
        code_fourniseur,
    ):
        self.data = {
            "nom": nom,
            "prenom": prenom,
            "code_fourniseur": code_fourniseur,
        }
