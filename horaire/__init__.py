from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout


from horaire.models import Horaire
from horaire.forms import HoraireForm
from rotation.models import Rotation


class HoraireDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    entree = StringProperty()
    sortie = StringProperty()
    rotation = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.entree = data["entree"]
        self.sortie = data["sortie"]
        self.rotation = Rotation()._read(data["code_rotation"])
        super().refresh_view_attrs(rv, index, data)


class HoraireScreen(Screen):
    model = Horaire
    dialog = None
    viewclass = HoraireDataRow

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = HoraireDataRow
        self.rv.load_data(self.model)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE Horaire",
                type="custom",
                content_cls=HoraireForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_horaire(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            self.dialog.title = "UPDATE Horaire"
            data = self.model()._read(int(code))
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_horaire(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_horaire(self, form):
        entree = form.ids.id_entree.text
        sortie = form.ids.id_sortie.text
        code_rotation = form.ids.id_rotation.value
        horaire = self.model()
        horaire.set_data(entree, sortie, code_rotation)
        horaire._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def update_horaire(self, form):
        code = form.code
        entree = form.ids.id_entree.text
        sortie = form.ids.id_sortie.text
        code_rotation = form.ids.id_rotation.value
        horaire = self.model()
        horaire.set_data(entree, sortie, code_rotation)
        horaire._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_horaire(self, code: str) -> None:
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
