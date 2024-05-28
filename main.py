import os

from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder

from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles

from driver import DriverScreen
from supplier import SupplierDetailScreen, SupplierScreen
from ligne import LigneScreen
from team import TeamScreen
from rotation import RotationScreen
from card import CardScreen
from horaire import HoraireScreen
from pointage import PointageScreen
from login import LoginScreen
from components import Sidebar


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

        # Load kiv files
        kv_directory = "kv"
        for filename in os.listdir(kv_directory):
            if filename.endswith(".kv"):
                file_path = os.path.join(kv_directory, filename)
                Builder.load_file(file_path)

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SupplierScreen(name="sup"))
        sm.add_widget(TeamScreen(name="team"))
        sm.add_widget(RotationScreen(name="rotation"))
        sm.add_widget(LigneScreen(name="ligne"))
        sm.add_widget(DriverScreen(name="driver"))
        sm.add_widget(CardScreen(name="card"))
        sm.add_widget(SupplierDetailScreen(name="sup-detail"))
        sm.add_widget(HoraireScreen(name="horaire"))
        sm.add_widget(PointageScreen(name="pointage"))
        return sm


if __name__ == "__main__":
    MainApp().run()
