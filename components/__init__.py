from kivy.app import App
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView


class Sidebar(MDFloatLayout):
    pass


# used in sidebar kivy file
class FlatButton(MDRectangleFlatButton):
    __width__ = NumericProperty()
    __height__ = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(size=self.set_width)

    def set_width(self, *args):
        self.width = self.__width__


class RV(MDRecycleView):
    def __init__(self, **kwargs) -> None:
        super(RV, self).__init__(**kwargs)
        app = App.get_running_app()
        app.rv = self
        self.data = []

    def load_data(self, model) -> None:
        data = model()._list()
        self.data = data
