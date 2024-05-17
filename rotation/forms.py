from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class RotationForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    type_rotation = StringProperty()

    def fill_data(self, data):
        self.code = str(data["code"])
        self.nom = str(data["nom"])
        self.type_rotation = str(data["type_rotation"])
