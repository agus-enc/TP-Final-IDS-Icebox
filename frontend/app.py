from flask import Flask, render_template, redirect, url_for, session, flash, request
from functools import wraps
from datetime import timedelta
import json
import urllib.request as cliente_http 
from urllib.error import URLError, HTTPError

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'icebox_trips_secretkey'
app.permanent_session_lifetime = timedelta(hours=3)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicie sesión para acceder.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validación provisoria local
        if username == 'fiuba' and password == 'ids':
            session.permanent = True
            session['user_id'] = 100
            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('mostrar_heladera')) 
        else:
            flash('Credenciales inválidas.', 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/heladera')
@login_required
def mostrar_heladera():
    usuario_id = session.get('usuario_id')
    imanes_heladera = []
    return render_template('heladera.html', imanes=imanes_heladera, usuario_id=usuario_id)

@app.route('/cajon')
@login_required
def cajon():
    usuario_id = session.get('usuario_id')
    imanes_cajon = []
    return render_template('cajon.html', imanes=imanes_cajon, usuario_id=usuario_id)

@app.route('/map')
@login_required
def map():
    return render_template('map.html')


@app.route('/viaje/creador')
@login_required
def creador():
    return render_template('creador.html')


@app.route('/biblioteca')
@login_required
def biblioteca():
    return render_template('biblioteca.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000) 