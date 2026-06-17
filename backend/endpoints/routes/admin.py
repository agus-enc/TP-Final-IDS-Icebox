from flask import Blueprint, session, jsonify, send_file, request
from ..dao.admin import obtener_estadisticas_viajes, obtener_estadisticas_ubicacion_imanes, obtener_estadisticas_reseñas_por_ciudad, obtener_estadisticas_usuarios_mas_activos
from endpoints.services.admin import generar_grafico_viajes, generar_pdf_reporte, generar_grafico_imanes, generar_grafico_reseñas, generar_grafico_usuarios_activos
from endpoints.db import ejecutar_consulta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def vista_admin_dashboard():
    
    id_usuario = request.headers.get('X-User-Id')

    if not id_usuario:
        return jsonify({"status":"error","message":"Falta identificacion de usuario."}), 401
    
    sql = "SELECT rol FROM usuarios WHERE id_usuario = %s"
    response = ejecutar_consulta(sql, (id_usuario,))

    if not response or response[0]['rol'] != 'admin':
        return jsonify({"status":"error","message":"Acceso denegado, no eres administrador."}), 403
    
    generar_grafico_viajes()
    generar_grafico_imanes()
    generar_grafico_reseñas()
    generar_grafico_usuarios_activos()
    
    datos_db = obtener_estadisticas_viajes()
    ciudades = []
    cantidades = []

    if not datos_db:
        ciudades = ['Sin viajes cargados']
        cantidades = [0]
    else:
        for fila in datos_db:
            ciudades.append(fila['nombre'])
            cantidades.append(fila['cantidad'])

    datos_imanes_db = obtener_estadisticas_ubicacion_imanes()
    ubicaciones = []
    cant_imanes = []

    if not datos_imanes_db:
        ubicaciones = ['Sin imanes cargados']
        cant_imanes = [0]
    else:
        for fila in datos_imanes_db:
            ubicaciones.append(fila['ubicacion_heladera'])
            cant_imanes.append(fila['cantidad'])
    
    datos_reseñas_db = obtener_estadisticas_reseñas_por_ciudad()
    ciudades_reseñas = []
    cant_reseñas = []

    if datos_reseñas_db:
        if len(datos_reseñas_db) == 2 and isinstance(datos_reseñas_db[0], list) and any(isinstance(x, str) for x in datos_reseñas_db[0]):
            ciudades_reseñas = datos_reseñas_db[0]
            cant_reseñas = datos_reseñas_db[1]
        else:
            for fila in datos_reseñas_db:
                if isinstance(fila, dict):
                    ciudades_reseñas.append(fila.get('ciudad', ''))
                    cant_reseñas.append(fila.get('total_reseñas', 0))
                elif isinstance(fila, (list, tuple)) and len(fila) >= 2:
                    if isinstance(fila[0], (int, float)):
                        cant_reseñas.append(fila[0])
                        ciudades_reseñas.append(fila[1])
                    else:
                        ciudades_reseñas.append(fila[0])
                        cant_reseñas.append(fila[1])
    
    datos_usuarios_db = obtener_estadisticas_usuarios_mas_activos()

    
    if datos_usuarios_db and isinstance(datos_usuarios_db, tuple) and len(datos_usuarios_db) == 2:
        usuarios = [str(u) for u in datos_usuarios_db[0]]
        cant_viajes = [int(c) for c in datos_usuarios_db[1]]
    else:
        usuarios = ['Sin usuarios activos']
        cant_viajes = [0]

    return jsonify({
        "status": "success", 
        "message": "Gráfico generado con éxito.",
        "ciudades": ciudades,
        "visitas": cantidades,
        "ubicaciones": ubicaciones, 
        "cant_imanes": cant_imanes,
        "ciudades_reseñas": ciudades_reseñas,
        "cant_reseñas": cant_reseñas,
        "usuarios": usuarios,
        "cant_viajes": cant_viajes
    }), 200

@admin_bp.route('/admin/descargar-reporte', methods=['GET'])
def descargar_reporte():

    id_usuario = request.headers.get('X-User-Id')

    if not id_usuario:
        return jsonify({"status":"error","message":"Falta identificacion de usuario."}), 401
    
    sql = "SELECT rol FROM usuarios WHERE id_usuario = %s"
    response = ejecutar_consulta(sql, (id_usuario,))

    if not response or response[0]['rol'] != 'admin':
        return jsonify({"status":"error","message":"Acceso denegado, no eres administrador."}), 403
    
    ruta_grafico = generar_grafico_viajes()
    ruta_grafico_imanes = generar_grafico_imanes()
    ruta_grafico_reseñas = generar_grafico_reseñas()
    ruta_grafico_usuarios = generar_grafico_usuarios_activos()
    archivo_pdf = generar_pdf_reporte(ruta_grafico, ruta_grafico_imanes, ruta_grafico_reseñas, ruta_grafico_usuarios)

    return send_file(archivo_pdf, as_attachment=True)