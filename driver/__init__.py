from kivy.lang.builder import Builder

from .screens import DriverScreen

kv_list = [
    "driver/forms/driver_form.kv",
    "driver/screens/driver_screen.kv",
]
for file in kv_list:
    Builder.load_file(file)
