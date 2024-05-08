from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from driver.models import Driver
from ligne.models import Ligne
from supplier.models import Supplier
from team.models import Team
from rotation.models import Rotation
from team.forms import TeamForm
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class TeamDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    rotation = StringProperty()
    ligne = StringProperty()
    driver = StringProperty()
    supplier = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        self.rotation = Rotation()._read(data["code_rotation"])["nom"]
        self.ligne = Ligne()._read(data["code_ligne"])["nom"]
        self.driver = Driver()._read(data["code_chauffeur"])["nom"]
        self.supplier = Supplier()._read(data["code_fourniseur"])["nom"]
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
            query = """
            SELECT equipe.code,equipe.nom ,equipe.code_rotation,
            equipe.code_ligne,equipe.code_chauffeur,equipe.code_fourniseur,
            rotation.nom AS nom_rotation,
            ligne.nom AS nom_ligne,
            chauffeur.nom AS nom_chauffeur,
            fourniseur.nom AS nom_fourniseur
            FROM equipe
            JOIN rotation ON equipe.code_rotation = rotation.code 
            JOIN ligne ON equipe.code_ligne = ligne.code  
            JOIN chauffeur ON equipe.code_chauffeur = chauffeur.code 
            JOIN fourniseur ON equipe.code_fourniseur = fourniseur.code
            WHERE equipe.code = ?
            """
            cursor = self.model().db.cursor
            cursor.execute(query, (code,))
            data = cursor.fetchone()
            form.fill_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_team(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def update_team(self, form):
        code = form.code
        nom = form.ids.id_nom.text
        rotation = form.ids.id_rotation.value
        ligne = form.ids.id_ligne.value
        chauffeur = form.ids.id_chauffeur.value
        fourniseur = form.ids.id_fourniseur.value
        team = self.model()
        team.set_data(nom, rotation, ligne, chauffeur, fourniseur)
        team._update(code)
        self.rv.load_data(self.model)
        self.dialog_close()

    def create_team(self, form):
        nom = form.ids.id_nom.text
        rotation = form.ids.id_rotation.value
        ligne = form.ids.id_ligne.value
        chauffeur = form.ids.id_chauffeur.value
        fourniseur = form.ids.id_fourniseur.value
        team = self.model()
        team.set_data(nom, rotation, ligne, chauffeur, fourniseur)
        team._create()
        self.rv.load_data(self.model)
        self.dialog_close()

    def delete_team(self, code):
        self.model()._delete(code)
        self.rv.load_data(self.model)

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None
