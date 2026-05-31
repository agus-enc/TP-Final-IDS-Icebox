from flask import Blueprint, render_template, session, redirect, url_for, flash
import urllib.request as cliente_http
from urllib.error import URLError, HTTPError

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def vista_admin_dashboard():
    if not session.get('es_admin'):

        flash("No tenes acceso a esta vista. Solo administradores.", "error")
        return redirect(url_for('imanes.mostrar_heladera'))
    
    #CONEXION CON EL BACK
    url_backend = "http://127.0.0.1:5000/endpoints/admin/dashboard" 

    try:
        req = cliente_http.Request(url_backend, method='GET')
        with cliente_http.urlopen(req) as respuesta:
            
            if respuesta.status == 200:
                return render_template('admin_dashboard.html')
    
    except (HTTPError, URLError):
        flash("Error de autorización en el servidor", "error")
        return render_template('imanes.mostrar_heladera')

    return render_template('admin_dashboard.html')