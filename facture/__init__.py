from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_facture(data):
    pdf = SimpleDocTemplate(f"{data[0][0]}.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=14,
        leading=22,
        alignment=1,  # Center alignment
        textColor=colors.darkblue,
    )

    title = Paragraph("facture", title_style)
    data = data
    print(data)
    header = ["Fourniseur", "Equipe", "Qté", "Prx Unitaire", "Montant Total"]
    data.insert(0, header)
    page_width, _ = A4
    col_widths = [page_width / (len(header) + 1)] * len(header)
    table = Table(data, colWidths=col_widths)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(table_style)
    spacer = Spacer(1, 12)
    elements = [title, spacer, table]
    pdf.build(elements)
