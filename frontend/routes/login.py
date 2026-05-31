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
    
    return redirect(url_for('login.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Capturamos los datos del formulario (Cambiamos username por email)
        email = request.form.get('email')
        password = request.form.get('password')

        # 2. Armamos el paquete JSON para el Backend
        datos_login = {
            "email": email,
            "password": password
        }

        # URL exacta de la ruta de login de tu Backend
        url_backend = "http://127.0.0.1:5000/usuarios/login" 

        try:
            # 3. Convertimos a JSON y preparamos la petición POST
            data_json = json.dumps(datos_login).encode('utf-8')
            req = cliente_http.Request(
                url_backend,
                data=data_json,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            # 4. Enviamos los datos al Backend y leemos la respuesta
            with cliente_http.urlopen(req) as respuesta:
                if respuesta.status == 200:
                    # El Back nos devuelve el JSON con los datos del usuario
                    respuesta_back = json.loads(respuesta.read().decode('utf-8'))
                    datos_usuario = respuesta_back['usuario']

                    # 5. Guardamos en la sesión de Flask los datos reales del usuario
                    session.permanent = True
                    session['usuario_id'] = datos_usuario['id_usuario']
                    session['nombre_usuario'] = datos_usuario['nombre_usuario']
                    
                    # 🔑 ACÁ SE ACTIVA EL CANDADO DEL ADMIN
                    # Si el rol es 'admin', esto se guarda como True. Si es 'usuario', como False.
                    session['es_admin'] = (datos_usuario.get('rol') == 'admin')

                    flash('¡Sesión iniciada correctamente!', 'success')

                    # 6. Redirección inteligente según el rol del usuario
                    if session['es_admin']:
                        return redirect(url_for('admin.admin_dashboard')) # Cambiá por el nombre real de tu ruta admin
                    else:
                        return redirect(url_for('imanes.mostrar_heladera'))

        except HTTPError as e:
            # Si el Back devuelve un 401 (Credenciales incorrectas)
            flash('El email o la contraseña son incorrectos.', 'error')
        except URLError:
            # Si el servidor Backend está apagado
            flash('No se pudo conectar con el servidor central.', 'error')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login.login'))