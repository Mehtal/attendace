from kivy.uix.behaviors.cover import Decimal
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime


def calculate_penalty(data, num_retard):
    temp_rotation = data[2]
    temp_pointage = data[3]
    temp_r = datetime.strptime(temp_rotation, "%Y-%m-%d %H:%M")
    temp_p = datetime.strptime(temp_pointage, "%Y-%m-%d %H:%M:%S")
    time_diff_min = (temp_p - temp_r).total_seconds() / 60
    penalty = 0
    # Pour un time egal ou inférieur a 1 heur
    if 0 < time_diff_min < 60:
        penalty = data[4] * 0.1

    # un delai dune 1 heur de retard
    if time_diff_min >= 60:
        penalty = (data[4] * time_diff_min) / (8 * 60)
    # retard freéquents et répétitifs
    if num_retard > 4:
        penalty = penalty * 2
    return Decimal(f"{penalty:.2f}")


def create_facture(f_data, data, start, end, total):
    table_data = data
    filename = f"pdf/{f_data['nom']}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=14,
        leading=22,
        alignment=1,
        textColor=colors.darkblue,
    )
    total_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=14,
        leading=22,
        alignment=2,
        textColor=colors.darkblue,
    )
    total = Paragraph(f"TOTAL : {total:.2f}", total_style)

    title = Paragraph("FACTURE : ...........", title_style)
    today = datetime.today().strftime("%Y-%m-%d")
    fourniseur_info = """
        <b>Fourniseur :</b> {} <br/>
        <b>Telephone :</b> {} <br/>
        <b>adresse :</b> {} <br/>
        <b>Date :</b> {} <br/>
        <b>Periode :</b> {} - {} <br/>
    """
    fourniseur_info = fourniseur_info.format(
        f_data["nom"], f_data["phone"], f_data["adresse"], today, start[0:10], end[0:10]
    )

    fourniseur_para = Paragraph(fourniseur_info, styles["Normal"])

    header = ["Chauffeur", "Equipe", "Début", "Arrivage", "Prx", "Amende", "T/J"]
    table_data.insert(0, header)
    page_width, _ = A4
    col_widths = [page_width / (len(header) + 1)] * len(header)
    table = Table(table_data, colWidths=col_widths)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.green),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
        ]
    )
    table.setStyle(table_style)
    spacer = Spacer(1, 30)
    elements = [fourniseur_para, spacer, title, spacer, table, spacer, total]
    pdf.build(elements)
    return filename
