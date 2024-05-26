from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from card.models import Card
from team.models import Team


class PointageForm(MDBoxLayout):
    code = StringProperty()
    card = ObjectProperty()
    timestamp = StringProperty()

    def load_data(self, data):
        self.code = str(data["code"])
        self.card = Card()._read(data["card"])
        self.timestamp = data["timestamp"]

    def get_card_list(self, caller, card_model):
        menu_list = [
            {
                "text": Team()._read(item["code_equipe"])["nom"],
                "value": item["code"],
                "model": card_model,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item, field=caller: self.set_card(x, field),
            }
            for item in card_model()._list()
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_list,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def set_card(self, x, field):
        field.text = Team()._read(x["code_equipe"])["nom"]
        field.value = x["code"]
        self.menu.dismiss()

    def show_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_save)
        date_picker.open()
        self.instance = instance

    def show_time_picker(self, instance):
        time_picker = MDTimePicker()
        time_picker.bind(on_save=self.on_time_save)
        time_picker.open()
        self.instance = instance

    def on_date_save(self, instance, value, date_range):
        self.instance.text = value.strftime("%Y-%m-%d")
        self.update_timestamp()

    def on_time_save(self, instance, time):
        self.instance.text = time.strftime("%H:%M")
        self.update_timestamp()

    def update_timestamp(self):
        # Ensure both date and time are set before updating the timestamp
        if hasattr(self, "date_instance") and hasattr(self, "time_instance"):
            self.timestamp = f"{self.date_instance.text} {self.time_instance.text}"
