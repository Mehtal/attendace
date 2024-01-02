from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen


class SupplierDetailScreen(Screen):
    model = ObjectProperty
    # supplier = Supplier()

    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, code):
        self.data = self.model._read(code)
        print(self.data, "\n ***********\n")
        self.code = str(self.data["code"])
        self.nom = self.data["nom"]
        self.telephone = self.data["telephone"]
        self.adresse = self.data["adresse"]

    def create_supplier(self, form):
        screen = self.manager.get_screen("sup")
        screen.create_supplier(form)
        self.manager.current = "sup"
