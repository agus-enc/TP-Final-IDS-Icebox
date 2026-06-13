from flask import Blueprint, session, jsonify, send_file, request
from ..dao.admin import obtener_estadisticas_viajes, obtener_estadisticas_ubicacion_imanes
from endpoints.services.admin import generar_grafico_viajes, generar_pdf_reporte, generar_grafico_imanes
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

    return jsonify({
        "status": "success", 
        "message": "Gráfico generado con éxito.",
        "ciudades": ciudades,
        "visitas": cantidades,
        "ubicaciones": ubicaciones, 
        "cant_imanes": cant_imanes
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
    
    ruta_grafico = 'backend_grafico/static/images/grafico_admin.png'
    ruta_grafico_imanes = generar_grafico_imanes()
    archivo_pdf = generar_pdf_reporte(ruta_grafico)

    return send_file(archivo_pdf, as_attachment=True)