from kivy.lang.builder import Builder

from .forms import SupplierForm
from .models import Supplier
from .screens import SupplierDetailScreen, SupplierScreen

kv_list = [
    "supplier/forms/supplier_form.kv",
    "supplier/screens/detail.kv",
    "supplier/screens/supplier_screen.kv",
]
for file in kv_list:
    Builder.load_file(file)
