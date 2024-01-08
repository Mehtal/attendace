from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from driver.forms import DriverForm
from driver.models import Driver


class DriverScreen(Screen):
    model = Driver()
    dialog = None

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.load_data(Driver)

    def detail_driver(self, code):
        detail_screen = self.manager.get_screen("driver-detail")
        detail_screen.model = self.model
        detail_screen.load_data(code)
        self.manager.current = "driver-detail"

    def delete_driver(self, code: str) -> None:
        self.model._delete(code)
        self.rv.load_data(Driver)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="UPDATE DRIVER",
                type="custom",
                content_cls=DriverForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_driver(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            data = self.model._read(code)
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_driver(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def update_driver(self, form):
        code = form.code
        nom = form.ids.id_nom.text
        prenom = form.ids.id_prenom.text
        code_forniseur = form.ids.id_code_forniseur.text
        self.model.data = {
            "nom": nom,
            "prenom": prenom,
            "code_forniseur": code_forniseur,
        }
        self.model._update(code)
        self.rv.load_data(Driver)
        self.dialog_close()

    def create_driver(self, form):
        nom = form.ids.id_nom.text
        prenom = form.ids.id_prenom.text
        code_forniseur = form.ids.id_code_forniseur.text
        self.model.data = {
            "nom": nom,
            "prenom": prenom,
            "code_forniseur": code_forniseur,
        }
        self.model._create()
        self.rv.load_data(Driver)
        self.dialog_close()

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None


class DriverDetailScreen(Screen):
    model = ObjectProperty
    # driver = driver()

    code = StringProperty()
    nom = StringProperty()
    prenom = StringProperty()
    code_forniseur = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, code):
        self.data = self.model._read(code)
        self.code = str(self.data["code"])
        self.nom = self.data["nom"]
        self.prenom = self.data["prenom"]
        self.code_forniseur = self.data["code_forniseur"]

    def create_driver(self, form):
        screen = self.manager.get_screen("sup")
        screen.create_driver(form)
        self.manager.current = "sup"
