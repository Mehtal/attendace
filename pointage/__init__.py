from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from pointage.models import Pointage
from pointage.forms import PointageForm
from card.models import Card
from team.models import Team


class PointageDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    card = ObjectProperty()
    team = ObjectProperty()
    timestamp = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.card = Card()._read(data["card"])
        self.team = Team()._read(self.card["code_equipe"])["nom"]
        self.timestamp = data["timestamp"]
        super().refresh_view_attrs(rv, index, data)


class PointageScreen(Screen):
    model = Pointage
    dialog = None
    viewclass = PointageDataRow

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = PointageDataRow
        self.rv.load_data(self.model)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE Pointage",
                type="custom",
                content_cls=PointageForm(),
            )
        form = self.dialog.content_cls
        form.ids.id_btn_list.clear_widgets()  # Clear previous buttons if any

        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_pointage(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            self.dialog.title = "UPDATE Pointage"
            data = self.model()._read(int(code))
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_pointage(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_pointage(self, form):
        card = form.ids.id_card.value
        timestamp = form.timestamp
        pointage = self.model()
        pointage.set_data(card, timestamp)
        pointage._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def update_pointage(self, form):
        code = form.code
        card = form.ids.id_card.value
        timestamp = form.timestamp
        pointage = self.model()
        pointage.set_data(card, timestamp)
        pointage._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_pointage(self, code: str) -> None:
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
