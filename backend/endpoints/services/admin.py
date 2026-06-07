import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from endpoints.db import ejecutar_consulta

def obtener_estadisticas_viajes():
    """ Hace la consulta a la base de datos usando db.py para traer los destinos y cuantos viajes tiene cada uno """

    sql = """
        SELECT paises.nombre, COUNT(paradas.id_parada) AS cantidad
        FROM paradas
        INNER JOIN ciudades ON paradas.id_ciudad = ciudades.id_ciudad
        INNER JOIN paises ON ciudades.id_pais = paises.id_pais
        GROUP BY paises.id_pais, paises.nombre
        ORDER BY cantidad DESC
        LIMIT 5
    """
    resultados = ejecutar_consulta(sql, None)
    return resultados


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

def generar_pdf_reporte(ruta_grafico):
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

    c.showPage()
    c.save()
    return ruta_pdf