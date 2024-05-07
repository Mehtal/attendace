from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class LigneForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.nom = data["nom"]
