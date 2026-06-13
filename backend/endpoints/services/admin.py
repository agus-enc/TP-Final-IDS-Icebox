import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from endpoints.db import ejecutar_consulta
from ..dao.admin import obtener_estadisticas_viajes, obtener_estadisticas_ubicacion_imanes

def generar_grafico_viajes():

    datos_db = obtener_estadisticas_viajes()
    paises = []
    cantidades = []

    if not datos_db:
        paises = ['Sin viajes cargados']
        cantidades = [0]
    else:
        for fila in datos_db:
            paises.append(fila['nombre'])
            cantidades.append(fila['cantidad'])
    
    plt.figure(figsize=(6,4))
    plt.bar(paises, cantidades, color='#7485e6', edgecolor='#333333', linewidth=2)

    plt.title('Países mas visitados (Top 5)', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Países', fontweight='bold')
    plt.ylabel('Cantidad de Visitas', fontweight='bold')

    ruta_grafico = os.path.join('frontend', 'static', 'images', 'grafico_admin.png')
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)

    plt.savefig(ruta_grafico, bbox_inches='tight', dpi=1000)
    plt.close()
    return ruta_grafico

def generar_grafico_imanes():
    
    datos_db = obtener_estadisticas_ubicacion_imanes()
    ubicaciones = []
    cantidades = []
    
    if not datos_db:
        ubicaciones = ['Sin imanes cargados']
        cantidades = [0]

    else:
            for fila in datos_db:
                ubicaciones.append(fila['ubicacion_heladera'])
                cantidades.append(fila['cantidad'])

    plt.figure(figsize=(6, 6))
    
    colores = ['#7485e6', '#a3b1ff']
    
    plt.pie(cantidades, labels=ubicaciones, colors=colores, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': '#333333', 'linewidth': 2})
    plt.title('Distribución de Imanes (Heladera vs Cajón)', fontsize=12, fontweight='bold', pad=15)

    ruta_grafico = os.path.join('frontend', 'static', 'images', 'grafico_imanes.png')
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)
    
    plt.savefig(ruta_grafico, bbox_inches='tight', dpi=1000)
    plt.close()
    return ruta_grafico

def generar_pdf_reporte(ruta_grafico, ruta_grafico_imanes):
    """
    Genera el reporte PDF insertando la imagen del grafico
    """
    ruta_pdf = "reporte_admin.pdf"
    c = canvas.Canvas(ruta_pdf)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 750, "Informe Estadístico - Icebox Trips")

    c.setFont("Helvetica", 11)
    c.drawString(100, 725, "Análisis de metricas de usuario globales (Paradas por País).")
    c.drawString(100, 710, "Acceso reestringido - Solo administradores.")

    c.setLineWidth(1)
    c.line(100, 690, 500, 690)

    if os.path.exists(ruta_grafico):
        c.drawImage(ruta_grafico, 100, 350, width=400, height=300)
    
    if os.path.exists(ruta_grafico_imanes):
        c.drawString(100, 320, "Distribución de Imanes:")
        c.drawImage(ruta_grafico_imanes, 100, 20, width=400, height=280)

    c.showPage()
    c.save()
    return ruta_pdf