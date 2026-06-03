from flask import Blueprint, render_template, session, redirect, url_for, flash
from constants import BACKEND_URL
import requests

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def vista_admin_dashboard():
    
    if not session.get('es_admin'):
        flash("No tenes acceso a esta vista. Solo administradores.", "error")
        
        return redirect(url_for('imanes.mostrar_heladera'))
    
    #CONEXION CON EL BACK
    url = f"{BACKEND_URL}/admin/dashboard"
    headers = {'X-User-Id': str(session.get('usuario_id'))}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return render_template('admin_dashboard.html')
        else:
            flash("Error de autorizacion en el servidor.", "error")
            return redirect(url_for('imanes.mostrar_heladera'))
        
    except requests.exceptions.RequestException:
        flash("No se pudo conectar con el servidor de estadísticas.", "error")
        return redirect(url_for('imanes.mostrar_heladera'))


@admin_bp.route('/admin/descargar-reporte', methods=['GET'])
def descargar_reporte():
    # 1. Le va a pedir el PDF al backend real
    url = f"{BACKEND_URL}/admin/descargar-reporte"
    headers = {'X-User-Id': str(session.get('usuario_id'))}
    
    response = requests.get(url, headers=headers)
    
    # 2. Si el backend devuelve el archivo, el front lo descarga
    if response.status_code == 200:
        from flask import Response
        return Response(response.content, mimetype='application/pdf', 
                        headers={"Content-Disposition": "attachment;filename=reporte.pdf"})
        
    flash("No se pudo descargar el reporte", "error")
    return redirect(url_for('admin.vista_admin_dashboard'))