from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


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
