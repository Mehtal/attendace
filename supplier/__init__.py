import os
import platform
import sqlite3
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors.cover import Decimal
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from facture import create_facture, calculate_penalty
from supplier.forms import FactureForm, SupplierForm
from supplier.models import Supplier


class SupplierDataRow(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    code = StringProperty()
    nom = StringProperty()
    telephone = StringProperty()
    adresse = StringProperty()

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

    def delete_supplier(self, id: str) -> None:
        self.supplier._delete(id)
        self.rv.load_data(Supplier)

    def open_facture_modal(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="UPDATE SUPPLIER", type="custom", content_cls=FactureForm()
            )
        form = self.dialog.content_cls
        button = MDRectangleFlatButton(
            text="GENERATE", on_release=lambda x: self.generate_pdf(form)
        )
        form.ids.id_btn_list.add_widget(button)
        self.dialog.open()

    def generate_pdf(self, form):
        f = form.ids
        fourniseur = form.fourniseur["code"]
        start = f.id_start_date.text
        end = f.id_end_date.text
        self.facture_with_date(fourniseur, start, end)

        self.dialog_close()

    def facture_with_date(self, code, start, end):
        conn = sqlite3.connect("sqlite.db")
        cursor = conn.cursor()
        query = """
        SELECT 
            d.nom AS chauffeur_nom,
            e.nom AS equipe_nom,
			p.rotation_start AS temp_rotation,
			p.timestamp AS temp_pointage,
            l.prix / 100.00  AS prix,
            f.nom AS nom_fourniseur,
            f.telephone ,
            f.adresse 
        FROM 
            pointage p
        JOIN 
            card c ON p.card = c.code 
        JOIN 
            equipe e ON c.code_equipe = e.code 
        JOIN 
            fourniseur f ON e.code_fourniseur = f.code
        JOIN 
            ligne l ON e.code_ligne = l.code
        JOIN
            chauffeur d ON e.code_chauffeur = d.code
        WHERE 
			p.entring = 1 
            AND e.code_fourniseur = ?
            AND DATE(p.timestamp) BETWEEN ? AND ?
        GROUP BY DATE(p.timestamp)
		ORDER BY p.timestamp ASC;
        """

        c = cursor.execute(query, (code, start, end))
        result = c.fetchall()
        if len(result) > 0:
            formatted_result = []
            fourniseur_info = {}
            total = 0
            for row in result:
                chauffeur_nom = row[0]
                equipe_nom = row[1]
                temp_rotation = row[2]
                temp_pointage = row[3]
                prix = row[4]

                formatted_result.append(
                    [
                        chauffeur_nom,
                        equipe_nom,
                        temp_rotation,
                        temp_pointage,
                        prix,
                    ]
                )

                fourniseur_info = {
                    "nom": result[0][5],
                    "phone": result[0][6],
                    "adresse": result[0][7],
                }

            num_retard = 0
            total = 0
            for data in formatted_result:
                penalty = calculate_penalty(data, num_retard)
                data.append(penalty)
                prix_jour = Decimal(data[4]) - Decimal(penalty)
                data.append(prix_jour)
                total += prix_jour
                if penalty:
                    num_retard += 1
            create_facture(fourniseur_info, formatted_result, start, end, total)

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
