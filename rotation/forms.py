from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class RotationForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()

    def fill_data(self, data):
        self.code = str(data["code"])
        self.nom = str(data["nom"])
