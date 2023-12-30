from database import Basedb


class TeamProtocol(Basedb):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_create()

    def _table_create(self):
        query: str = """
        CREATE TABLE IF NOT EXISTS equipe(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        code_member INTEGER ,
        code_rotation INTEGER ,
        code_ligne INTEGER ,
        code_chauffeur INTEGER ,
        code_fourniseur INTEGER ,
        FOREIGEN KEY (code_member) REFERENCES member (id),
        FOREIGEN KEY (code_rotation) REFERENCES rotation (id),
        FOREIGEN KEY (code_ligne) REFERENCES ligne (id),
        FOREIGEN KEY (code_chauffeur) REFERENCES chauffeur (id),
        FOREIGEN KEY (code_fourniseur) REFERENCES forniseur (id),
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
                query = "SELECT * FROM equipe WHERE id=?"
                lastrowid = self.cursor.lastrowid
                cursor = self.cursor.execute(query, str(lastrowid))
                created_team = cursor.fetchone()
                return created_team
        except Exception as e:
            print(e)

    def _read(self, id: int):
        query: str = "SELECT * FROM equipe WHERE id=?"
        cursor = self.cursor.execute(query, str(id))
        fetched_team = cursor.fetchone()
        return fetched_team

    def _update(self, id: int, data: dict):
        query = """
        UPDATE equipe
        SET nom = ?, code_member = ?,code_rotation = ? , code_ligne= ?,
        code_chauffeur = ?, code_fourniseur = ? 
        WHERE id = ?
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
                id,
            ),
        )
        self.conn.commit()
        updated_team = cursor.fetchone()
        return updated_team

    def _delete(self, id: int):
        query = "DELETE FROM equipe WHERE id=?"
        cursor = self.cursor.execute(query, str(id))
        self.conn.commit()

    def _list(self):
        query: str = "SELECT * FROM equipe"
        cursor = self.cursor.execute(query)
        fetch_list = cursor.fetchall()
        return fetch_list


class Team(SupplierProtocol):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.db = TeamProtocol()

    def _create(self):
        return self.db._create(self.data)

    def _read(self, id: int):
        return self.db._read(id)

    def _update(self, id: int):
        return self.db._update(id, self.data)

    def _delete(self, id):
        return self.db._delete(id)

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
