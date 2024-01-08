from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class DriverForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    prenom = StringProperty()
    code_fourniseur = StringProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.nom = data["nom"]
        self.prenom = data["prenom"]
        self.code_fourniseur = data["code_fourniseur"]
