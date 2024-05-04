from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from driver.models import Driver
from ligne.models import Ligne
from supplier.models import Supplier
from team.models import Rotation


class RotationForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()

    def load_rotation(self, data):
        self.code = str(data["code"])
        self.nom = str(data["nom"])


class TeamForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    rotation = Rotation
    ligne = Ligne
    chauffeur = Driver
    fourniseur = Supplier

    def get_menu_list(self, caller, model):
        menu_list = [
            {
                "text": item["nom"],
                "value": item["code"],
                "model": model,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item, field=caller: self.set_items(x, field),
            }
            for item in model()._list()
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_list,
            position="bottom",
            width_mult=4,
        )
        self.menu.bind()
        self.menu.open()

    def set_items(self, x, field):
        field.text = x["nom"]
        field.value = x["code"]
        self.menu.dismiss()

    # def set_item(self, fourniseur):
    #     self.fourniseur = fourniseur
    #     self.code_fourniseur = fourniseur["code"]
    #     self.ids.id_fourniseur.text = fourniseur["nom"]
    #     self.menu.dismiss()
    # def load_data(self, data):
    #     print(f"Loading data : {data}")
    #     self.code = str(data["code"])
    #     self.nom = data["nom"]
    #     self.rotation = Rotation()._read(data["code_rotation"])
    #     self.ligne = Ligne()._read(data["code_ligne"])
    #     self.chauffeur = Driver()._read(data["code_chauffeur"])
    #     self.fourniseur = Supplier()._read(data["code_fourniseur"])
