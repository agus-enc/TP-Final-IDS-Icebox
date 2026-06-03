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
    url = f"{BACKEND_URL}/api/admin/dashboard"
    headers = {'X-User-Id': str(session.get('id_usuario'))}

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