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
        CREATE TABLE IF NOT EXISTS rotation(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO member(nom)
                VALUES(?)
                """
                self.cursor.execute(
                    query,
                    (data["nom"],),
                )

                self.conn.commit()
                query = "SELECT * FROM rotation WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_rotation = cursor.fetchone()
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
        updated_rotation = cursor.fetchone()
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


class MemberProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS member(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        code_rotation INTEGER NOT NULL,
        FOREIGN KEY (code_rotation) REFERENCES rotation (code)
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO member(nom,prenom,code_rotation)
                VALUES(?,?,?)
                """
                self.cursor.execute(
                    query,
                    (
                        data["nom"],
                        data["prenom"],
                        data["code_rotation"],
                    ),
                )

                self.conn.commit()
                query = "SELECT * FROM member WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_member = cursor.fetchone()
                return created_member
        except Exception as e:
            print(e)

    def _read(self, code: int):
        query: str = "SELECT * FROM member WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_member = cursor.fetchone()
        return fetched_member

    def _update(self, code: int, data: dict):
        query = """
        UPDATE member
        SET nom = ?, prenom = ?,code_rotation = ? 
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                data["prenom"],
                data["code_rotation"],
                code,
            ),
        )
        self.conn.commit()
        updated_member = cursor.fetchone()
        return updated_member

    def _delete(self, code: int):
        query = "DELETE FROM member WHERE code=?;"
        self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = """
        SELECT *
        FROM member
        JOIN rotation ON equipe.code_rotation = rotation.code;
        """
        cursor = self.cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({f"{col}": str(row[col]) for col in row.keys()})
        return data


class TeamProtocol:
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS equipe(
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        code_member INTEGER ,
        code_rotation INTEGER NOT NULL,
        code_ligne INTEGER NOT NULL,
        code_chauffeur INTEGER NOT NULL,
        code_fourniseur INTEGER NOT NULL,
        FOREIGN KEY (code_member) REFERENCES member (code),
        FOREIGN KEY (code_rotation) REFERENCES rotation (code),
        FOREIGN KEY (code_ligne) REFERENCES ligne (code),
        FOREIGN KEY (code_chauffeur) REFERENCES chauffeur (code),
        FOREIGN KEY (code_fourniseur) REFERENCES fourniseur (code)
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def _create(self, data: dict):
        try:
            with self.conn:
                query: str = """
                INSERT INTO equipe(nom,code_member,code_rotation,code_ligne,code_chauffeur,code_fourniseur)
                VALUES(?,?,?,?,?,?)
                """
                self.cursor.execute(
                    query,
                    (
                        data["nom"],
                        data["code_member"],
                        data["code_rotation"],
                        data["code_ligne"],
                        data["code_chauffeur"],
                        data["code_fourniseur"],
                    ),
                )

                self.conn.commit()
                query = "SELECT * FROM equipe WHERE code=?"
                lastrowid = str(self.cursor.lastrowid)
                cursor = self.cursor.execute(query, (lastrowid,))
                created_team = cursor.fetchone()
                return created_team
        except Exception as e:
            print(e)

    def _read(self, id: int):
        query: str = "SELECT * FROM equipe WHERE code=?"
        cursor = self.cursor.execute(query, (code,))
        fetched_team = cursor.fetchone()
        return fetched_team

    def _update(self, id: int, data: dict):
        query = """
        UPDATE equipe
        SET nom = ?, code_member = ?,code_rotation = ? , code_ligne= ?,
        code_chauffeur = ?, code_fourniseur = ? 
        WHERE code = ?
        """
        cursor = self.cursor.execute(
            query,
            (
                data["nom"],
                data["code_member"],
                data["code_rotation"],
                data["code_ligne"],
                data["code_chauffeur"],
                data["code_fourniseur"],
                code,
            ),
        )
        self.conn.commit()
        updated_team = cursor.fetchone()
        return updated_team

    def _delete(self, id: int):
        query = "DELETE FROM equipe WHERE id=?"
        cursor = self.cursor.execute(query, (code,))
        self.conn.commit()

    def _list(self):
        query: str = "SELECT * FROM equipe"
        """
        SELECT *
        FROM equipe
        JOIN member ON equipe.code_member = member.code
        JOIN rotation ON equipe.code_rotation = rotation.code
        JOIN ligne ON equipe.code_ligne = ligne.code
        JOIN chauffeur ON equipe.code_chauffeur = chauffeur.code
        JOIN fourniseur ON equipe.code_fourniseur = fourniseur.code
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

    def set_data(
        self,
        nom,
    ):
        self.data = {"nom": nom}
        self._create()


class Member:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = MemberProtocol()

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
        prenom,
        code_rotation,
    ):
        self.data = {"nom": nom, "prenom": prenom, "code_rotation": code_rotation}
        self._create()


class Team:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = TeamProtocol()

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
        code_member,
        code_rotation,
        code_ligne,
        code_chauffeur,
        code_fourniseur,
    ):
        self.data = {
            "nom": nom,
            "code_member": code_member,
            "code_rotation": code_rotation,
            "code_ligne": code_ligne,
            "code_chauffeur": code_chauffeur,
            "code_fourniseur": code_fourniseur,
        }
        self._create()
