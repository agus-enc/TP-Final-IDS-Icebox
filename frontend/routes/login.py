from flask import Blueprint, render_template, redirect, url_for, session, flash, request, json
from constants import BACKEND_URL
import requests

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

    url_backend = f"{BACKEND_URL}/usuarios"

    try:
        respuesta = requests.post(url_backend, json=datos_registro)

        if respuesta.status_code in [200, 201]:
            flash("¡Cuenta creada con éxito! Ya podés iniciar sesión.", "success")
            return redirect(url_for('login.login'))
        else:
            flash("Error al registrarse, el email o contraseña ya pueden estar en uso.", "error")
            return redirect(url_for('login.vista_registro'))
        
    except requests.exceptions.RequestException:
        flash("No se pudo conectar con el servidor central.", "error")
        return redirect(url_for('login.vista_registro'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        nombre_usuario = request.form.get('nombre_usuario')
        password = request.form.get('password')

        datos_login = {
            'nombre_usuario': nombre_usuario,
            'password': password
        }

        url_backend = f"{BACKEND_URL}/usuarios/login"
        
        try:
            
            respuesta = requests.post(url_backend, json=datos_login)

            if respuesta.status_code == 200:
                
                respuesta_back = respuesta.json()
                datos_usuario = respuesta_back['usuario']

                session.permanent = True
                session['usuario_id'] = datos_usuario['id_usuario']
                session['nombre_usuario'] = datos_usuario['nombre_usuario']
                
                session['es_admin'] = (datos_usuario.get('rol') == 'admin')

                flash('¡Sesión iniciada correctamente!', 'success')

                if session['es_admin']:
                    return redirect(url_for('admin.vista_admin_dashboard'))
                else:
                    return redirect(url_for('imanes.mostrar_heladera'))
            
            elif respuesta.status_code in [400, 401]:
                
                flash('El usuario o la contraseña son incorrectos.', 'error')
            else:
                flash('Hubo un problema en el servidor central.', 'error')
                
            
        except requests.exceptions.RequestException:
            # Si el backend está apagado o no responde la red
            flash('No se pudo conectar con el servidor central.', 'error')

    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login.login'))