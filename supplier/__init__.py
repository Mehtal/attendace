from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from supplier.forms import SupplierForm
from supplier.models import Supplier


class SupplierDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

    def delete_data(self, model):
        model._delete(self.code)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        self.telephone = data["telephone"]
        self.adresse = data["adresse"]
        super().refresh_view_attrs(rv, index, data)


class SupplierScreen(Screen):
    supplier = Supplier()
    dialog = None

    def on_kv_post(self, base_widget):
        self.rv = self.ids.id_rv
        self.rv.viewclass = SupplierDataRow
        self.rv.load_data(Supplier)

    def detail_supplier(self, code):
        detail_screen = self.manager.get_screen("sup-detail")
        detail_screen.model = self.supplier
        detail_screen.load_data(code)
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


class SupplierDetailScreen(Screen):
    model = ObjectProperty

    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, code):
        self.data = self.model._read(code)
        self.code = str(self.data["code"])
        self.nom = self.data["nom"]
        self.telephone = self.data["telephone"]
        self.adresse = self.data["adresse"]

    def create_supplier(self, form):
        screen = self.manager.get_screen("sup")
        screen.create_supplier(form)
        self.manager.current = "sup"
