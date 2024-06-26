from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from ligne.models import Ligne
from ligne.forms import LigneForm


class LigneDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    prix = StringProperty()

    def delete_data(self, model):
        model._delete(self.code)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        self.prix = data["prix"]
        super().refresh_view_attrs(rv, index, data)


class LigneScreen(Screen):
    model = Ligne
    dialog = None
    viewclass = LigneDataRow

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = LigneDataRow
        self.rv.load_data(self.model)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE Ligne",
                type="custom",
                content_cls=LigneForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_ligne(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            self.dialog.title = "UPDATE LIGNE"
            data = self.model()._read(int(code))
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_ligne(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_ligne(self, form):
        nom = form.ids.id_nom.text
        prix = form.ids.id_prix.text
        ligne = self.model()
        ligne.set_data(nom, int(prix))
        print(ligne.data)
        ligne._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def update_ligne(self, form):
        code = form.code
        nom = form.ids.id_nom.text
        prix = form.ids.id_prix.text
        ligne = self.model()
        ligne.set_data(nom, int(prix))
        ligne._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_ligne(self, code: str) -> None:
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
