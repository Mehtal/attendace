from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from team.models import Rotation, Team
from team.forms import TeamForm, RotationForm
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

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="CREATE TEAM",
                type="custom",
                content_cls=TeamForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_team(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            self.dialog.title = "UPDATE DRIVER"
            # data = self.model()._read(code)
            # form.load_data(data)
            # button = MDRectangleFlatButton(
            #     text="UPDATE", on_release=lambda x: self.update_driver(form)
            # )
            # form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def open_rotation_modal(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Create Rotation",
                type="custom",
                content_cls=RotationForm(),
            )
        form = self.dialog.content_cls
        button = MDRectangleFlatButton(
            text="CREATE", on_release=lambda x: self.create_rotation(form)
        )
        form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def create_rotation(self, form):
        nom = form.ids.id_nom.text
        rotation = Rotation()
        rotation.set_data(nom)
        rotation._create()
        self.dialog_close()

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

    def create_team(self, form):
        nom = form.ids.id_nom.text
        rotation = form.ids.id_rotation.value
        ligne = form.ids.id_ligne.value
        chauffeur = form.ids.id_chauffeur.value
        fourniseur = form.ids.id_fourniseur.value
        team = self.model()
        team.set_data(nom, rotation, ligne, chauffeur, fourniseur)
        print(team.data, "-------***************")
        team._create()
        # self.rv.load_data(self.model)
        self.dialog_close()

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
