from kivy.app import App
from kivy.graphics import Color, Line
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView

kv_list = [
    "components/sidebar.kv",
    "components/table.kv",
]
for file in kv_list:
    Builder.load_file(file)


class Sidebar(MDFloatLayout):
    pass


class FlatButton(MDRectangleFlatButton):
    __width__ = NumericProperty()
    __height__ = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(size=self.set_width)

    def set_width(self, *args):
        self.width = self.__width__


class DataCell(MDLabel):
    def __init__(self, **kwargs):
        super(DataCell, self).__init__(**kwargs)
        self.padding = dp(8)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.line = Line(width=2)
        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        self.line.rectangle = (self.x, self.y, self.width, self.height)


class DriverDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    prenom = StringProperty()
    code_fourniseur = StringProperty()
    nom_fourniseur = StringProperty()

    def delete_data(self, model):
        model._delete(self.code)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.code = data["code"]
        self.nom = data["nom"]
        self.prenom = data["prenom"]
        self.code_fourniseur = data["code_fourniseur"]
        self.nom_fourniseur = data["nom_fourniseur"]
        super().refresh_view_attrs(rv, index, data)


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


class RV(MDRecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        app = App.get_running_app()
        app.rv = self
        self.data = []

    def load_data(self, model) -> None:
        data = model()._list()
        self.data = data
