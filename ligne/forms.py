from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class LigneForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    prix = StringProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.nom = data["nom"]
        self.prix = str(data["prix"])
