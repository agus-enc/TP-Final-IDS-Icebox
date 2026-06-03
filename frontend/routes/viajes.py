import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils import parsear_formulario_paradas, procesar_paquete_iman
from constants import BACKEND_URL
from auth import login_required

viajes_bp = Blueprint('viajes', __name__)

@viajes_bp.route('/biblioteca')
@login_required
def biblioteca():
    usuario_id = session.get('usuario_id')
    url_pedir_viajes = f"{BACKEND_URL}/{usuario_id}/viajes"
    resp = requests.get(url_pedir_viajes)
    
    if resp.status_code == 200:
        viajes = resp.json()
    else:
        viajes = []
        
    return render_template('biblioteca.html', viajes=viajes)

@viajes_bp.route('/viajes/<int:id_viaje>/editar', methods=['GET', 'POST'])
@login_required
def editor(id_viaje):
    if request.method == 'POST':
        # 1. Actualizar Título y Portada
        titulo_nuevo = request.form.get('titulo_viaje')
        requests.put(f"{BACKEND_URL}/viajes/{id_viaje}", json={"titulo": titulo_nuevo})

        foto_portada = request.files.get('foto_portada')
        if foto_portada and foto_portada.filename != '':
            archivos = {'imagen': (foto_portada.filename, foto_portada.read(), foto_portada.content_type)}
            requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes", files=archivos, data={'tipo': 'header'})

        if request.form.get('borrar_portada') == 'true':
            requests.delete(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes/header")

        # 2. Borrar paradas eliminadas en la UI
        str_borradas = request.form.get('paradas_borradas')
        if str_borradas:
            ids_a_borrar = str_borradas.split(',')
            for id_p in ids_a_borrar:
                if id_p.strip():
                    requests.delete(f"{BACKEND_URL}/paradas/{id_p.strip()}")

        # 3. Procesar Paradas e Imanes usando los Helpers
        paradas_data = parsear_formulario_paradas(request.form, request.files)
        lote_imanes = []
        archivos_imanes = {}

        for p_data in paradas_data:
            payload_parada = {
                "id_viaje": id_viaje,
                "id_ciudad": p_data['id_ciudad'],
                "orden_en_ruta": p_data['indice'],
                "texto_resena": p_data['texto_resena']
            }

            id_parada = p_data['id_parada']

            # A. Guardar o Actualizar Parada
            if id_parada:
                requests.put(f"{BACKEND_URL}/paradas/{id_parada}", json=payload_parada)
            else:
                resp_parada = requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/paradas", json=payload_parada)
                if resp_parada.status_code in [200, 201]:
                    id_parada = resp_parada.json().get('id_parada')

            # B. Empaquetar Imán
            if id_parada:
                procesar_paquete_iman(lote_imanes, archivos_imanes, id_parada, p_data)

        # 4. Enviar Batch de Imanes
        if lote_imanes:
            payload_batch = {"id_viaje": id_viaje, "imanes_data": json.dumps(lote_imanes)}
            res_batch = requests.post(f"{BACKEND_URL}/imanes/batch", data=payload_batch, files=archivos_imanes)

            if res_batch.status_code != 201:
                try:
                    error_data = res_batch.json()
                    mensaje = error_data['errors'][0].get('message', '') if 'errors' in error_data else ''
                    flash(f"Cambios guardados, pero falló un imán: {mensaje}", "error")
                except:
                    flash("Cambios guardados, pero ocurrió un error con los imanes.", "error")
            else:
                flash("¡Viaje e imanes actualizados con éxito!", "success")
        else:
            flash("¡Viaje guardado con éxito!", "success")

        return redirect(url_for('viajes.editor', id_viaje=id_viaje))

    # GET: CARGAR LA PÁGINA (Sin cambios estructurales)
    resp_viaje = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}")
    viaje_real = resp_viaje.json() if resp_viaje.status_code == 200 else {}

    resp_paradas = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}/paradas")
    paradas_reales = resp_paradas.json() if resp_paradas.status_code == 200 else []

    resp_lugares = requests.get(f"{BACKEND_URL}/ciudades")
    lugares_reales = resp_lugares.json() if resp_lugares.status_code == 200 else []

    resp_imagenes = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes")
    imagenes_reales = resp_imagenes.json() if resp_imagenes.status_code == 200 else []

    viaje_real['url_portada'] = next((img['imagen_url'] for img in imagenes_reales if img['tipo'] == 'header'), None)

    return render_template('editor.html', viaje=viaje_real, paradas=paradas_reales, lugares=lugares_reales)

