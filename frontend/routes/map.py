import requests
from flask import Blueprint, render_template, session, redirect, url_for
from auth import login_required

BACKEND_URL = "http://localhost:5000"

mapa_bp = Blueprint('mapa', __name__)

@mapa_bp.route('/mapa')
@login_required 
def mostrar_mapa():
    id_usuario = session.get('user_id')

    url_backend = f"{BACKEND_URL}/usuarios/{id_usuario}/paises/visitados"
    
    paises_codigos = []
    try:
        response = requests.get(url_backend)
        if response.status_code == 200:
            paises_visitados = response.json()
            paises_codigos = [pais['codigo'] for pais in paises_visitados] # ISO de 3 letras
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el backend de lugares: {e}")

    return render_template('map.html', paises_visitados=paises_codigos)
