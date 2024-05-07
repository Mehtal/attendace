from kivy.properties import ObjectProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from supplier.models import Supplier


class DriverForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    prenom = StringProperty()
    fourniseur = ObjectProperty()

    def load_data(self, data):
        print(f"Loading data : {data}")
        self.code = str(data["code"])
        self.nom = data["nom"]
        self.prenom = data["prenom"]
        self.fourniseur = Supplier()._read(data["code_fourniseur"])

    def get_fourniseur_list(self):
        fournisuer_list = Supplier()._list()
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
        self.code_fourniseur = fourniseur["code"]
        self.ids.id_fourniseur.text = fourniseur["nom"]
        self.menu.dismiss()
