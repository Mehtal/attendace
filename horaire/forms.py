from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from rotation.models import Rotation
from kivymd.uix.pickers import MDTimePicker


class HoraireForm(MDBoxLayout):
    code = StringProperty()
    entree = StringProperty()
    sortie = StringProperty()
    code_rotation = ObjectProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.entree = data["entree"]
        self.sortie = data["sortie"]
        self.code_rotation = Rotation()._read(data["code_rotation"])

    def get_rotation_list(self, caller, rotation_model):
        menu_list = [
            {
                "text": item["nom"],
                "value": item["code"],
                "model": rotation_model,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item, field=caller: self.set_rotation(x, field),
            }
            for item in rotation_model()._list()
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_list,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def set_rotation(self, x, field):
        field.text = x["nom"]
        field.value = x["code"]
        self.menu.dismiss()

    def show_time_picker(self, instance):
        time_picker = MDTimePicker()
        time_picker.bind(on_save=self.on_time_save)
        time_picker.open()
        self.instance = instance

    def on_time_save(self, instance, time):
        self.instance.text = time.strftime("%H:%M")