@viajes_bp.route('/mockup-diario')
def mockup_diario():
    return render_template('diario.html')

@viajes_bp.route('/crear_viaje', methods=['GET', 'POST'])
@login_required
def crear_viaje():
    if request.method == 'POST':
        # 1. CREAR EL VIAJE PADRE
        titulo = request.form.get('titulo_viaje')
        if not titulo:
            flash("El título del viaje es obligatorio.", "error")
            return redirect(url_for('viajes.crear_viaje'))

        # EXTRAEMOS EL ID DEL USUARIO DESDE LA SESIÓN DE FLASK
        usuario_id = session.get('usuario_id')

        # AGREGAMOS EL ID A LA URL DEL BACKEND
        res_v = requests.post(f"{BACKEND_URL}/{usuario_id}/viajes", json={"titulo": titulo})

        if res_v.status_code not in [200, 201]:
            flash("Error crítico al crear el viaje en el servidor.", "error")
            return redirect(url_for('viajes.biblioteca'))

        id_viaje = res_v.json().get('id_viaje')

        # 2. PROCESAR PORTADA (Opcional)
        foto_portada = request.files.get('foto_portada')
        if foto_portada and foto_portada.filename != '':
            archivos = {'imagen': (foto_portada.filename, foto_portada.read(), foto_portada.content_type)}
            requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/imagenes", files=archivos, data={'tipo': 'header'})

        # 3. CREAR PARADAS Y EMPAQUETAR IMANES (Usando Helpers)
        paradas_data = parsear_formulario_paradas(request.form, request.files)
        lote_imanes = []
        archivos_imanes = {}

        for p_data in paradas_data:
            payload_parada = {
                "id_viaje": id_viaje,
                "id_ciudad": p_data['id_ciudad'],
                "orden_en_ruta": p_data['indice'],
                "texto_resena": p_data['texto_resena']
            }

            # A. Guardamos la Parada
            resp_parada = requests.post(f"{BACKEND_URL}/viajes/{id_viaje}/paradas", json=payload_parada)

            if resp_parada.status_code in [200, 201]:
                id_parada = resp_parada.json().get('id_parada')

                # B. Empaquetar Imán
                procesar_paquete_iman(lote_imanes, archivos_imanes, id_parada, p_data)

        # 4. ENVIAR BATCH DE IMANES AL BACKEND
        if lote_imanes:
            payload_batch = {"id_viaje": id_viaje, "imanes_data": json.dumps(lote_imanes)}
            res_batch = requests.post(f"{BACKEND_URL}/imanes/batch", data=payload_batch, files=archivos_imanes)

            if res_batch.status_code != 201:
                flash("Viaje creado, pero hubo un error de validación con los imanes elegidos.", "error")
            else:
                flash("¡Viaje y sus imanes creados con éxito!", "success")
        else:
            flash("¡Viaje creado con éxito!", "success")

        # Redirigimos al editor del viaje recién creado
        return redirect(url_for('viajes.editor', id_viaje=id_viaje))

    # GET: Cargar la pantalla vacía
    resp_lugares = requests.get(f"{BACKEND_URL}/ciudades")
    lugares_reales = resp_lugares.json() if resp_lugares.status_code == 200 else []
    return render_template('creador.html', lugares=lugares_reales)

@viajes_bp.route('/viajes/<int:id_viaje>/borrar', methods=['POST'])
@login_required
def borrar_viaje(id_viaje):
    resp = requests.delete(f"{BACKEND_URL}/viajes/{id_viaje}")
    if resp.status_code in [200, 204]:
         flash("Viaje eliminado con éxito", "success")
    else:
         flash("Error al eliminar el viaje", "error")
        
    return redirect(url_for('viajes.biblioteca'))