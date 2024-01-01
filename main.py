import os
import sys

BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
from kivy.config import Config as cfg

cfg.set("graphics", "window_state", "maximized")
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout

from components import FlatButton
from components.supplier.create import SupplierForm
from supplier.models import Supplier


class SupplierDetailScreen(Screen):
    model = ObjectProperty
    supplier = Supplier()

    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, code):
        self.data = self.supplier._read(code)
        self.code = str(self.data["code"])
        self.nom = self.data["nom"]
        self.telephone = self.data["telephone"]
        self.adresse = self.data["adresse"]

    def create_supplier(self, form):
        screen = self.manager.get_screen("sup")
        screen.create_supplier(form)
        self.manager.current = "sup"


class SupplierScreen(Screen):
    supplier = Supplier()
    dialog = None

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.load_data(Supplier)

    def detail_supplier(self, code):
        detail_screen = self.manager.get_screen("sup-detail")
        self.manager.current = "sup-detail"

    def delete_supplier(self, id: str) -> None:
        self.supplier._delete(id)
        self.rv.load_data(Supplier)

    def open_modal(self, code: str = "", update: bool = False):
        if not self.dialog:
            self.dialog = MDDialog(
                title="UPDATE SUPPLIER",
                type="custom",
                content_cls=SupplierForm(),
            )
        form = self.dialog.content_cls
        if not update:
            button = MDRectangleFlatButton(
                text="CREATE", on_release=lambda x: self.create_supplier(form)
            )
            form.ids.id_btn_list.add_widget(button)
        else:
            data = self.supplier._read(code)
            form.load_data(data)
            button = MDRectangleFlatButton(
                text="UPDATE", on_release=lambda x: self.update_supplier(form)
            )
            form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def update_supplier(self, form):
        code = form.code
        nom = form.ids.id_nom.text
        telephone = form.ids.id_telephone.text
        adresse = form.ids.id_adresse.text
        self.supplier.data = {
            "nom": nom,
            "telephone": telephone,
            "adresse": adresse,
        }
        self.supplier._update(code)
        self.rv.load_data(Supplier)
        self.dialog_close()

    def create_supplier(self, form):
        nom = form.ids.id_nom.text
        telephone = form.ids.id_telephone.text
        adresse = form.ids.id_adresse.text
        self.supplier.data = {
            "nom": nom,
            "telephone": telephone,
            "adresse": adresse,
        }
        self.supplier._create()
        self.rv.load_data(Supplier)
        self.dialog_close()

    def dialog_close(self, *args):
        self.dialog.dismiss()
        self.dialog = None


class Sidebar(MDFloatLayout):
    pass


class MainApp(MDApp):
    def build(self):
        LabelBase.register(
            name="HackNerdFont",
            fn_regular="fonts/HackNerdFont-Regular.ttf",
            fn_bold="fonts/HackNerdFont-Bold.ttf",
            fn_italic="fonts/HackNerdFont-Italic.ttf",
            fn_bolditalic="fonts/HackNerdFont-BoldItalic.ttf",
        )
        theme_font_styles.append("HackNerdFont")
        self.theme_cls.font_styles["HackNerdFont"] = [
            "HackNerdFont",
            "16",
            False,
            0.15,
        ]

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        sm = ScreenManager()
        self.supplier_screen = SupplierScreen(name="sup")
        sm.add_widget(self.supplier_screen)
        sm.add_widget(SupplierDetailScreen(name="sup-detail"))
        return sm


if __name__ == "__main__":
    MainApp().run()
