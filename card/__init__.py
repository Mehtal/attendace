from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from card.models import Card
from card.forms import CardForm
from card.misc import create_qr_code, read_qr_code, FileManager
from team.models import Team


class CardDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    equipe = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.equipe = Team()._read(data["code_equipe"])
        super().refresh_view_attrs(rv, index, data)


class CardScreen(Screen):
    model = Card
    dialog = None
    viewclass = CardDataRow

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = CardDataRow
        self.rv.load_data(self.model)

    def edit_card(self):
        read_qr_code()

    def edit_card_from_img(self):
        f = FileManager()
        f.file_manager_open()

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE Card",
                type="custom",
                content_cls=CardForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_card(form)
            )
            form.ids.id_btn_list.add_widget(button)
            rfid = create_qr_code()
            form.code = rfid
        else:
            self.dialog.title = "UPDATE Card"
            data = self.model()._read(int(code))
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_card(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_card(self, form):
        code = form.ids.id_code.text
        code_equipe = form.ids.id_equipe.value
        card = self.model()
        card.set_data(code, code_equipe)
        card._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def update_card(self, form):
        code = form.code
        code_equipe = form.ids.id_equipe.value
        card = self.model()
        card.set_data(code, code_equipe)
        card._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_card(self, code: str) -> None:
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
