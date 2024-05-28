from time import time
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from pointage.models import Pointage
from rotation.models import Rotation
from horaire.models import Horaire
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivy.config import Config

from card.misc import read_qr_code
from card.models import Card
from datetime import timezone, datetime

Window.size = (360, 640)
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main = self.ids.main
        main.add_widget(
            MDRectangleFlatButton(
                text="Entree",
                font_size=24,
                size_hint=(1, 1),
                md_bg_color="#3498db",
                on_release=self.enter,
                theme_text_color="Custom",
                text_color="white",
            )
        )
        main.add_widget(
            MDRectangleFlatButton(
                text="Sortie",
                font_size=24,
                size_hint=(1, 1),
                md_bg_color="#3498db",
                on_release=self.sortie,
                theme_text_color="Custom",
                text_color="white",
            )
        )

    def enter(self, instance):
        self.manager.current = "enter"

    def sortie(self, instance):
        self.manager.current = "exit"


class EnterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rotation = Rotation()._list()
        box = self.ids.id_enter
        for item in rotation:
            box.add_widget(
                MDRectangleFlatButton(
                    text=item["nom"],
                    id=item["code"],
                    size_hint=(1, 1),
                    md_bg_color="#3498db",
                    font_size=24,
                    on_release=self.get_horaire,
                    theme_text_color="Custom",
                    text_color="white",
                )
            )

    def get_horaire(self, instance):
        horaire_list = Horaire()._list()
        data = []
        for horaire in horaire_list:
            if horaire["code_rotation"] == instance.id:
                data.append(horaire["entree"])

        third = self.manager.get_screen("third")
        third.add_bttons(data)
        self.manager.current = "third"


class ExitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rotation = Rotation()._list()
        box = self.ids.id_exit
        for item in rotation:
            box.add_widget(
                MDRectangleFlatButton(
                    text=item["nom"],
                    id=item["code"],
                    size_hint=(1, 1),
                    md_bg_color="#3498db",
                    font_size=24,
                    on_release=self.get_horaire,
                    theme_text_color="Custom",
                    text_color="white",
                )
            )

    def get_horaire(self, instance):
        horaire_list = Horaire()._list()
        data = []
        for horaire in horaire_list:
            if horaire["code_rotation"] == instance.id:
                data.append(horaire["sortie"])

        second = self.manager.get_screen("second")
        second.add_bttons(data)
        self.manager.current = "second"


class SecondScreen(Screen):

    def add_bttons(self, data):
        for item in data:
            self.ids.main.add_widget(
                MDRectangleFlatButton(
                    text=item,
                    size_hint=(1, 1),
                    md_bg_color="red",
                    font_size=24,
                    theme_text_color="Custom",
                    text_color="white",
                    on_release=self.pointage,
                )
            )

    def pointage(self, instance):
        card = read_qr_code()
        timestamp = datetime.now()
        pointage = Pointage()
        pointage.set_data(card, timestamp)
        pointage._create()
        self.manager.current = "first"


class ThirdScreen(Screen):

    def add_bttons(self, data):
        for item in data:
            self.ids.main.add_widget(
                MDRectangleFlatButton(
                    text=item,
                    size_hint=(1, 1),
                    md_bg_color="#04980b",
                    font_size=24,
                    theme_text_color="Custom",
                    text_color="white",
                    on_release=self.pointage,
                )
            )

    def pointage(self, instance):
        card = read_qr_code()
        today = datetime.today().strftime("%Y-%m-%d")
        rotation_start = f"{today} {instance.text}"
        timestamp = datetime.now()
        pointage = Pointage()
        pointage.set_data(card, timestamp, entring=1, rotation_start=rotation_start)
        pointage._create()
        self.ids.main.clear_widgets()
        self.manager.current = "first"


class PointageApp(MDApp):
    def build(self):
        Builder.load_file("kv/pointage.kv")
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name="first"))
        sm.add_widget(EnterScreen(name="enter"))
        sm.add_widget(ExitScreen(name="exit"))
        sm.add_widget(SecondScreen(name="second"))
        sm.add_widget(ThirdScreen(name="third"))
        return sm


if __name__ == "__main__":
    PointageApp().run()
