import os
import sys

from kivy.config import Config as cfg


cfg.set("graphics", "window_state", "maximized")

BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)


from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles

from components import FlatButton
from driver import DriverScreen
from supplier import SupplierDetailScreen, SupplierScreen
from ligne import LigneScreen
from team.screens import TeamScreen


class MainApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"

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
        sm.add_widget(LigneScreen(name="ligne"))
        self.supplier_screen = SupplierScreen(name="sup")
        sm.add_widget(self.supplier_screen)
        sm.add_widget(SupplierDetailScreen(name="sup-detail"))
        sm.add_widget(DriverScreen(name="driver"))
        sm.add_widget(TeamScreen(name="team"))
        return sm


if __name__ == "__main__":
    MainApp().run()
