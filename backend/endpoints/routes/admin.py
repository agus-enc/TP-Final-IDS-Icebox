from flask import Blueprint, session, jsonify, send_file
from services.admin import generar_grafico_viajes, generar_pdf_reporte

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def dashboard():
    
    if not session.get('usuario') or not session.get('es_admin'):
        return jsonify({"status": "success", "error": "Acceso denegado. No eres administrador."}), 403
    
    generar_grafico_viajes()
    return jsonify({"status": "success", "message": " Gráfico generado con éxito."}), 200


@admin_bp.route('/admin/descargar-reporte', methods=['GET'])
def descargar_reporte():

    if not session.get('usuario') or not session.get('es_admin'):
        return jsonify({"status": "error", "message": "Acceso denegado"}), 403
    
    ruta_grafico = 'frontend/static/images/grafico_admin.png'
    archivo_pdf = generar_pdf_reporte(ruta_grafico)

    return send_file(archivo_pdf, as_attachment=True)