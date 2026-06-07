from flask import Blueprint, session, jsonify, send_file, request
from endpoints.services.admin import generar_grafico_viajes, generar_pdf_reporte, obtener_estadisticas_viajes
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

    # 3. Mandamos el JSON con los datos incluidos
    return jsonify({
        "status": "success", 
        "message": "Gráfico generado con éxito.",
        "ciudades": ciudades,
        "visitas": cantidades
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
    
    ruta_grafico = 'frontend/static/images/grafico_admin.png'
    archivo_pdf = generar_pdf_reporte(ruta_grafico)

    return send_file(archivo_pdf, as_attachment=True)