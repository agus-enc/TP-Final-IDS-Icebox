import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from auth import login_required
BACKEND_URL = "http://localhost:5000/endpoints"

viajes_bp = Blueprint('viajes', __name__)

@viajes_bp.route('/viaje/creador')
@login_required
def creador():
    return render_template('creador.html')

@viajes_bp.route('/biblioteca')
@login_required
def biblioteca():
    return render_template('biblioteca.html')

@viajes_bp.route('/viajes/<int:id_viaje>/editar', methods=['GET', 'POST'])
def editor(id_viaje):
    if request.method == 'POST':
        # 1. ACTUALIZAR TÍTULO
        titulo_nuevo = request.form.get('titulo_viaje')
        requests.put(f"{BACKEND_URL}/viajes/{id_viaje}", json={"titulo": titulo_nuevo})

        foto_portada = request.files.get('foto_portada')
        if foto_portada and foto_portada.filename != '':
            archivos = {'imagen': (foto_portada.filename, foto_portada.read(), foto_portada.content_type)}
            datos = {'tipo': 'header'}
            res_img = requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes", files=archivos, data=datos)

            if res_img.status_code not in [200, 201]:
                print(f"ERROR AL SUBIR PORTADA: {res_img.status_code} - {res_img.text}")
            else:
                print("PORTADA SUBIDA CON ÉXITO")

        # 2. PROCESAR BORRADO DE PORTADA Y PARADAS
        if request.form.get('borrar_portada') == 'true':
            requests.delete(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes/header")

        str_borradas = request.form.get('paradas_borradas')
        if str_borradas:
            ids_a_borrar = str_borradas.split(',')
            for id_p in ids_a_borrar:
                if id_p.strip():
                    requests.delete(f"{BACKEND_URL}/paradas/{id_p.strip()}")

        # 4. PROCESAR FORMULARIO
        for key in request.form.keys():
            if key.startswith('texto_parada_'):
                indice = key.split('_')[-1]
                id_parada = request.form.get(f'id_parada_{indice}')
                id_ciudad = request.form.get(f'ciudad_parada_{indice}')
                texto = request.form.get(f'texto_parada_{indice}')

                payload_parada = {
                    "id_viaje": id_viaje,
                    "id_ciudad": int(id_ciudad) if id_ciudad else 0,
                    "orden_en_ruta": int(indice),
                    "texto_resena": texto
                }

                if id_parada:
                    requests.put(f"{BACKEND_URL}/paradas/{id_parada}", json=payload_parada)
                else:
                    requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/paradas", json=payload_parada)

        return redirect(url_for('viajes.editor', id_viaje=id_viaje))

    # GET: CARGAR LA PÁGINA
    resp_viaje = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}")
    viaje_real = resp_viaje.json() if resp_viaje.status_code == 200 else {}

    resp_paradas = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}/paradas")
    paradas_reales = resp_paradas.json() if resp_paradas.status_code == 200 else []

    resp_lugares = requests.get(f"{BACKEND_URL}/ciudades")
    lugares_reales = resp_lugares.json() if resp_lugares.status_code == 200 else []

    resp_imagenes = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes")
    imagenes_reales = resp_imagenes.json() if resp_imagenes.status_code == 200 else []

    # Busca si existe alguna imagen de tipo "header" y extrae su URL
    viaje_real['url_portada'] = next((img['imagen_url'] for img in imagenes_reales if img['tipo'] == 'header'), None)

    return render_template('editor.html', viaje=viaje_real, paradas=paradas_reales, lugares=lugares_reales)