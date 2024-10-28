from importlib.metadata import files
from operator import attrgetter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfgen import canvas

from processor.data_processor import gasto_anual


def graph(lista_gastos):
    #lista_gastos = [Gasto(concepto, gasto) for concepto, gasto in gasto_anual_concepto.items()]

    lista_gastos = sorted(lista_gastos, key=lambda x:x.gasto, reverse=True)
    conceptos = [g.concepto for g in lista_gastos]
    gastos = [g.gasto for g in lista_gastos]

    plt.figure(figsize=(10,8))
    plt.barh(conceptos, gastos, color='skyblue')
    plt.xlabel('Gasto')
    plt.ylabel('Concepto')
    plt.title('Anual')
    plt.gca().invert_yaxis()
    # plt.show()

def reporte_gastos(lista_gastos):
    contenido = []
    df = pd.DataFrame([(g.concepto, g.gasto) for g in lista_gastos], columns=['Concepto','Gasto'])
    df_ordenado_az = df.sort_values(by='Concepto')
    df_ordenado_gastos = df.sort_values(by='Gasto', ascending=False)

    # crear pdf
    pdf = SimpleDocTemplate("Gastos.pdf", pagesize=letter)

    contenido.append(generar_archivo(df_ordenado_az, "Alfabetico"))
    contenido.append(generar_archivo(df_ordenado_gastos, "Gastos mayor a menor"))

    # pdf.build([item for sublist in contenido for item in sublist])
    # pdf.build([item for sublist in contenido for item in sublist])


def generar_pdf(lista_gastos):
    dataframe = pd.DataFrame([(g.concepto, g.gasto) for g in lista_gastos], columns=['Concepto', 'Gasto'])
    outout_path = Path.cwd()
    pdf = FPDF(orientation="landscape", format="a3")
    pdf.add_page()
    pdf.set_font("Times", size=12)

    line_height = pdf.font_size * 17.5
    #col_width = pdf.epw / 5

    for row in dataframe:
        for v in row:
            print(v)
            pdf.multi_cell(0, 0, str(v), border=1, align="L")
        pdf.ln(line_height)
    file_name = Path(f"{outout_path}\\gastos.pdf")
    pdf.output(name="gastos.pdf",dest="F")


def generar_archivo(lista_gastos):
    gastos_ordenados = sorted(lista_gastos, key=attrgetter('gasto'), reverse=True)
    c = canvas.Canvas("gastos.pdf", pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height -40, "Reporte Gastos Anual (M -> m)")

    y = height - 80
    c.setFont("Helvetica",12)

    # agregar gastos
    for gasto in gastos_ordenados:
        c.drawString(100, y, f"{gasto.concepto}:     ${gasto.gasto:.2f}")
        y-=20

        if y <50:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica",12)
    c.save()


