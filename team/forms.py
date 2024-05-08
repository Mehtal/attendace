from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from driver.models import Driver
from supplier.models import Supplier


class TeamForm(MDBoxLayout):
    code = StringProperty()
    nom = StringProperty()
    data = ObjectProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ids.id_chauffeur.bind(value=self.get_fournisseur)

    def fill_data(self, data):
        self.data = data

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

    def set_items(self, x, field) -> None:
        field.text = x["nom"]
        field.value = x["code"]
        self.menu.dismiss()

    def get_fournisseur(self, driver_widget, widget_text) -> None:
        supplier_widget = self.ids.id_fourniseur
        driver = Driver()._read(driver_widget.value)
        supplier = Supplier()._read(driver["code_fourniseur"])
        supplier_widget.text = supplier["nom"]
        supplier_widget.value = str(supplier["code"])
