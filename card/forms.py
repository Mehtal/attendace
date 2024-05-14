from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from team.models import Team


class CardForm(MDBoxLayout):
    code = StringProperty()
    equipe = ObjectProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.equipe = Team()._read(data["code_equipe"])

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
