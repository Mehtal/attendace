from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from rotation.models import Rotation
from rotation.forms import RotationForm


class RotationDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        super().refresh_view_attrs(rv, index, data)


class RotationScreen(Screen):
    model = Rotation
    dialog = None
    viewclass = RotationDataRow

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = RotationDataRow
        self.rv.load_data(self.model)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE Rotation",
                type="custom",
                content_cls=RotationForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_rotation(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            self.dialog.title = "UPDATE Rotation"
            data = self.model()._read(int(code))
            form.fill_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_rotation(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_rotation(self, form):
        nom = form.ids.id_nom.text
        rotation = self.model()
        rotation.set_data(nom)
        rotation._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def update_rotation(self, form):
        code = form.code
        nom = form.ids.id_nom.text
        rotation = self.model()
        rotation.set_data(nom)
        rotation._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_rotation(self, code: str) -> None:
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
