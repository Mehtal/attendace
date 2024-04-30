from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from team.models import Rotation, Team

from kivy.uix.recycleview.views import RecycleDataViewBehavior


class TeamDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    code_rotation = StringProperty()
    code_ligne = StringProperty()
    code_chauffeur = StringProperty()
    code_fourniseur = StringProperty()

    def on_delete(self, model):
        model._delete(self.code)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        self.code_rotation = data["rotation"]
        self.code_ligne = data["code_ligne"]
        self.code_chauffeur = data["code_chauffeur"]
        self.code_fourniseur = data("code_fourniseur")
        return super().refresh_view_attrs(rv, index, data)


class TeamScreen(Screen):
    model = Team
    dialog = None

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = TeamDataRow
        self.rv.load_data(self.model)

    # def detail_driver(self, code):
    #     detail_screen = self.manager.get_screen("driver-detail")
    #     detail_screen.model = self.model
    #     detail_screen.load_data(code)
    #     self.manager.current = "driver-detail"
    #
    # def delete_driver(self, code: str) -> None:
    #     self.model()._delete(code)
    #     self.rv.load_data(self.model)
    #
    # def open_modal(self, code: str = "", update: bool = False):
    #     if not self.dialog:
    #         self.dialog = MDDialog(
    #             title="CREATE DRIVER",
    #             type="custom",
    #             content_cls=DriverForm(),
    #         )
    #     form = self.dialog.content_cls
    #     if not update:
    #         button = MDRectangleFlatButton(
    #             text="CREATE", on_release=lambda x: self.create_driver(form)
    #         )
    #         form.ids.id_btn_list.add_widget(button)
    #     else:
    #         self.dialog.title = "UPDATE DRIVER"
    #         data = self.model()._read(code)
    #         form.load_data(data)
    #         button = MDRectangleFlatButton(
    #             text="UPDATE", on_release=lambda x: self.update_driver(form)
    #         )
    #         form.ids.id_btn_list.add_widget(button)
    #     self.dialog.open()
    #
    # def update_driver(self, form):
    #     code = form.code
    #     nom = form.ids.id_nom.text
    #     prenom = form.ids.id_prenom.text
    #     code_fourniseur = form.fourniseur["code"]
    #     driver = self.model()
    #     driver.set_data(nom, prenom, code_fourniseur)
    #     driver._update(code)
    #     self.rv.load_data(self.model)
    #     self.dialog_close()
    #
    # def create_driver(self, form):
    #     nom = form.ids.id_nom.text
    #     prenom = form.ids.id_prenom.text
    #     code_fourniseur = form.fourniseur["code"]
    #     driver = self.model()
    #     driver.set_data(nom, prenom, code_fourniseur)
    #     driver._create()
    #     self.rv.load_data(self.model)
    #     self.dialog_close()
    #
    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
