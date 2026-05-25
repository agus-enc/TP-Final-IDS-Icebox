from flask import Flask, render_template, redirect, url_for, session, flash, request
from functools import wraps
from datetime import timedelta

app = Flask(__name__,
            template_folder='template',
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'icebox_trips_secretkey'
app.permanent_session_lifetime = timedelta(hours=3)

#Control de acceso
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicie sesion para acceder.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #validacion provisoria local
        if username == 'fiuba' and password == 'ids':
            session.permanent = True
            session['user_id'] = 100
            flash('Sesion iniciada correctamente', 'success')
            return redirect(url_for('heladera'))
        else:
            flash('Credenciales invalidas.', 'error')
        
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada.', 'success')
    return redirect(url_for('login'))

#RUTAS DE INTEGRACION DE VISTAS
@app.route('/')

@app.route('/heladera')
@login_required
def heladera():
    render_template('heladera.html')


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

@app.route('/cajon')
@login_required
def cajon():
    return render_template('cajon.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)