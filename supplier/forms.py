from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from supplier.models import Supplier

import sqlite3


class SupplierForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.nom = data["nom"]
        self.telephone = data["telephone"]
        self.adresse = data["adresse"]


class FactureForm(MDBoxLayout):
    start = StringProperty()
    end = StringProperty()
    fourniseur = ObjectProperty()

    def show_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_save)
        date_picker.open()
        self.instance = instance

    def on_date_save(self, instance, value, date_range):
        self.instance.text = value.strftime("%Y-%m-%d") + self.instance.value

    def get_fourniseur_list(self):
        conn = sqlite3.connect("sqlite.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        fournisuer_list = []
        query = """
            select f.code , f.nom
            from pointage p 
            JOIN card c ON p.card = c.code
            JOIN equipe e ON c.code_equipe = e.code
            JOIN fourniseur f ON e.code_fourniseur = f.code
            GROUP BY f.code
        """
        rows = c.execute(query).fetchall()
        for row in rows:
            fournisuer_list.append({f"{col}": str(row[col]) for col in row.keys()})

        print(f"FOURNISEUR LIST \n\n\n {fournisuer_list}")

        menu_list = [
            {
                "text": fourniseur["nom"],
                "value": fourniseur["code"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=fourniseur: self.set_item(x),
            }
            for fourniseur in fournisuer_list
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.id_fourniseur,
            items=menu_list,
            position="center",
            width_mult=4,
        )
        self.menu.bind()
        self.menu.open()

    def set_item(self, fourniseur):
        self.fourniseur = fourniseur
        self.ids.id_fourniseur.text = fourniseur["nom"]
        self.menu.dismiss()
