import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from ..dao.admin import obtener_estadisticas_viajes, obtener_estadisticas_ubicacion_imanes, obtener_estadisticas_reseñas_por_ciudad, obtener_estadisticas_usuarios_mas_activos

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

def generar_grafico_reseñas():

    datos_db = obtener_estadisticas_reseñas_por_ciudad()
    ciudades = []
    cantidades = []

    if not datos_db:
        ciudades = ['Sin reseñas']
        cantidades = [0]
    else:
        for fila in datos_db:
            if isinstance(datos_db, tuple) and isinstance(datos_db[0], list):
                ciudades = datos_db[0]
                cantidades = datos_db[1]
            else:
                for fila in datos_db:
                    ciudades.append(fila.get('ciudad', ''))
                    cantidades.append(fila.get('total_reseñas', 0))
    
    plt.figure(figsize=(6, 6))
    colores = ['#7485e6', '#a3b1ff', '#cbd5e1', '#94a3b8', '#e2e8f0']
    
    plt.pie(cantidades, labels=ciudades, colors=colores, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': '#333333', 'linewidth': 2})
    plt.title('Top Ciudades con Más Reseñas', fontsize=12, fontweight='bold', pad=15)

    ruta_grafico_reseñas = os.path.join('frontend', 'static', 'images', 'grafico_resenas.png')
    os.makedirs(os.path.dirname(ruta_grafico_reseñas), exist_ok=True)
    
    plt.savefig(ruta_grafico_reseñas, bbox_inches='tight', dpi=1000)
    plt.close()
    
    return ruta_grafico_reseñas

def generar_grafico_usuarios_activos():

    datos_usuarios_db = obtener_estadisticas_usuarios_mas_activos()
    usuarios = []
    cant_viajes = []

    if datos_usuarios_db and isinstance(datos_usuarios_db, tuple) and len(datos_usuarios_db) == 2:
        usuarios = datos_usuarios_db[0]     
        cant_viajes = datos_usuarios_db[1]  
    else:
        usuarios = ['Sin usuarios']
        cant_viajes = [0]
    
    usuarios = usuarios[::-1]
    cant_viajes = cant_viajes[::-1]

    plt.figure(figsize=(6, 4))
    colores = ['#e2e8f0', '#cbd5e1', '#94a3b8', '#a3b1ff', '#7485e6']
    
    if len(usuarios) < 5:
        colores = colores[-len(usuarios):]

    barras = plt.barh(range(len(usuarios)), cant_viajes, color=colores, edgecolor='#333333', linewidth=1.5)
    plt.yticks(range(len(usuarios)), usuarios)
    
    plt.title('Ranking de Viajeros Frecuentes (Top 5)', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Cantidad de Viajes Creados', fontsize=10, fontweight='bold')
    
    plt.gca().xaxis.get_major_locator().set_params(integer=True)

    for barra in barras:
        ancho = barra.get_width()
        plt.text(ancho + 0.1, barra.get_y() + barra.get_height()/2, f'{int(ancho)}', va='center', ha='left', fontsize=10, fontweight='bold', color='#333333')

    plt.tight_layout()

    ruta_grafico_usuarios = os.path.join('frontend', 'static', 'images', 'grafico_usuarios_activos.png')
    os.makedirs(os.path.dirname(ruta_grafico_usuarios), exist_ok=True)
    
    plt.savefig(ruta_grafico_usuarios, dpi=150)
    plt.close()

    return ruta_grafico_usuarios

def generar_pdf_reporte(ruta_grafico, ruta_grafico_imanes, ruta_grafico_reseñas, ruta_grafico_usuarios):
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
        c.drawImage(ruta_grafico, 100, 350, width=400, height=280)
    
    if os.path.exists(ruta_grafico_imanes):
        c.drawImage(ruta_grafico_imanes, 100, 20, width=400, height=300)

    c.showPage()

    if os.path.exists(ruta_grafico_reseñas):
        c.drawImage(ruta_grafico_reseñas, 100, 350, width=400, height=300)

    if os.path.exists(ruta_grafico_usuarios):
        c.drawImage(ruta_grafico_usuarios, 100, 20, width=400, height=280)

    c.showPage()
    c.save()
    return ruta_pdf