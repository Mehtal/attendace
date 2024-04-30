from kivy.lang.builder import Builder

from .screens import LigneScreen
from .forms import LigneForm

Builder.load_file("ligne/screens/ligne_screen.kv")
Builder.load_file("ligne/forms/ligne_form.kv")
