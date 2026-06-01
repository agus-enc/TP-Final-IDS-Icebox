import requests
from flask import Blueprint, render_template, session, redirect, url_for
from auth import login_required

BACKEND_URL = "http://localhost:5000/endpoints"

mapa_bp = Blueprint('mapa', __name__)

@mapa_bp.route('/mapa')
@login_required  
def mostrar_mapa():
    id_usuario = session.get('usuario_id')

    url_backend = f"{BACKEND_URL}/usuarios/{id_usuario}/paises/visitados"
    
    # 1. Datos de prueba
    paises_codigos = ["ARG", "ESP", "FRA"] 
    
    # 2. Datos de prueba
    datos_imanes = {
        "ARG": [
            {"nombre_ciudad": "Buenos Aires", "relato": "Hermosa capital"},
            {"nombre_ciudad": "Córdoba", "relato": "Muy buena comida"}
        ],
        "ESP": [
            {"nombre_ciudad": "Madrid", "relato": "Increíble museo del Prado"}
        ],
        "FRA": [
            {"nombre_ciudad": "París", "relato": "La ciudad de la luz"}
        ]
    }

    # paises_codigos = []
    try:
        response = requests.get(url_backend)
        if response.status_code == 200:
            paises_visitados = response.json()
            paises_codigos = [pais['codigo'] for pais in paises_visitados] # ISO de 3 letras
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el backend de lugares: {e}")

    # datos_imanes = {}
    for codigo in paises_codigos:
        url_imanes = f"{BACKEND_URL}/usuarios/{session.get('user_id')}/paises/{codigo}/imanes"
        try:
            resp_imanes = requests.get(url_imanes)
            if resp_imanes.status_code == 200:
                datos_imanes[codigo] = resp_imanes.json()
        except Exception as e:
            print(f"Error: {e}")

    return render_template('map.html', 
                           paises_visitados=paises_codigos, 
                           datos_imanes=datos_imanes)