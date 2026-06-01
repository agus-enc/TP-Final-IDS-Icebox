from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from auth import login_required
import requests

BACKEND_URL = "http://localhost:5000/endpoints"

imanes_bp = Blueprint('imanes', __name__)

@imanes_bp.route('/')
@imanes_bp.route('/heladera')
@login_required
def mostrar_heladera():
    usuario_id = session.get('usuario_id')
    imanes_heladera = []
    return render_template('heladera.html', imanes=imanes_heladera, usuario_id=usuario_id)

@imanes_bp.route('/cajon')
@login_required
def cajon():
    usuario_id = session.get('usuario_id')
    imanes_cajon = []
    return render_template('cajon.html', imanes=imanes_cajon, usuario_id=usuario_id)

@imanes_bp.route('/imanes', methods=['POST'])
# @login_required
def guardar_iman():
    id_viaje = request.form.get('id_viaje')

    # Red de seguridad obligatoria
    if not id_viaje:
        flash("Error crítico: No se identificó el viaje.", "error")
        return redirect(url_for('viajes.biblioteca'))

    # 1. Recolectar datos del formulario clásico de tu Editor/Creador
    id_parada = request.form.get('id_parada')
    tipo = request.form.get('tipo')
    pais = request.form.get('pais')
    archivo = request.files.get('archivo')

    # 2. Armar el paquete para reenviarlo a la API Backend
    datos = {
        'tipo': tipo,
        'id_parada': id_parada,
        'id_viaje': id_viaje
    }
    if pais:
        datos['pais'] = pais

    archivos = {}
    if archivo and archivo.filename != '':
        # Extraemos el archivo físico para mandarlo por HTTP multiparte
        archivos = {'archivo': (archivo.filename, archivo.read(), archivo.content_type)}

    try:
        # 3. Consumir nuestra propia API de la Fase 4
        respuesta = requests.post(f"{BACKEND_URL}/imanes", data=datos, files=archivos)

        if respuesta.status_code == 201:
            flash("¡Imán asignado con éxito!", "success")
        else:
            # 4. Si la regla SQL falla (Ej: "Ya usaste el imán de España"), leemos el JSON
            error_data = respuesta.json()
            if 'errors' in error_data and len(error_data['errors']) > 0:
                mensaje = error_data['errors'][0].get('message', 'Error desconocido.')
                descripcion = error_data['errors'][0].get('description', '')
                flash(f"{mensaje} {descripcion}", "error")
            else:
                flash("Error al procesar el imán en el servidor.", "error")

    except Exception as e:
        flash("Error de conexión con el servidor interno.", "error")

    # 5. El núcleo del Server-Side Rendering: Redirigimos para recargar el Editor
    return redirect(url_for('viajes.editor', id_viaje=id_viaje))