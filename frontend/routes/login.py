from flask import Blueprint, render_template, redirect, url_for, session, flash, request, json
import urllib.request as cliente_http
from urllib.error import URLError, HTTPError

login_bp = Blueprint('login', __name__)

@login_bp.route('/registro', methods=['GET'])
def vista_registro():
    return render_template('registro.html')

@login_bp.route('/', methods=['POST'])
def procesar_registro():
    nombre = request.form.get('nombre_usuario')
    email = request.form.get('email')
    password = request.form.get('password')

    datos_registro = {
        "nombre_usuario": nombre,
        "email": email,
        "password": password
    }

    url_backend = "http://127.0.0.1:5000/endpoints/usuarios"

    try:
        data_json = json.dumps(datos_registro).encode('utf-8')

        req = cliente_http.Request(
            url_backend,
            data=data_json,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with cliente_http.urlopen(req) as respuesta:
            if respuesta.status == 201 or respuesta.status == 200:
                flash("¡Cuenta creada con exito. Ya podes iniciar sesion", "success")
                return redirect(url_for('login.login'))
        
    except HTTPError as e:
        flash("Error al registrarse. Revisá los datos.", "error")
        return redirect(url_for('login.vista_registro'))
    except URLError:
        flash("No se pudo conectar con el servidor.", "error")
        return redirect(url_for('login.vista_registro'))
    
    return redirect(url_for('login.vista_registro'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validación provisoria local
        if username == 'fiuba' and password == 'ids':
            
            session.permanent = True
            
            session['usuario_id'] = 100
            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('imanes.mostrar_heladera'))
        else:
            flash('Credenciales inválidas.', 'error')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login.login'))